from tests.data.result_test_data import *
import random  # see tests.test_update
from google.appengine.api import memcache
from models.root import *

class WinnerData(ResultTestData):

    def __init__(self,year,week_number,data_name,leave_objects_in_datastore=False):
        self.year = year
        self.week_number = week_number
        self.set_week_state('not_started')
        self.featured_game_state('not_started')
        self.number_of_leaders(0)
        self.number_of_players(0)
        self.tiebreaker_winner(None)
        self.week_official()
        self.game_data = dict()
        ResultTestData.__init__(self,year=year,week_number=week_number,data_name=data_name,leave_objects_in_datastore=leave_objects_in_datastore)

    def set_week_state(self,state):
        self.__week_state = state

    def week_official(self):
        self.__week_official = True

    def week_unofficial(self):
        self.__week_official = False

    def featured_game_state(self,state):
        self.__featured_state = state

    def number_of_leaders(self,num_leaders):
        self.__num_leaders = num_leaders

    def number_of_players(self,num_players):
        self.__num_players = num_players

    def tiebreaker_winner(self,tiebreak_number):
        self.__tiebreak = tiebreak_number

    def setup_database(self):
        self.__setup_players()
        self.__setup_game_teams()

        if self.__week_state == "not_started":
            self.__setup_week_not_started()
        elif self.__week_state == "final":
            self.__setup_week_final()

    # defined in result_test_data
    #def cleanup(self):
        #pass

    def __setup_players(self):
        assert self.__num_players >= self.__num_leaders
        player_names = [ "Player %d" % (player_num) for player_num in range(self.__num_players) ]
        self.setup_players(player_names)

    def __setup_week_not_started(self,seed=111):
        random.seed(seed)

        for game_number in range(1,11):
            self.__setup_random_game(game_number,"not_started")

        self.setup_week()

        # don't care about player picks, just set up some picks for each player with dummy data
        for name in self.players:
            for game_number in range(1,11):
                self.__create_random_pick(name,game_number)

    def __setup_week_final(self,seed=777):
        random.seed(seed)

        for game_number in range(1,11):
            self.__setup_random_game(game_number,"final")

        self.__setup_leaders_and_non_leaders()

    def __setup_game_teams(self):
        game_team_names = dict()
        game_team_names[1] = ("Arizona", "Colorado")
        game_team_names[2] = ("Virginia","Virginia Tech")
        game_team_names[3] = ("Iowa","Kansas")                 
        game_team_names[4] = ("Louisiana Monroe","Maryland")               
        game_team_names[5] = ("Michigan", "Mississippi")            
        game_team_names[6] = ("Nevada", "Northwestern")           
        game_team_names[7] = ("Oklahoma State", "Pittsburgh")             
        game_team_names[8] = ("South Alabama", "Southern Miss")          
        game_team_names[9] = ("Temple","Stanford")               
        game_team_names[10] = ("Georgia", "Georgia Tech")

        game_teams = dict()
        for game_number in game_team_names:
            team1,team2 = game_team_names[game_number]
            team1_key = self.team_lookup[team1]
            team2_key = self.team_lookup[team2]
            game_teams[game_number] = (team1_key,team2_key)

        self.game_team_keys = game_teams

    def __not_started_game(self,number):
        team1_key,team2_key = self.game_team_keys[number]
        parent = root_games(self.year,self.week_number)
        game = Game(number=number,team1=team1_key,team2=team2_key,team1_score=None,team2_score=None,favored="team2",spread=0.5,state="not_started",quarter=None,time_left=None,date=None,parent=parent)
        return game

    def __in_progress_game(self,number,favored="team1",spread=0.5,team1_score=19,team2_score=20,quarter="3rd",time_left="7:00"):
        team1_key,team2_key = self.game_team_keys[number]
        parent = root_games(self.year,self.week_number)
        game = Game(number=number,team1=team1_key,team2=team2_key,team1_score=team1_score,team2_score=team2_score,favored=favored,spread=spread,state="in_progress",quarter=quarter,time_left=time_left,date=None,parent=parent)
        return game

    def __final_game(self,number,favored="team1",spread=0.5,team1_score=30,team2_score=29):
        team1_key,team2_key = self.game_team_keys[number]
        parent = root_games(self.year,self.week_number)
        game = Game(number=number,team1=team1_key,team2=team2_key,team1_score=team1_score,team2_score=team2_score,favored=favored,spread=spread,state="final",quarter=None,time_left=None,date=None,parent=parent)
        return game

    # return randomly chosen winners and losers
    # assume that random.seed set for repeatability
    def __get_winners_and_losers(self):
        num_losers = self.__num_players - self.__num_leaders
        player_keys = self.players.values()
        indexes = range(len(player_keys))
        random.shuffle(indexes)

        winner_index = indexes[:self.__num_leaders]
        loser_index = indexes[self.__num_leaders:]

        winner_keys = [player_keys[i] for i in winner_index ]
        loser_keys = [player_keys[i] for i in loser_index ]

        winners = [ self.__get_player_name(player_key) for player_key in winner_keys ]
        losers = [ self.__get_player_name(player_key) for player_key in loser_keys ]

        return winners,losers

    def __get_player_name(self,player_key):
        for name in self.players:
            if self.players[name] == player_key:
                return name
        raise AssertionError, "could not find player"

    # assumes random.seed already called
    def __setup_random_game(self,game_number,state):
        favored = random.choice(["team1","team2"])
        spread = float(random.randint(0,15)) + 0.5
        team1_score = random.randint(0,50)
        team2_score = random.randint(0,50)
        team1_key,team2_key = self.game_team_keys[game_number]
        parent = root_games(self.year,self.week_number)

        if state == "not_started":
            team1_score = None
            team2_score = None

        if state == "in_progress":
            quarter = "1st"
            time_left = "3:00"
        else:
            quarter = ""
            time_left = ""

        game = Game(number=game_number,team1=team1_key,team2=team2_key,team1_score=team1_score,team2_score=team2_score,favored=favored,spread=spread,state=state,quarter=quarter,time_left=time_left,date=None,parent=parent)

        self.setup_game(game)
        self.game_data[game_number] = game

    def __create_random_pick(self,player_name,game_number):
        win_or_lose = random.choice(["win","lose"])
        self.__create_pick(player_name,game_number,win_or_lose)

    def __create_winning_pick(self,player_name,game_number,win_tiebreak=None):
        self.__create_pick(player_name,game_number,"win",win_tiebreak)

    def __create_losing_pick(self,player_name,game_number):
        self.__create_pick(player_name,game_number,"lose")

    def __create_pick(self,player_name,game_number,win_or_lose,win_tiebreak=None):
        game = self.game_data[game_number]

        p = Pick(parent=root_picks(self.year,self.week_number))
        if win_or_lose == "win":
            p.winner = self.__get_game_winner(game)
        else:
            p.winner = self.__get_game_loser(game)

        if game_number == 10:
            p.team1_score,p.team2_score = self.__featured_game_pick_score(game,win_tiebreak)
        else:
            p.team1_score = None
            p.team2_score = None

        self.setup_pick(p,player_name,game_number)

    # assumes random.seed already called
    def __setup_leaders_and_non_leaders(self):
        winners,losers = self.__get_winners_and_losers()

        # pick a winner
        if self.__week_official or self.__tiebreak != None:
            names = list(winners)
            random_winner_name = random.choice(names)
            random_winner_key = str(self.players[random_winner_name])

        if self.__week_official:
            self.setup_week(winner=random_winner_key)
        else:
            self.setup_week()

        leading_wins = random.randint(5,9)

        for player_name in winners:
            featured_game_result = self.__get_featured_game_expected_result(player_name,random_winner_name)
            games_to_win,games_to_lose = self.__get_games_to_win_and_lose(leading_wins,featured_game_result)
            for game_number in games_to_win:
                should_player_win_tiebreak = player_name == random_winner_name
                self.__create_winning_pick(player_name,game_number,should_player_win_tiebreak)
            for game_number in games_to_lose:
                self.__create_losing_pick(player_name,game_number)

        for player_name in losers:
            num_wins = random.randint(0,leading_wins-1)
            games_to_win,games_to_lose = self.__get_games_to_win_and_lose(num_wins)
            for game_number in games_to_win:
                self.__create_winning_pick(player_name,game_number)
            for game_number in games_to_lose:
                self.__create_losing_pick(player_name,game_number)


    def __get_games_to_win_and_lose(self,num_wins,featured_game_result=None):
        if featured_game_result == "win":
            assert num_wins > 1
            game_numbers = range(1,10)
            random.shuffle(game_numbers)
            game_numbers.insert(0,10)  # place feature game at front to ensure a win
            wins = game_numbers[:num_wins]
            losses = game_numbers[num_wins:]
        elif featured_game_result == "loss":
            assert num_wins < 10,"num wins = %d" % (num_wins)
            game_numbers = range(1,10)
            random.shuffle(game_numbers)
            game_numbers.append(10)  # place feature game at back to ensure a loss
            wins = game_numbers[:num_wins]
            losses = game_numbers[num_wins:]
        else:
            game_numbers = range(1,11)
            random.shuffle(game_numbers)
            wins = game_numbers[:num_wins]
            losses = game_numbers[num_wins:]

        return wins,losses

    def __get_game_winner(self,game):
        if self.__is_team1_winning(game):
            return "team1"
        elif self.__is_team2_winning(game):
            return "team2"
        else:
            raise AssertionError,"neither team winning, unexpected"

    def __get_game_loser(self,game):
        if self.__is_team1_winning(game):
            return "team2"
        elif self.__is_team2_winning(game):
            return "team1"
        else:
            raise AssertionError,"neither team winning, unexpected"


    def __is_team1_winning(self,game):
        score_diff = game.team2_score-game.team1_score
        if game.favored == "team2":
            spread = game.spread
        elif game.favored == "team1":
            spread = -game.spread
        else:
            raise AssertionError,"game.favored has an invalid value"
        return score_diff < spread
        
        
    def __is_team2_winning(self,game):
        score_diff = game.team2_score-game.team1_score
        if game.favored == "team2":
            spread = game.spread
        elif game.favored == "team1":
            spread = -game.spread
        else:
            raise AssertionError,"game.favored has an invalid value"
        return score_diff > spread

    def __get_featured_game_expected_result(self,player_name,winner_name):
        assert self.__tiebreak != None and self.__tiebreak <= 3 and self.__tiebreak >= 0

        if self.__tiebreak == None:
            return None

        # ensure that tiebreak 0 wins (1 player chooses featured game correctly)
        if self.__tiebreak == 0:
            if player_name == winner_name:
                return "win"
            else:
                return "loss"

        # all other tiebreaks, return a win to advance to next tiebreak
        return "win"

    def __featured_game_pick_score(self,game,win_tiebreak):
        assert self.__tiebreak != None and self.__tiebreak <= 3 and self.__tiebreak >= 0

        tiebreak_does_not_matter = win_tiebreak == None
        if tiebreak_does_not_matter or self.__tiebreak == 0:
            team1_score = random.randint(0,50)
            team2_score = random.randint(0,50)
            return team1_score,team2_score

        result_spread = game.team1_score - game.team2_score
        result_total = game.team1_score + game.team2_score

        if self.__tiebreak == 1:
            team2_score = random.randint(0,50)

            if win_tiebreak:
                team1_score = team2_score + result_spread
            else:
                team1_score = team2_score + result_spread + random.randint(1,20)

            return team1_score,team2_score

        if self.__tiebreak == 2:
            team1_score = 10
            team2_score = 0
            total_difference = abs(result_total - team1_score - team2_score)
            spread_difference = abs(team1_score - team2_score - result_spread)

            if not win_tiebreak:
                diff = 0
                i = 0
                while diff < total_difference:
                    team2_score = random.randint(10,50)
                    team1_score = team2_score + spread_difference
                    diff = abs(result_total - team1_score - team2_score)
                    i += 1
                    if i > 50:
                        raise AssertionError,"Error could not find a score"

            return team1_score,team2_score



