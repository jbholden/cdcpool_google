# data needed:
# - player pick for each game
# - games to calculate

class CalculateResults:

    def __init__(self,week,games,player_picks):
        self.__week = week
        self.__games = games
        self.__picks = player_picks
        self.__players = player_picks.keys()

    def get_team_player_picked_to_win(self,player_name,game):
        picks = self.__picks.get(player_name)
        assert picks != None
        for pick in picks:
            if pick.game == game:
                return pick.winner
        raise AssertionError, "Could not find game"


    def get_team_name_player_picked_to_win(self,player_name,game):
        winner = self.get_team_player_picked_to_win(player_name,game)
        if winner == "home":
            return game.home_team.name
        elif winner == "away":
            return game.away_team.name
        raise AssertionError,"Error determining winner name"

    def is_home_team_winning_pool(self,game):
        score_diff = game.home_score-game.away_score
        if game.favored == "home":
            spread = game.spread
        elif game.favored == "away":
            spread = -game.spread
        else:
            raise AssertionError,"game.favored has an invalid value"
        return score_diff > spread

    def is_away_team_winning_pool(self):
        score_diff = game.home_score-game.away_score
        if game.favored == "home":
            spread = game.spread
        elif game.favored == "away":
            spread = -game.spread
        else:
            raise AssertionError,"game.favored has an invalid value"
        return score_diff < spread

    def get_pool_game_winner(self):
       pass

    def get_pool_game_winner_team_name(self):
       pass

    def get_game_winner(self):
       pass

    def get_game_winner_team_name(self):
       pass

    def get_game_away_team(self):
       pass

    def get_game_home_team(self):
       pass

    def get_team_winning_pool_game(self):
       pass

    def get_team_name_winning_pool_game(self):
       pass

    def get_team_winning_game(self):
       pass

    def get_team_name_winning_game(self):
       pass

    def get_game_state(self):
       pass

    def did_player_win_game(self):
       pass

    def get_number_of_wins(self):
       pass

    def did_player_lose_game(self):
       pass

    def get_number_of_losses(self):
       pass

    def is_player_winning_game(self):
       pass

    def is_player_losing_game(self):
       pass

    def is_player_projected_to_win_game(self):
       pass

    def is_player_possible_to_win_game(self):
       pass

    def get_number_of_projected_wins(self):
       pass

    def get_number_of_possible_wins(self):
       pass

    def all_games_final(self):
       pass

    def no_games_started(self):
       pass

    def at_least_one_game_in_progress(self):
       pass

    def get_summary_state_of_all_games(self):
       pass

    def get_game_result_string(self):
       pass

    def get_favored_team_name(self):
       pass

    def get_game_score_spread(self):
       pass

    def get_pick_score_spread(self):
       pass

    def player_did_not_pick(self):
       pass

    def get_featured_game(self):
       pass

    def get_game(self):
       pass

    def get_game_pick(self):
       pass

    def get_team_name(self):
       pass
