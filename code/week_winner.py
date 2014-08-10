from code.update import *
from code.database import *
from code.calculator import *

class WeekWinnerData:
    featured_game_state = None
    winner = None
    projected = None
    official = None
    num_tied_for_first = None

class WeekWinnerCalculationData:
    player_wins = None
    player_projected_wins = None
    featured_game = None
    featured_game_winner = None
    featured_game_ahead = None
    player_featured_game_picks = None
    player_submit_times = None
    week_state = None
    week = None  # TODO unsure if needed

class WeekWinner:
    calculated_winner = None
    players_tied_for_first = None
    players_won_tiebreak0 = None
    players_lost_tiebreak0 = None
    players_won_tiebreak1 = None
    players_lost_tiebreak1 = None
    players_won_tiebreak2 = None
    players_lost_tiebreak2 = None
    players_won_tiebreak3 = None
    players_lost_tiebreak3 = None

    def __init__(self,year,week_number):
        self.__data = self.__setup_data_to_use(year,week_number)
        if self.__data.week_state == "in_progress":
            self.use_projected_winner = True
        else:
            self.use_projected_winner = False

        self.__calculate_tied_for_first()
        self.__calculate_tiebreaker_0()
        self.__calculate_tiebreaker_1()
        self.__calculate_tiebreaker_2()
        self.__calculate_tiebreaker_3()
        self.__calculate_winner()


    def get_winner(self):
        if self.__data.week.winner != None:
            return self.__data.week.winner

        if self.__data.featured_game.state == "not_started":
            return None

        if self.__data.featured_game.state == "in_progress":
            return None

        return self.calculated_winner

    def get_projected_winner(self):
        if self.__data.featured_game.state == "in_progress":
            return self.calculated_winner
        return None

    def verify_winner(self):
        if self.__data.featured_game.state != "final":
            return None
        return self.calculated_winner != None and len(self.calculated_winner) == 1 and self.calculated_winner[0] == self.__data.week.winner

    def get_players_tied_for_first(self):
        return self.players_tied_for_first

    def get_players_that_won_tiebreak_0(self):
        return self.players_won_tiebreak0

    def get_players_that_lost_tiebreak_0(self):
        return self.players_lost_tiebreak0

    def get_players_that_won_tiebreak_1(self):
        return self.players_won_tiebreak1

    def get_players_that_lost_tiebreak_1(self):
        return self.players_lost_tiebreak1

    def get_players_that_won_tiebreak_2(self):
        return self.players_won_tiebreak2

    def get_players_that_lost_tiebreak_2(self):
        return self.players_lost_tiebreak2

    def get_players_that_won_tiebreak_3(self):
        return self.players_won_tiebreak3

    def get_players_that_lost_tiebreak_3(self):
        return self.players_lost_tiebreak3

    # if cannot determine correct winner, this will be False
    # example use case:  cannot determine winner of tiebreak 3
    def is_winner_valid(self):
        return self.__winner_valid

    def __calculate_winner(self):

        self.__winner_valid = True

        if self.is_tiebreaker_3_valid():
            if self.players_won_tiebreak3 == None or len(self.players_won_tiebreak3) != 1:
                self.calculated_winner = None  # unexpected error
                self.__winner_valid = False
                return
            self.calculated_winner = self.players_won_tiebreak3[0]
            return
        else:
            unable_to_determine_winner = self.players_won_tiebreak2 != None and len(self.players_won_tiebreak2) > 1
            if unable_to_determine_winner:
                self.calculated_winner = self.players_won_tiebreak3
                self.__winner_valid = False
                return

        if self.players_won_tiebreak2 != None and len(self.players_won_tiebreak2) == 1:
            self.calculated_winner = self.players_won_tiebreak2[0]
            return

        if self.players_won_tiebreak1 != None and len(self.players_won_tiebreak1) == 1:
            self.calculated_winner = self.players_won_tiebreak1[0]
            return

        if self.players_won_tiebreak0 != None and len(self.players_won_tiebreak0) == 1:
            self.calculated_winner = self.players_won_tiebreak0[0]
            return

        if self.players_tied_for_first != None and len(self.players_tied_for_first) == 1:
            self.calculated_winner = self.players_tied_for_first[0]
            return

        self.calculated_winner = None
        self.__winner_valid = False

    def is_winner_official(self):
        return self.__data.week.winner != None

    def __calculate_tied_for_first(self):
        if self.use_projected_winner:
            player_wins = self.__data.player_projected_wins
        else:
            player_wins = self.__data.player_wins

        most_wins = max(player_wins.values())
        self.players_tied_for_first = [player_key for player_key in player_wins if player_wins[player_key] == most_wins]


    def __calculate_tiebreaker_0(self):
        if self.tiebreaker_0_unnecessary():
            self.players_won_tiebreak0 = None
            self.players_lost_tiebreak0 = None
            return

        if self.__data.featured_game.state == "not_started":
            self.players_won_tiebreak0 = None
            self.players_lost_tiebreak0 = None
            return

        if self.__data.featured_game.state == "final":
            featured_winner = self.__data.featured_game_winner
        elif self.__data.featured_game.state == "in_progress":
            featured_winner = self.__data.featured_game_ahead
        else:
            raise AssertionError,"Should not reach here"

        self.players_won_tiebreak0 = []
        self.players_lost_tiebreak0 = []

        for player_key in self.players_tied_for_first:
            player_pick = self.__data.player_featured_game_picks[player_key]
            if player_pick.winner == featured_winner:
                self.players_won_tiebreak0.append(player_key)
            else: 
                self.players_lost_tiebreak0.append(player_key)

    def __calculate_tiebreaker_1(self):
        if self.tiebreaker_1_unnecessary():
            self.players_won_tiebreak1 = None
            self.players_lost_tiebreak1 = None
            return

        players = self.__get_players_to_use(tiebreaker_number=1)

        game = self.__data.featured_game
        result_spread = game.team1_score - game.team2_score

        # find the min difference
        min_difference = 0
        first_valid_pick = True
        for player_key in players:
            pick = self.__data.player_featured_game_picks[player_key]

            # no score entered
            if pick.team1_score == None or pick.team2_score == None:
                continue

            pick_spread = pick.team1_score - pick.team2_score
            pick_difference = abs(pick_spread-result_spread) 
            if first_valid_pick or pick_difference < min_difference:
                min_difference = pick_difference
                first_valid_pick = False

        # calculate who won/lost
        self.players_won_tiebreak1 = []
        self.players_lost_tiebreak1 = []
        for player_key in players:
            pick = self.__data.player_featured_game_picks[player_key]

            # no score entered
            if pick.team1_score == None or pick.team2_score == None:
                self.players_lost_tiebreak1.append(player_key)

            pick_spread = pick.team1_score - pick.team2_score
            pick_difference = abs(pick_spread-result_spread) 
            if pick_difference == min_difference:
                self.players_won_tiebreak1.append(player_key)
            else:
                self.players_lost_tiebreak1.append(player_key)


    def __calculate_tiebreaker_2(self):
        if self.tiebreaker_2_unnecessary():
            self.players_won_tiebreak2 = None
            self.players_lost_tiebreak2 = None
            return

        players = self.__get_players_to_use(tiebreaker_number=2)

        game = self.__data.featured_game
        result_total = game.team1_score + game.team2_score

        # find the min difference
        min_difference = 0
        first_valid_pick = True
        for player_key in players:
            pick = self.__data.player_featured_game_picks[player_key]

            # no score entered
            if pick.team1_score == None or pick.team2_score == None:
                continue

            pick_total = pick.team1_score + pick.team2_score
            pick_difference = abs(result_total-pick_total)
            if first_valid_pick or pick_difference < min_difference:
                min_difference = pick_difference
                first_valid_pick = False

        # calculate who won/lost
        self.players_won_tiebreak2 = []
        self.players_lost_tiebreak2 = []
        for player_key in players:
            pick = self.__data.player_featured_game_picks[player_key]

            # no score entered
            if pick.team1_score == None or pick.team2_score == None:
                self.players_lost_tiebreak2.append(player_key)

            pick_total = pick.team1_score + pick.team2_score
            pick_difference = abs(result_total-pick_total)
            if pick_difference == min_difference:
                self.players_won_tiebreak2.append(player_key)
            else:
                self.players_lost_tiebreak2.append(player_key)

    def __calculate_tiebreaker_3(self):
        self.__tiebreaker_3_valid = False

        if self.tiebreaker_3_unnecessary():
            self.players_won_tiebreak3 = None
            self.players_lost_tiebreak3 = None
            return

        players = self.__get_players_to_use(tiebreaker_number=3)
        self.players_won_tiebreak3 = []
        self.players_lost_tiebreak3 = []

        entry_times = [ value for value in self.__data.player_submit_times.values() if value != None ]
        if len(entry_times) == 0:
            for player_key in players:
                self.players_won_tiebreak3.append(player_key)
            return

        self.__tiebreaker_3_valid = True
        earliest_time = min(entry_times)
        for player_key in players:
            if self.__data.player_submit_times[player_key] == earliest_time:
                self.players_won_tiebreak3.append(player_key)
            else:
                self.players_lost_tiebreak3.append(player_key)

    def tiebreaker_0_unnecessary(self):
        return len(self.players_tied_for_first) == 1

    def tiebreaker_1_unnecessary(self):
        one_player_won_tiebreak0 = self.players_won_tiebreak0 != None and len(self.players_won_tiebreak0) == 1
        return self.tiebreaker_0_unnecessary() or one_player_won_tiebreak0

    def tiebreaker_2_unnecessary(self):
        one_player_won_tiebreak1 = self.players_won_tiebreak1 != None and len(self.players_won_tiebreak1) == 1
        return self.tiebreaker_1_unnecessary() or one_player_won_tiebreak1

    def tiebreaker_3_unnecessary(self):
        one_player_won_tiebreak2 = self.players_won_tiebreak2 != None and len(self.players_won_tiebreak2) == 1
        return self.tiebreaker_2_unnecessary() or one_player_won_tiebreak2

    # tiebreaker 3 is valid when: 
    # - week.lock_picks is set (i.e a pick deadline set)
    # - the picks were entered before the pick deadline
    # - the submit time makes sense (i.e. submit time year matches the week.year)
    # TODO:  consider adding a pick submit time to Picks data model?
    #        If Picks.created or Picks.modified gets corrupted, submit time won't be valid
    def is_tiebreaker_3_valid(self):
        return self.__tiebreaker_3_valid

    def __get_players_to_use(self,tiebreaker_number):
        # tiebreak0:  use players tied for first
        # tiebreak1:  use tiebreak0 or players tied for first
        # tiebreak2:  use tiebreak1, tiebreak0, players tied for first
        # tiebreak3:  use tiebreak2, tiebreak1, tiebreak0, players_tied_for_first
        if tiebreaker_number == 0:
            return self.players_tied_for_first

        no_tiebreak_0_players =  self.players_won_tiebreak0 == None or len(self.players_won_tiebreak0) == 0
        no_tiebreak_1_players =  self.players_won_tiebreak1 == None or len(self.players_won_tiebreak1) == 0
        no_tiebreak_2_players =  self.players_won_tiebreak2 == None or len(self.players_won_tiebreak2) == 0

        if tiebreaker_number == 1:
            if no_tiebreak_0_players:
                return self.players_tied_for_first
            return self.players_won_tiebreak0

        if tiebreaker_number == 2:
            if no_tiebreak_1_players:
                if no_tiebreak_0_players:
                    return self.players_tied_for_first
                else:
                    return self.players_won_tiebreak0
            else:
                return self.players_won_tiebreak1

        if tiebreaker_number == 3:
            if no_tiebreak_2_players:
                if no_tiebreak_1_players:
                    if no_tiebreak_0_players:
                        return self.players_tied_for_first
                    else:
                        return self.players_won_tiebreak0
                else:
                    return self.players_won_tiebreak1
            else:
                return self.players_won_tiebreak2

        raise AssertionError,"tiebreaker_number %d is invalid." % (tiebreaker_number)

    def get_winner_data_object(self):
        w = WeekWinnerData()
        w.featured_game_state = self.__data.featured_game.state
        w.winner = self.get_winner()
        w.projected = self.get_projected_winner()
        w.official = self.is_winner_official()
        w.num_tied_for_first = len(self.players_tied_for_first)
        return w

    def get_week_winner_data(self):
        return self.__data

    def __setup_data_to_use(self,year,week_number):
        database = Database()
        week_data = database.load_week_data(year,week_number)
        calc = CalculateResults(week_data)

        data = WeekWinnerCalculationData()
        data.player_wins = dict()
        data.player_projected_wins = dict()
        data.player_featured_game_picks = dict()
        data.player_submit_times = dict()
        data.week_state = calc.get_summary_state_of_all_games()
        data.featured_game = calc.get_featured_game()
        data.week = week_data.week

        featured_game_key = str(data.featured_game.key())

        if data.featured_game.state == "not_started":
            data.featured_game_winner = None
            data.featured_game_ahead = None
        if data.featured_game.state == "in_progress":
            data.featured_game_winner = None
            data.featured_game_ahead = calc.get_team_winning_pool_game(featured_game_key)
        if data.featured_game.state == "final":
            data.featured_game_winner = calc.get_pool_game_winner(featured_game_key)
            data.featured_game_ahead = None

        for player_key in week_data.players:
            data.player_wins[player_key] = calc.get_number_of_wins(player_key)
            data.player_projected_wins[player_key] = calc.get_number_of_projected_wins(player_key)
            data.player_featured_game_picks[player_key] = calc.get_player_pick_for_game(player_key,featured_game_key)
            data.player_submit_times[player_key] = calc.get_player_submit_time(player_key,data.week)
        return data

