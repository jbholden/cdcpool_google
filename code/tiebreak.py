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

        return details


    def get_tiebreaker1_details(self):
        pass

    def get_tiebreaker2_details(self):
        pass

    def get_tiebreaker3_details(self):
        pass

    def __calculate_tiebreaker0_details(self):
        pass

    def __calculate_tiebreaker1_details(self):
        pass

    def __calculate_tiebreaker2_details(self):
        pass

    def __calculate_tiebreaker3_details(self):
        pass

    def __get_player_name(self,player_key):
        return self.__week_data.players[player_key].name
