import webapp2
import logging
from code.update import *
from code.database import *
from handler import *

# TODO: JSON tests
# - bad year, week
# - before pick deadline
# - after pick deadline

class PlayerResultsJson(Handler):

    def __convert_to_format_required_for_json(self,summary,results):
        results_list = []
        for result in results:
            results_list.append(result.get_dict())

        player_results = dict()
        player_results['summary'] = summary.get_dict()
        player_results['player_results'] = results_list
        return player_results

    def __hide_player_results(self,player_id,year,week_number):
        if self.__player_logged_in(player_id):
            return False

        database = Database()
        return database.before_pick_deadline(year,week_number)

    def __player_logged_in(self,player_id):
        # TODO:  check login credentials
        return False


    def get(self,year_param,week_number_param,player_id_param):

        year = int(year_param)
        week_number = int(week_number_param)
        player_id = int(player_id_param)

        if self.__hide_player_results(player_id,year,week_number):
            self.error(400)
            self.render_json({'error':'pick deadline has not passed'})
            return

        u = Update()
        summary,results = u.get_player_results(player_id,year,week_number)
        results_json = self.__convert_to_format_required_for_json(summary,results)
        self.render_json(results_json)
