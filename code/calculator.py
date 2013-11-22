# TODO:  decide if want to use game key or game object (currently use key)
# TODO:  consolidate winner/team ahead functions?
import logging

class CalculateResults:

    def __init__(self,week,games,player_picks):
        self.__week = week
        self.__games = games
        self.__picks = player_picks
        self.__players = player_picks.keys()

    def get_game_away_team(self):
       raise AssertionError,"Not implemented"
    def get_game_home_team(self):
       raise AssertionError,"Not implemented"
    def get_game_state(self):
       raise AssertionError,"Not implemented"


    def get_team_player_picked_to_win(self,player_name,game):
        assert game != None, 'Game is not valid'

        picks = self.__picks.get(player_name)
        assert picks != None, "Could not find player %s picks." % (player_name)

        pick = self.__find_player_pick_for_game(picks,game)
        assert pick != None,"Could not find a pick that matches the passed in game"

        return pick.winner


    def get_team_name_player_picked_to_win(self,player_name,game):
        winner = self.get_team_player_picked_to_win(player_name,game)
        if winner == "team1":
            return game.team1.name
        elif winner == "team2":
            return game.team2.name
        raise AssertionError,"Error determining winner name"


    def is_team1_winning_pool(self,game):
        score_diff = game.team2_score-game.team1_score
        if game.favored == "team2":
            spread = game.spread
        elif game.favored == "team1":
            spread = -game.spread
        else:
            raise AssertionError,"game.favored has an invalid value"
        return score_diff < spread


    def is_team2_winning_pool(self,game):
        score_diff = game.team2_score-game.team1_score
        if game.favored == "team2":
            spread = game.spread
        elif game.favored == "team1":
            spread = -game.spread
        else:
            raise AssertionError,"game.favored has an invalid value"
        return score_diff > spread


    def get_pool_game_winner(self,game):
        assert game != None,"Game is not valid"

        if game.state == "final":
            if self.is_team1_winning_pool(game):
                return "team1"
            elif self.is_team2_winning_pool(game):
                return "team2"
            else:
                raise AssertionError,"Either team1 or team2 should be ahead"
        else:
            return None

    def get_pool_game_winner_team_name(self,game):
        winner = self.get_pool_game_winner(game)
        game_not_final = not(winner)
        if game_not_final:
            return None

        if winner == "team1":
            return game.team1.name
        elif winner == "team2":
            return game.team2.name
        else:
            raise AssertionError,"Either team1 or team2 should have won"

    def get_game_winner(self,game):
        assert game != None,"Invalid game value (None)"

        if game.state == "final":
            assert game.team1_score != game.team2_score,"Game cannot end in a tie"

            if game.team1_score > game.team2_score:
                return "team1"
            else:
                return "team2"
        else:
            return None


    def get_game_winner_team_name(self,game):
        winner = self.get_game_winner(game)
        game_not_final = not(winner)
        if game_not_final:
            return None

        if winner == "team1":
            return game.team1.name
        elif winner == "team2":
            return game.team2.name
        else:
            raise AssertionError,"Either team1 or team2 should have won"

    def get_team_winning_pool_game(self,game):
        assert game != None,"Game is not valid"

        if game.state == "in_progress":
            if self.is_team1_winning_pool(game):
                return "team1"
            elif self.is_team2_winning_pool(game):
                return "team2"
            else:
                raise AssertionError,"Either team1 or team2 should be ahead"
        else:
            return None

    def get_team_name_winning_pool_game(self,game):
        team = self.get_team_winning_pool_game(game)
        game_not_in_progress = not(team)
        if game_not_in_progress:
            return None

        if team == "team1":
            return game.team1.name
        elif team == "team2":
            return game.team2.name
        else:
            raise AssertionError,"Either team1 or team2 should be ahead"

    def get_team_winning_game(self,game):
        assert game != None,"Game is not valid"

        if game.state == "in_progress":
            if game.team1_score > game.team2_score:
                return "team1"
            elif game.team1_score == game.team2_score:
                return "tied"
            else:
                return "team2"
        else:
            return None


    def get_team_name_winning_game(self,game):
        team = self.get_team_winning_game(game)
        game_not_in_progress = not(team)
        if game_not_in_progress:
            return None

        if team == "team1":
            return game.team1.name
        elif team == "team2":
            return game.team2.name
        elif team == "tied":
            return "tied"
        else:
            raise AssertionError,"Invalid team value"

    def player_did_not_pick(self,player_name,game):
        assert game != None, 'Game is not valid'

        picks = self.__picks.get(player_name)
        assert picks != None, "Could not find player %s" % (player_name)

        pick = self.__find_player_pick_for_game(picks,game)
        if pick == None:
            return True

        return pick.winner == None

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

    def get_featured_game(self):
       pass

    def get_game(self):
       pass

    def get_game_pick(self):
       pass

    def get_team_name(self):
       pass

    def is_pick_tiebreaker_score_missing(self):
        pass

    def __find_player_pick_for_game(self,picks,game):
        game_key = game.key()
        for pick in picks:
            if pick.game.key() == game_key:
                return pick
        return None

