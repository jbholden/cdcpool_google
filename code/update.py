from google.appengine.ext import db
from google.appengine.api import memcache
from database import *
from calculator import *
from code.week_results import *
from code.player_results import *
from code.overall_results import *

# TODO:  create test to simulate start of a pool
#        - players signed up for year
#        - week 1 created with games
#        - no week 1 picks yet

class Update:

    def update_years_and_week_numbers(self):
        database = Database()
        years = database.load_weeks_and_years(update=True)

    def update_all_week_results(self):
        # TODO:  tests
        self.update_years_and_week_numbers()
        database = Database()
        years = database.get_years()
        for year in years:
            self.update_all_week_results_in_a_year(year)

    def update_all_overall_results(self):
        pass

    def update_all_week_results_in_a_year(self,year):
        # TODO:  tests
        database = Database()
        weeks = database.get_week_numbers(year)
        for week_number in weeks:
            results = self.update_week_results(year,week_number)

    # save data to the database
    def update_week_results(self,year,week_number):
        # TODO:  tests
        results = self.get_week_results(year,week_number,update=True)

    def update_overall_results(self,year):
        pass

    def update_player_results(self,year,week_number):
        # TODO:  tests
        database = Database()
        players = database.load_players(year)
        for player_key in players:
            player_id = players[player_key].key().id()
            summary,results = self.get_player_results(player_id,year,week_number,update=True)

    def update_players(self,year):
        # TODO:  tests
        database = Database()
        players = database.load_players(year,update=True)

    def get_week_results(self,year,week_number,update=False):
        key = "week_results_%d_%d" % (year,week_number)
        results = memcache.get(key)
        if update or not(results):
            results = self.__calculate_week_results(year,week_number)
            memcache.set(key,results)
        return results

    def delete_week_results_from_memcache(self,year,week_number):
        key = "week_results_%d_%d" % (year,week_number)
        memcache.delete(key)

    def delete_player_results_from_memcache(self,player_id,year,week_number):
        key = "player_results_%d_%d_%d" % (player_id,year,week_number)
        memcache.delete(key)

    def get_week_state(self,year,week_number):
        database = Database()
        week_data = database.load_week_data(year,week_number)
        calc = CalculateResults(week_data)
        return calc.get_summary_state_of_all_games()

    def get_player_results(self,player_id,year,week_number,update=False):
        key = "player_results_%d_%d_%d" % (player_id,year,week_number)
        player_results = memcache.get(key)
        if update or not(player_results):
            player_results = self.__calculate_player_results(player_id,year,week_number)
            memcache.set(key,player_results)
        summary = player_results[0]  # redundant but makes code clearer
        results = player_results[1]  # redundant but makes code clearer
        return summary,results

    def __setup_overall_results(self,database,year,update=False):
        players = database.load_players(year,update)
        results = dict()
        for player in players.values():
            result = OverallResults()
            result.rank = 1
            result.projected_rank = 1
            result.player_id = player.key().id() 
            result.player_name = player.name
            result.overall = 0
            result.projected = 0
            result.possible = 0
            result.week_points = []
            result.last_week_projected = 0
            result.last_week_possible = 0
            results[result.player_id] = result
        return results

    # TODO:  highlight overall weekly winner somehow
    def __update_overall_results(self,player_id,overall_results,week_result,last_week):
        overall_results[player_id].overall += week_result.wins
        overall_results[player_id].projected += week_result.projected_wins
        overall_results[player_id].possible += week_result.possible_wins
        overall_results[player_id].week_points += [ week_result.wins ]

        if last_week:
            overall_results[player_id].last_week_projected = week_result.projected_wins
            overall_results[player_id].last_week_possible = week_result.possible_wins

    def __update_overall_results_unplayed_weeks(self,overall_results,last_week_number):
        number_of_weeks = 13
        number_of_points_per_week = 10

        assert last_week_number <= number_of_weeks, "Unexpected last week number %d, only expected %d weeks" % (last_week_number,number_of_weeks)

        number_of_unplayed_weeks = number_of_weeks - last_week_number
        number_of_points_left = number_of_points_per_week * number_of_unplayed_weeks
        for player_id in overall_results:
            overall_results[player_id].projected += number_of_points_left
            overall_results[player_id].possible += number_of_points_left

    def __update_overall_results_win_pct(self,overall_results,last_week_number):
        number_of_points_per_week = 10
        number_of_total_points_so_far = last_week_number * number_of_points_per_week

        for player_id in overall_results:
            if overall_results[player_id].overall == 0:
                win_pct = 0.0
            else:
                win_pct = float(overall_results[player_id].overall) / float(number_of_total_points_so_far)

            overall_results[player_id].win_pct = "%0.3f" % (win_pct)

    def __calculate_overall_results(self,year,update="none"):
        if update == "all":
            update_players = True
            update_week_numbers = True
            update_all_week_results = True
            update_last_week_results = True
        elif update == "all_results":
            update_players = False
            update_week_numbers = False
            update_all_week_results = True
            update_last_week_results = True
        elif update == "last_week_results":
            update_players = False
            update_week_numbers = False
            update_all_week_results = False
            update_last_week_results = True
        elif update == "none":
            update_players = False
            update_week_numbers = False
            update_all_week_results = False
            update_last_week_results = False
        else:
            raise AssertionError,"Invalid update value %s" % (update)

        database = Database()
        overall_results = self.__setup_overall_results(database,year,update=update_players)

        week_numbers = database.get_week_numbers(year,update=update_week_numbers)
        last_week_number = week_numbers[-1]

        for week_number in week_numbers:
            last_week = week_number == last_week_number
            update_week_results = update_all_week_results or (update_last_week_results and last_week)
            week_results = self.get_week_results(year,week_number,update=update_week_results)
            for week_result in week_results:
                self.__update_overall_results(week_result.player_id,overall_results,week_result,last_week)

        self.__update_overall_results_unplayed_weeks(overall_results,last_week_number)
        self.__update_overall_results_win_pct(overall_results,last_week_number)

        overall_results = self.__convert_overall_results_to_list(overall_results)
        overall_results = self.assign_overall_rank(overall_results)
        overall_results = self.assign_overall_projected_rank(overall_results)
        overall_results = self.__sort_by_rank(overall_results)

        return overall_results


    def __calculate_week_results(self,year,week_number):
        database = Database()
        week_data = database.load_week_data(year,week_number)

        calc = CalculateResults(week_data)

        results = []
        for player_key in week_data.players:
            player_results = WeekResults()
            player_results.rank = 1
            player_results.projected_rank = 1
            player_results.player_id = week_data.players[player_key].key().id()
            player_results.player_name = week_data.players[player_key].name
            player_results.wins = calc.get_number_of_wins(player_key)
            player_results.losses = calc.get_number_of_losses(player_key)
            player_results.win_pct = calc.get_win_percent_string(player_key)
            player_results.projected_wins = calc.get_number_of_projected_wins(player_key)
            player_results.possible_wins = calc.get_number_of_possible_wins(player_key)
            player_results.winner = None

            results.append(player_results)

        if len(results) > 0:
            results = self.assign_rank(results)
            results = self.assign_projected_rank(results)
            results = self.__sort_by_rank(results)

        return results


    def __calculate_player_results(self,player_id,year,week_number):
        player_key = str(db.Key.from_path('Player',player_id))

        database = Database()
        week_data = database.load_week_data(year,week_number)

        calc = CalculateResults(week_data)
        summary = self.__calculate_player_summary(player_id,player_key,calc,week_data)
        game_results = self.__calculate_player_game_results_sorted_by_game_number(player_key,calc,week_data)

        return summary,game_results


    def __calculate_player_summary(self,player_id,player_key,calc,week_data):
        summary = PlayerSummary()
        summary.player_id = player_id
        summary.player_name = week_data.get_player(player_key).name
        summary.wins = calc.get_number_of_wins(player_key)
        summary.losses = calc.get_number_of_losses(player_key)
        summary.win_pct = calc.get_win_percent_string(player_key)
        summary.possible_wins = calc.get_number_of_possible_wins(player_key)
        summary.projected_wins = calc.get_number_of_projected_wins(player_key)
        summary.week_state = calc.get_summary_state_of_all_games()
        return summary


    def __calculate_player_game_results_sorted_by_game_number(self,player_key,calc,week_data):
        number_of_games = len(week_data.games)
        game_results = [None]*number_of_games
        for game_key in week_data.games:
            game = week_data.get_game(game_key)
            result = self.__calculate_player_game_result(player_key,game_key,game,calc,week_data)
            game_results[game.number-1] = result
        return game_results


    def __calculate_player_game_result(self,player_key,game_key,game,calc,week_data):
        result = PlayerResult()
        result.player_pick = calc.get_team_name_player_picked_to_win(player_key,game_key)
        result.result = calc.get_game_result_string(player_key,game_key)
        result.team1 = week_data.get_team1_name(game_key)
        result.team2 = week_data.get_team2_name(game_key)
        result.game_state = game.state
        result.favored = calc.get_favored_team_name(game_key)
        result.favored_spread = game.spread
        result.game_date = game.date

        if game.state == "final":
            result.team1_score = game.team1_score
            result.team2_score = game.team2_score
            result.winning_team = calc.get_game_winner_team_name(game_key)
            result.game_spread = calc.get_game_score_spread(game_key)
        elif game.state == "in_progress":
            result.team1_score = game.team1_score
            result.team2_score = game.team2_score
            result.winning_team = calc.get_team_name_winning_game(game_key)
            result.game_spread = calc.get_game_score_spread(game_key)
            result.game_quarter = game.quarter
            result.game_time_left = game.time_left
        elif game.state == "not_started":
            result.team1_score = ''
            result.team2_score = ''
        else:
            raise AssertionError,"Game state %s is not valid" % (game.state)

        return result

    def get_overall_results(self,year,update="none"):
        key = "overall_results_%d" % (year)
        results = memcache.get(key)
        if update != "none" or not(results):
            results = self.__calculate_overall_results(year,update)
            memcache.set(key,results)
        return results

    def __sort_by_rank(self,results):
        return sorted(results,key=lambda result:result.rank)

    def assign_rank(self,results,winner=None):
        # sort by losses first so that people with more losses get a lower rank
        # this is the case where a player did not enter any picks for a week
        # that player would have 10 losses before any games were started, and therefore
        # should be ranked lower
        sorted_by_losses = sorted(results,key=lambda result:result.losses)
        sorted_results = sorted(sorted_by_losses,key=lambda result:result.wins,reverse=True)

        assigned_results = []

        if winner:
            self.__move_winner_to_top_of_results(sorted_results,winner)
            self.__winner_sanity_check(sorted_results)
            next_rank = 2   # no ties for first place
        else:
            next_rank = 1   # there can be ties for first place

        wins = sorted_results[0].wins
        losses = sorted_results[0].losses

        for i,player_result in enumerate(sorted_results):

            first_place = i == 0
            second_place = i == 1

            if first_place:
                player_result.rank = 1
                assigned_results.append(player_result)
                continue

            if second_place and winner:
                player_result.rank = 2
                wins = player_result.wins
                losses = player_result.losses
            else:
                record_changed = player_result.wins != wins or player_result.losses != losses

                if record_changed:
                    next_rank = i+1
                    player_result.rank = next_rank
                    wins = player_result.wins
                    losses = player_result.losses
                else:
                    player_result.rank = next_rank

            assigned_results.append(player_result)

        return assigned_results



    def assign_projected_rank(self,results,projected_winner=None):
        sorted_results = sorted(results,key=lambda result:result.projected_wins,reverse=True)

        assigned_results = []

        if projected_winner:
            self.__move_winner_to_top_of_results(sorted_results,projected_winner)
            self.__projected_winner_sanity_check(sorted_results)
            next_rank = 2   # no ties for first place
        else:
            next_rank = 1   # there can be ties for first place

        projected_wins = sorted_results[0].projected_wins

        for i,player_result in enumerate(sorted_results):

            first_place = i == 0
            second_place = i == 1

            if first_place:
                player_result.projected_rank = 1
                assigned_results.append(player_result)
                continue

            if second_place and projected_winner:
                player_result.projected_rank = 2
                projected_wins = player_result.projected_wins
            else:
                wins_changed = player_result.projected_wins != projected_wins

                if wins_changed:
                    next_rank = i+1
                    player_result.projected_rank = next_rank
                    projected_wins = player_result.projected_wins
                else:
                    player_result.projected_rank = next_rank

            assigned_results.append(player_result)

        return assigned_results

    def assign_overall_rank(self,results):
        sorted_results = sorted(results,key=lambda result:result.overall,reverse=True)

        assigned_results = []
        next_rank = 1   

        overall = sorted_results[0].overall

        for i,player_result in enumerate(sorted_results):

            overall_changed = player_result.overall != overall

            if overall_changed:
                next_rank = i+1
                player_result.rank = next_rank
                overall = player_result.overall
            else:
                player_result.rank = next_rank

            assigned_results.append(player_result)

        return assigned_results


    def assign_overall_projected_rank(self,results):
        sorted_results = sorted(results,key=lambda result:result.projected,reverse=True)

        assigned_results = []
        next_rank = 1   

        projected = sorted_results[0].projected

        for i,player_result in enumerate(sorted_results):

            projected_changed = player_result.projected != projected

            if projected_changed:
                next_rank = i+1
                player_result.projected_rank = next_rank
                projected = player_result.projected
            else:
                player_result.projected_rank = next_rank

            assigned_results.append(player_result)

        return assigned_results


    def __move_winner_to_top_of_results(self,results,winner):
        winner_index = None
        for i,player in enumerate(results):
            if player.player_key == winner:
                winner_index = i
        assert winner_index != None,"Could not find the winning player in the results"
        results.insert(0,results.pop(winner_index))

    def __winner_sanity_check(self,results):
        # the winner should have the best record or tied for the best record
        assert len(results) > 2, "Expected more than 1 player in the results"

        winner = results[0]
        next_best = results[1]

        assert winner.wins >= next_best.wins,"Winner had fewer wins than another (%d vs. %d)" % (winner.wins,next_best.wins)
        assert winner.losses <= next_best.losses,"Winner had more losses than another (%d vs. %d)" % (winner.losses,next_best.losses)

    def __projected_winner_sanity_check(self,results):
        # the winner should have the best record or tied for the best record
        assert len(results) > 2, "Expected more than 1 player in the results"

        winner = results[0]
        next_best = results[1]

        assert winner.projected_wins >= next_best.projected_wins,"Projected winner had fewer wins than another (%d vs. %d)" % (winner.projected_wins,next_best.projected_wins)

    def __convert_overall_results_to_list(self,overall_results_dict):
        return overall_results_dict.values()



