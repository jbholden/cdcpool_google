from week_winner import *
from database import *
from calculator import *

class Tiebreak:

    def __init__(self,year,week_number):
        self.__winners = WeekWinner(year,week_number)
        self.__week_data = database.load_week_data(year,week_number)
        self.__calc = Calculator(self.__week_data)

        self.__calculate_tiebreak_summary_details()
        self.__calculate_tiebreaker0_details()
        self.__calculate_tiebreaker1_details()
        self.__calculate_tiebreaker2_details()
        self.__calculate_tiebreaker3_details()

    def was_able_to_determine_winner(self):
        return self.__winners.is_winner_valid()

    def get_tiebreaker_summary(self):
        return self.__tiebreak_summary

    def get_tiebreaker0_details(self):
        return self.__tiebreak0_details

    def get_tiebreaker1_details(self):
        return self.__tiebreak1_details

    def get_tiebreaker2_details(self):
        return self.__tiebreak2_details

    def get_tiebreaker3_details(self):
        return self.__tiebreak3_details

    def get_tiebreaker1_summary(self):
        return self.__tiebreak1_summary

    def get_tiebreaker2_summary(self):
        return self.__tiebreak2_summary

    def get_tiebreaker3_summary(self):
        return self.__tiebreak3_summary

    def __calculate_tiebreak_summary_details(self):
        details = dict()
        players = self.__winners.get_players_tied_for_first()
        for player_key in players:
            d = TiebreakSummary()
            d.player_key = player_key
            d.player_name = self.__get_player_name(player_key)
            details[player_key] = d

            number_of_tiebreaks = 0
            tiebreak0 = None
            tiebreak1 = None
            tiebreak2 = None
            tiebreak3 = None

        t0_players_won = self.__winners.get_players_that_won_tiebreak_0()
        t0_players_lost = self.__winners.get_players_that_lost_tiebreak_0()
        t1_players_won = self.__winners.get_players_that_won_tiebreak_1()
        t1_players_lost = self.__winners.get_players_that_lost_tiebreak_1()
        t2_players_won = self.__winners.get_players_that_won_tiebreak_2()
        t2_players_lost = self.__winners.get_players_that_lost_tiebreak_2()
        t3_players_won = self.__winners.get_players_that_won_tiebreak_3()
        t3_players_lost = self.__winners.get_players_that_lost_tiebreak_3()

        for player_key in t0_players_won:
            result = self.__get_tiebreak_result("win")
            css_id = self.__get_tiebreak_id(result)

            details[player_key].tiebreak0 = result
            details[player_key].tiebreak0_id = css_id
            details[player_key].number_of_tiebreaks += 1

        for player_key in t0_players_lost:
            result = self.__get_tiebreak_result("loss")
            css_id = self.__get_tiebreak_id(result)

            details[player_key].tiebreak0 = result
            details[player_key].tiebreak0_id = css_id
            details[player_key].number_of_tiebreaks += 1


        for player_key in t1_players_won:
            result = self.__get_tiebreak_result("win")
            css_id = self.__get_tiebreak_id(result)

            details[player_key].tiebreak1 = result
            details[player_key].tiebreak1_id = css_id
            details[player_key].number_of_tiebreaks += 1

        for player_key in t1_players_lost:
            result = self.__get_tiebreak_result("loss")
            css_id = self.__get_tiebreak_id(result)

            details[player_key].tiebreak1 = result
            details[player_key].tiebreak1_id = css_id
            details[player_key].number_of_tiebreaks += 1

        for player_key in t2_players_won:
            result = self.__get_tiebreak_result("win")
            css_id = self.__get_tiebreak_id(result)

            details[player_key].tiebreak2 = result
            details[player_key].tiebreak2_id = css_id
            details[player_key].number_of_tiebreaks += 1

        for player_key in t2_players_lost:
            result = self.__get_tiebreak_result("loss")
            css_id = self.__get_tiebreak_id(result)

            details[player_key].tiebreak2 = result
            details[player_key].tiebreak2_id = css_id
            details[player_key].number_of_tiebreaks += 1

        for player_key in t3_players_won:
            result = self.__get_tiebreak_result("win")
            css_id = self.__get_tiebreak_id(result)

            details[player_key].tiebreak3 = result
            details[player_key].tiebreak3_id = css_id
            details[player_key].number_of_tiebreaks += 1

        for player_key in t3_players_lost:
            result = self.__get_tiebreak_result("loss")
            css_id = self.__get_tiebreak_id(result)

            details[player_key].tiebreak3 = result
            details[player_key].tiebreak3_id = css_id
            details[player_key].number_of_tiebreaks += 1

        self.__tiebreak_summary = self.__sort_tiebreak_summary(details.values())

    def __calculate_tiebreaker0_details(self):
        details = []

        players = self.__winners.get_players_that_won_tiebreak_0()
        winner_data = self.__winners.get_week_winner_data()
        featured_game_key = str(winner_data.featured_game.key())

        for player_key in players:
            d = Tiebreak0Data()
            d.player_key = player_key
            d.player_name = self.__get_player_name(player_key)
            d.player_pick = self.__calc.get_team_name_player_picked_to_win(player_key,featured_game_key)
            d.result = self.__get_tiebreak_result("win")
            d.featured_game_winner = self.__get_featured_game_winner()
            details.append(d)

        players = self.__winners.get_players_that_lost_tiebreak_0()
        for player_key in players:
            d = Tiebreak0Data()
            d.player_key = player_key
            d.player_name = self.__get_player_name(player_key)
            d.player_pick = self.__calc.get_team_name_player_picked_to_win(player_key,featured_game_key)
            d.result = self.__get_tiebreak_result("loss")
            d.featured_game_winner = self.__get_featured_game_winner()
            details.append(d)

        self.__tiebreak0_details = self.__sort_tiebreak0(details)

    def __calculate_tiebreaker1_details(self):
        details = []

        winner_data = self.__winners.get_week_winner_data()
        featured_game_key = str(winner_data.featured_game.key())

        summary = Tiebreak1Summary()
        summary.team1 = self.__week_data.get_team1_name(featured_game_key)
        summary.team2 = self.__week_data.get_team2_name(featured_game_key)
        summary.team1_score = winner_data.featured_game.team1_score
        summary.team2_score = winner_data.featured_game.team2_score
        summary.result_spread = summary.team1_score - summary.team2_score

        players = self.__winners.get_players_that_won_tiebreak_1()

        for player_key in players:
            d = Tiebreak1Data()
            d.player_key = player_key
            d.player_name = self.__get_player_name(player_key)
            d.result = self.__get_tiebreak_result("win")

            pick = self.__calc.get_player_pick_for_game(player_key,featured_game_key)

            d.team1_score = pick.team1_score
            d.team2_score = pick.team2_score
            d.pick_spread = pick.team1_score - pick.team2_score
            d.difference = abs(d.pick_spread - summary.result_spread)

            details.append(d)

        players = self.__winners.get_players_that_lost_tiebreak_1()

        for player_key in players:
            d = Tiebreak1Data()
            d.player_key = player_key
            d.player_name = self.__get_player_name(player_key)
            d.result = self.__get_tiebreak_result("loss")

            pick = self.__calc.get_player_pick_for_game(player_key,featured_game_key)

            d.team1_score = pick.team1_score
            d.team2_score = pick.team2_score
            d.pick_spread = pick.team1_score - pick.team2_score
            d.difference = abs(d.pick_spread - summary.result_spread)

            details.append(d)

        self.__tiebreak1_summary = summary
        self.__tiebreak1_details = self.__sort_tiebreak1(details)

    def __calculate_tiebreaker2_details(self):
        details = []

        winner_data = self.__winners.get_week_winner_data()
        featured_game_key = str(winner_data.featured_game.key())

        summary = Tiebreak2Summary()
        summary.team1 = self.__week_data.get_team1_name(featured_game_key)
        summary.team2 = self.__week_data.get_team2_name(featured_game_key)
        summary.team1_score = winner_data.featured_game.team1_score
        summary.team2_score = winner_data.featured_game.team2_score
        summary.result_total = summary.team1_score + summary.team2_score

        players = self.__winners.get_players_that_won_tiebreak_2()

        for player_key in players:
            d = Tiebreak2Data()
            d.player_key = player_key
            d.player_name = self.__get_player_name(player_key)
            d.result = self.__get_tiebreak_result("win")

            pick = self.__calc.get_player_pick_for_game(player_key,featured_game_key)

            d.team1_score = pick.team1_score
            d.team2_score = pick.team2_score
            d.pick_total = pick.team1_score + pick.team2_score
            d.difference = abs(summary.result_total - d.pick_total)

            details.append(d)

        players = self.__winners.get_players_that_lost_tiebreak_2()

        for player_key in players:
            d = Tiebreak2Data()
            d.player_key = player_key
            d.player_name = self.__get_player_name(player_key)
            d.result = self.__get_tiebreak_result("loss")

            pick = self.__calc.get_player_pick_for_game(player_key,featured_game_key)

            d.team1_score = pick.team1_score
            d.team2_score = pick.team2_score
            d.pick_total = pick.team1_score + pick.team2_score
            d.difference = abs(summary.result_total - d.pick_total)

            details.append(d)

        self.__tiebreak2_summary = summary
        self.__tiebreak2_details = self.__sort_tiebreak2(details)

    def __calculate_tiebreaker3_details(self):
        details = []

        summary = Tiebreak3Summary()
        summary.valid = self.__winners.is_tiebreaker_3_valid()

        players = self.__winners.get_players_that_won_tiebreak_3()
        for player_key in players:
            d = Tiebreak3Data()
            d.player_key = player_key
            d.player_name = self.__get_player_name(player_key)
            d.result = self.__get_tiebreak_result("win")
            d.pick_entry_time = self.__get_player_submit_time(player_key)
            details.append(d)

        players = self.__winners.get_players_that_lost_tiebreak_3()
        for player_key in players:
            d = Tiebreak3Data()
            d.player_key = player_key
            d.player_name = self.__get_player_name(player_key)
            d.result = self.__get_tiebreak_result("loss")
            d.pick_entry_time = self.__get_player_submit_time(player_key)
            details.append(d)

        self.__tiebreak3_summary = summary
        self.__tiebreak3_details = self.__sort_tiebreak3(details)

    def __get_player_name(self,player_key):
        return self.__week_data.players[player_key].name

    def __get_tiebreak_id(self,value):
        if value == "won":
            return "tiebreak-won"
        elif value == "lost":
            return "tiebreak-lost"
        elif value == "ahead":
            return "tiebreak-ahead"
        elif value == "behind":
            return "tiebreak-behind"
        else:
            return "tiebreak-blank"

    def __get_tiebreak_result(self,win_loss):
        winner_data = self.__winners.get_week_winner_data()
        featured_game = winner_data.featured_game

        if featured_game.state == "not_started":
            return ""

        if featured_game.state == "in_progress" and win_loss == "win":
            return "ahead"

        if featured_game.state == "in_progress" and win_loss == "loss":
            return "behind"

        if featured_game.state == "final" and win_loss == "win":
            return "won"

        if featured_game.state == "final" and win_loss == "loss":
            return "lost"

        if win_loss != "win" or win_loss != "loss":
            raise AssertionError,"Bad win_loss value %s" % (win_loss)
            return

        raise AssertionError,"Bad state value %s" % (featured_game.state)

    def __get_featured_game_winner(self):
        winner_data = self.__winners.get_week_winner_data()
        featured_game = winner_data.featured_game

        if featured_game.state == "not_started":
            return ""

        if featured_game.state == "in_progress":
            return self.__calc.get_team_name_winning_pool_game(featured_game_key)

        if featured_game.state == "final":
            return self.__calc.get_pool_game_winner_team_name(featured_game_key)

        raise AssertionError,"Bad state value %s" % (featured_game.state)

    def __get_player_submit_time(self,player_key):
        winner_data = self.__winners.get_week_winner_data()
        pick_entry_time = winner_data.player_submit_times[player_key]

        if pick_entry_time == None:
            return "indeterminate"

        return pick_entry_time.strftime("%m/%d/%y %I:%M:%S %p UTC")

    def __sort_tiebreak_summary(self,summary):
        sort_by_name = sorted(summary,key=lambda item:item.player_name)
        sort_by_wins = sorted(sort_by_name,key=lambda item:item.result == "won",reverse=True)
        sort_by_ahead = sorted(sort_by_wins,key=lambda item:item.result == "ahead",reverse=True)
        sort_by_tie = sorted(sort_by_ahead,key=lambda item:item.number_of_tiebreaks,reverse=True)
        return sort_by_tie

    def __sort_tiebreak0(self,details):
        sort_by_name = sorted(details,key=lambda item:item.player_name)
        sort_by_wins = sorted(sort_by_name,key=lambda item:item.result == "won",reverse=True)
        sort_by_ahead = sorted(sort_by_wins,key=lambda item:item.result == "ahead",reverse=True)
        return sort_by_ahead

    def __sort_tiebreak1(self,details):
        sort_by_name = sorted(details,key=lambda item:item.player_name)
        sort_by_difference = sorted(sort_by_name,key=lambda item:item.difference)
        return sort_by_difference

    def __sort_tiebreak2(self,details):
        sort_by_name = sorted(details,key=lambda item:item.player_name)
        sort_by_difference = sorted(sort_by_name,key=lambda item:item.difference)
        return sort_by_difference

    def __sort_tiebreak3(self,details):
        sort_by_name = sorted(details,key=lambda item:item.player_name)
        sort_by_submit_time = sorted(sort_by_name,key=lambda item:item.pick_entry_time)
        move_none_to_end = sorted(sort_by_submit_time,key=lambda item:item != None,reverse=True)
        return move_none_to_end



