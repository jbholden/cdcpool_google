# TODO:  decide if want to use game key or game object (currently use key)
# TODO:  consolidate winner/team ahead functions?
import logging

class CalculateResults:

    def __init__(self,data):
        self.__data = data

    # these are leftover from the node.js calculator file
    # if needed, then can implement later
    def get_game_state(self):
       raise AssertionError,"Not implemented"
    def get_game_pick(self):
       raise AssertionError,"Not implemented"
    def get_player_name(self,player_key):
       raise AssertionError,"Not implemented"
    def get_game(self,game_key):
       raise AssertionError,"Not implemented"
    def get_team_name(self,team_key):
       raise AssertionError,"Not implemented"

    def get_team_player_picked_to_win(self,player_key,game_key):
        picks = self.__data.get_player_picks(player_key)
        pick = self.__find_player_pick_for_game(picks,game_key)
        assert pick != None,"Could not find a pick that matches the passed in game"
        return pick.winner

    def get_team_name_player_picked_to_win(self,player_key,game_key):
        assert self.__game_key_valid(game_key),"Game key is not valid"

        if self.player_did_not_pick(player_key,game_key):
            return ""

        winner = self.get_team_player_picked_to_win(player_key,game_key)
        if winner == "team1":
            return self.__data.get_team1_name(game_key)
        elif winner == "team2":
            return self.__data.get_team2_name(game_key)
        raise AssertionError,"Error determining winner name (winner=%s)" % (winner)

    def is_team1_winning_pool(self,game_key):
        game = self.__data.get_game(game_key)
        score_diff = game.team2_score-game.team1_score
        if game.favored == "team2":
            spread = game.spread
        elif game.favored == "team1":
            spread = -game.spread
        else:
            raise AssertionError,"game.favored has an invalid value"
        return score_diff < spread


    def is_team2_winning_pool(self,game_key):
        game = self.__data.get_game(game_key)
        score_diff = game.team2_score-game.team1_score
        if game.favored == "team2":
            spread = game.spread
        elif game.favored == "team1":
            spread = -game.spread
        else:
            raise AssertionError,"game.favored has an invalid value"
        return score_diff > spread


    def get_pool_game_winner(self,game_key):
        game = self.__data.get_game(game_key)

        if game.state == "final":
            if self.is_team1_winning_pool(game_key):
                return "team1"
            elif self.is_team2_winning_pool(game_key):
                return "team2"
            else:
                raise AssertionError,"Either team1 or team2 should be ahead"
        else:
            return None

    def get_pool_game_winner_team_name(self,game_key):
        winner = self.get_pool_game_winner(game_key)
        game_not_final = not(winner)
        if game_not_final:
            return None

        if winner == "team1":
            return self.__data.get_team1_name(game_key)
        elif winner == "team2":
            return self.__data.get_team2_name(game_key)
        else:
            raise AssertionError,"Either team1 or team2 should have won"

    def get_game_winner(self,game_key):
        game = self.__data.get_game(game_key)

        if game.state == "final":
            assert game.team1_score != game.team2_score,"Game cannot end in a tie (%s to %s)" % (game.team1_score,game.team2_score)

            if game.team1_score > game.team2_score:
                return "team1"
            else:
                return "team2"
        else:
            return None


    def get_game_winner_team_name(self,game_key):
        winner = self.get_game_winner(game_key)
        game_not_final = not(winner)
        if game_not_final:
            return None

        if winner == "team1":
            return self.__data.get_team1_name(game_key)
        elif winner == "team2":
            return self.__data.get_team2_name(game_key)
        else:
            raise AssertionError,"Either team1 or team2 should have won"

    def get_team_winning_pool_game(self,game_key):
        game = self.__data.get_game(game_key)

        if game.state == "in_progress":
            if self.is_team1_winning_pool(game_key):
                return "team1"
            elif self.is_team2_winning_pool(game_key):
                return "team2"
            else:
                raise AssertionError,"Either team1 or team2 should be ahead"
        else:
            return None

    def get_team_name_winning_pool_game(self,game_key):
        team = self.get_team_winning_pool_game(game_key)
        game_not_in_progress = not(team)
        if game_not_in_progress:
            return None

        if team == "team1":
            return self.__data.get_team1_name(game_key)
        elif team == "team2":
            return self.__data.get_team2_name(game_key)
        else:
            raise AssertionError,"Either team1 or team2 should be ahead"

    def get_team_winning_game(self,game_key):
        game = self.__data.get_game(game_key)

        if game.state == "in_progress":
            if game.team1_score > game.team2_score:
                return "team1"
            elif game.team1_score == game.team2_score:
                return "tied"
            else:
                return "team2"
        else:
            return None


    def get_team_name_winning_game(self,game_key):
        team = self.get_team_winning_game(game_key)
        game_not_in_progress = not(team)
        if game_not_in_progress:
            return None

        if team == "team1":
            return self.__data.get_team1_name(game_key)
        elif team == "team2":
            return self.__data.get_team2_name(game_key)
        elif team == "tied":
            return "tied"
        else:
            raise AssertionError,"Invalid team value"

    def player_did_not_pick(self,player_key,game_key):
        assert self.__game_key_valid(game_key),"Game key is not valid"
        picks = self.__data.get_player_picks(player_key)
        pick = self.__find_player_pick_for_game(picks,game_key)
        if pick == None:
            return True

        return pick.winner == None


    def did_player_win_game(self,player_key,game_key):
        if self.player_did_not_pick(player_key,game_key):
            return False

        game_winner = self.get_pool_game_winner(game_key)
        if game_winner:
            player_winner = self.get_team_player_picked_to_win(player_key,game_key)
            return player_winner == game_winner
        return False

    def did_player_lose_game(self,player_key,game_key):
        if self.player_did_not_pick(player_key,game_key):
            return True

        game_winner = self.get_pool_game_winner(game_key)
        if game_winner:
            player_winner = self.get_team_player_picked_to_win(player_key,game_key)
            return player_winner != game_winner
        return False

    def get_number_of_wins(self,player_key):
        wins = 0
        for game_key in self.__data.games:
            if self.did_player_win_game(player_key,game_key):
                wins += 1
        return wins

    def __debug_print_game(self,player_key,game_key):
        team1 = self.__data.get_team1_name(game_key)
        team2 = self.__data.get_team2_name(game_key)
        if self.did_player_win_game(player_key,game_key):
            result = "win"
        elif self.did_player_lose_game(player_key,game_key):
            result = "loss"
        else:
            result = "indeterminate"
        print "%s vs. %s: %s" % (team1,team2,result)

    def get_number_of_losses(self,player_key):
        losses = 0
        for game_key in self.__data.games:
            if self.did_player_lose_game(player_key,game_key):
                losses += 1
        return losses

    def is_player_winning_game(self,player_key,game_key):
        game = self.__data.get_game(game_key)
        assert game != None,"invalid game key"

        player = self.__data.get_player(player_key)
        assert player != None,"invalid player key"

        if game.state == "final":
            return False

        if self.player_did_not_pick(player_key,game_key):
            return False

        team_ahead = self.get_team_winning_pool_game(game_key)

        if team_ahead:
            picks = self.__data.get_player_picks(player_key)
            pick = self.__find_player_pick_for_game(picks,game_key)
            assert pick != None, "Could not find pick for player key %s" % (player_key)

            return team_ahead == pick.winner

        return False

    def is_player_losing_game(self,player_key,game_key):
        game = self.__data.get_game(game_key)
        assert game != None,"invalid game key"

        player = self.__data.get_player(player_key)
        assert player != None,"invalid player key"

        if game.state == "final":
            return False

        if self.player_did_not_pick(player_key,game_key):
            return True

        team_ahead = self.get_team_winning_pool_game(game_key)

        if team_ahead:
            picks = self.__data.get_player_picks(player_key)
            pick = self.__find_player_pick_for_game(picks,game_key)
            assert pick != None, "Could not find pick for player key %s" % (player_key)

            return team_ahead != pick.winner

        return False

    def is_player_projected_to_win_game(self,player_key,game_key):
        game = self.__data.get_game(game_key)
        assert game != None,"invalid game key"

        player = self.__data.get_player(player_key)
        assert player != None,"invalid player key"

        if self.player_did_not_pick(player_key,game_key):
            return False

        if game.state == "final":
            return self.did_player_win_game(player_key,game_key)
        elif game.state == "in_progress":
            return self.is_player_winning_game(player_key,game_key)
        elif game.state == "not_started":
            return True
        else:
            raise AssertionError,"invalid game state"

    def is_player_possible_to_win_game(self,player_key,game_key):
        game = self.__data.get_game(game_key)
        assert game != None,"invalid game value"

        if self.player_did_not_pick(player_key,game_key):
            return False

        if game.state == "final":
            return self.did_player_win_game(player_key,game_key)
        elif game.state == "in_progress":
            return True
        elif game.state == "not_started":
            return True
        else:
            raise AssertionError,"invalid game state"


    def get_number_of_projected_wins(self,player_key):
        wins = 0
        for game_key in self.__data.games:
            if self.is_player_projected_to_win_game(player_key,game_key):
                wins += 1
        return wins

    def get_number_of_possible_wins(self,player_key):
        wins = 0
        for game_key in self.__data.games:
            if self.is_player_possible_to_win_game(player_key,game_key):
                wins += 1
        return wins

    def all_games_final(self):
        final_games = 0
        for game in self.__data.games.values():
            if game.state == "final":
                final_games += 1
        return final_games == len(self.__data.games)


    def no_games_started(self):
        not_started = 0
        for game in self.__data.games.values():
            if game.state == "not_started":
                not_started += 1
        return not_started == len(self.__data.games)

    def at_least_one_game_in_progress(self):
        in_progress = 0
        for game in self.__data.games.values():
            if game.state == "in_progress":
                in_progress += 1
        return in_progress > 0

    def get_summary_state_of_all_games(self):
        if self.all_games_final():
            return "final"
        if self.no_games_started():
            return "not_started"
        return "in_progress"

    def get_game_result_string(self,player_key,game_key):
        assert self.__game_key_valid(game_key),"Invalid game key"
        assert self.__player_key_valid(player_key),"Invalid player key"

        if self.did_player_win_game(player_key,game_key):
            return "win"
        if self.did_player_lose_game(player_key,game_key):
            return "loss"
        if self.is_player_winning_game(player_key,game_key):
            return "ahead"
        if self.is_player_losing_game(player_key,game_key):
            return "behind"
        return ""

    def get_favored_team_name(self,game_key):
        game = self.__data.get_game(game_key)
        assert game != None

        if game.favored == "team1":
            return self.__data.get_team1_name(game_key)
        elif game.favored == "team2":
            return self.__data.get_team2_name(game_key)
        raise AssertionError,"invalid favored value"


    def get_game_score_spread(self,game_key):
        game = self.__data.get_game(game_key)
        assert game != None,"invalid game value"
        assert game.state != "not_started","a game that has not started has no spread"
        assert game.team1_score != None,"invalid score value"
        assert game.team2_score != None,"invalid score value"
        return abs(game.team1_score-game.team2_score)
       

    def get_pick_score_spread(self,pick):
        assert pick != None,"invalid pick value"
        assert pick.team1_score != None,"pick team1 score is invalid"
        assert pick.team2_score != None,"pick team2 score is invalid"
        return abs(pick.team1_score-pick.team2_score)

    def get_featured_game(self):
        for game in self.__data.games.values():
            if game.number == 10:
                return game
        raise AssertionError,"did not find a featured game"

    def get_win_percent(self,player_key):
        wins = self.get_number_of_wins(player_key)
        losses = self.get_number_of_losses(player_key)
        num_games = wins+losses

        if num_games == 0:
            return 0.0
        return float(wins) / float(num_games)

    def get_win_percent_string(self,player_key):
        win_pct = self.get_win_percent(player_key)
        return "%0.3f" % (win_pct)

    def get_player_pick_for_game(self,player_key,game_key):
        picks = self.__data.get_player_picks(player_key)
        pick = self.__find_player_pick_for_game(picks,game_key)
        assert pick != None,"Could not find a pick that matches the passed in game"
        return pick

    def get_player_submit_time(self,player_key,week=None):
        picks = self.__data.get_player_picks(player_key)
        latest_time = None
        for pick in picks:
            pick_entry_time = max(pick.created,pick.modified)

            if latest_time == None or pick_entry_time > latest_time:
                latest_time = pick_entry_time

        if self.__submit_time_invalid(week,latest_time):
            return None

        return latest_time

    def __find_player_pick_for_game(self,picks,game_key):
        for pick in picks:
            if pick.game == game_key:
                return pick
        return None

    def __game_key_valid(self,game_key):
        return self.__data.games.get(game_key) != None

    def __player_key_valid(self,player_key):
        player = self.__data.get_player(player_key)
        return player != None

    def __submit_time_invalid(self,week,submit_time):
        if week == None:
            return False

        pick_deadline_not_set = week.lock_picks == None
        if pick_deadline_not_set:
            return True

        picks_entered_after_pick_deadline = submit_time > week.lock_picks
        if picks_entered_after_pick_deadline:
            return True

        #submit_time_in_wrong_year = submit_time.year != week.year
        #if submit_time_in_wrong_year:
            #return True

        return False

