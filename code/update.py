from google.appengine.ext import db
from google.appengine.api import memcache
from database import *
from calculator import *
from week_results import *

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

    def get_week_state(self,year,week_number):
        database = Database()
        week_data = database.load_week_data(year,week_number)
        calc = CalculateResults(week_data)
        return calc.get_summary_state_of_all_games()

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

        results = self.assign_rank(results)
        results = self.assign_projected_rank(results)
        results = self.__sort_by_rank(results)

        return results


    def get_overall_results(self,year):
        pass

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




