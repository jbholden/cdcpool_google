from week_winner import *
from database import *
from calculator import *

class Tiebreak:

    def __init__(self,year,week_number):
        self.__winners = WeekWinner(year,week_number)
        self.__week_data = database.load_week_data(year,week_number)
        self.__calc = Calculator(self.__week_data)

        self.__calculate_tiebreaker0_details()
        self.__calculate_tiebreaker1_details()
        self.__calculate_tiebreaker2_details()
        self.__calculate_tiebreaker3_details()

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

            if winner_data.featured_game.state == "not_started":
                d.result = ""
                d.featured_game_winner = ""
            elif winner_data.featured_game.state == "in_progress":
                d.result = "ahead"
                d.featured_game_winner = self.__calc.get_team_name_winning_pool_game(featured_game_key)
            elif winner_data.featured_game.state == "final":
                d.result = "won"
                d.featured_game_winner = self.__calc.get_pool_game_winner_team_name(featured_game_key)
            else:
                raise AssertionError,"Bad state value %s" % (winner_data.featured_game.state)

            details.append(d)

        players = self.__winners.get_players_that_lost_tiebreak_0()
        for player_key in players:
            d = Tiebreak0Data()
            d.player_key = player_key
            d.player_name = self.__get_player_name(player_key)
            d.player_pick = self.__calc.get_team_name_player_picked_to_win(player_key,featured_game_key)

            if winner_data.featured_game.state == "not_started":
                d.result = ""
                d.featured_game_winner = ""
            elif winner_data.featured_game.state == "in_progress":
                d.result = "behind"
                d.featured_game_winner = self.__calc.get_team_name_winning_pool_game(featured_game_key)
            elif winner_data.featured_game.state == "final":
                d.result = "lost"
                d.featured_game_winner = self.__calc.get_pool_game_winner_team_name(featured_game_key)
            else:
                raise AssertionError,"Bad state value %s" % (winner_data.featured_game.state)
            details.append(d)

        self.__tiebreak0_details = details

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

            if winner_data.featured_game.state == "not_started":
                d.result = ""
            elif winner_data.featured_game.state == "in_progress":
                d.result = "ahead"
            elif winner_data.featured_game.state == "final":
                d.result = "won"
            else:
                raise AssertionError,"Bad state value %s" % (winner_data.featured_game.state)

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

            if winner_data.featured_game.state == "not_started":
                d.result = ""
            elif winner_data.featured_game.state == "in_progress":
                d.result = "behind"
            elif winner_data.featured_game.state == "final":
                d.result = "lost"
            else:
                raise AssertionError,"Bad state value %s" % (winner_data.featured_game.state)

            pick = self.__calc.get_player_pick_for_game(player_key,featured_game_key)

            d.team1_score = pick.team1_score
            d.team2_score = pick.team2_score
            d.pick_spread = pick.team1_score - pick.team2_score
            d.difference = abs(d.pick_spread - summary.result_spread)

            details.append(d)

        self.__tiebreak1_summary = summary
        self.__tiebreak1_details = details

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

            if winner_data.featured_game.state == "not_started":
                d.result = ""
            elif winner_data.featured_game.state == "in_progress":
                d.result = "ahead"
            elif winner_data.featured_game.state == "final":
                d.result = "won"
            else:
                raise AssertionError,"Bad state value %s" % (winner_data.featured_game.state)

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

            if winner_data.featured_game.state == "not_started":
                d.result = ""
            elif winner_data.featured_game.state == "in_progress":
                d.result = "behind"
            elif winner_data.featured_game.state == "final":
                d.result = "lost"
            else:
                raise AssertionError,"Bad state value %s" % (winner_data.featured_game.state)

            pick = self.__calc.get_player_pick_for_game(player_key,featured_game_key)

            d.team1_score = pick.team1_score
            d.team2_score = pick.team2_score
            d.pick_total = pick.team1_score + pick.team2_score
            d.difference = abs(summary.result_total - d.pick_total)

            details.append(d)

        self.__tiebreak2_summary = summary
        self.__tiebreak2_details = details

    def __calculate_tiebreaker3_details(self):
        pass

    def __get_player_name(self,player_key):
        return self.__week_data.players[player_key].name
