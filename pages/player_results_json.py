import webapp2
import logging
from code.update import *
from handler import *

class PlayerResultsJson(Handler):

    def __convert_to_format_required_for_json(self,summary,results):
        results_list = []
        for result in results:
            results_list.append(result.get_dict())

        player_results = dict()
        player_results['summary'] = summary.get_dict()
        player_results['player_results'] = results_list
        return player_results

    def get(self,year_param,week_number_param,player_id_param):

        year = int(year_param)
        week_number = int(week_number_param)
        player_id = int(player_id_param)

        u = Update()
        summary,results = u.get_player_results(player_id,year,week_number)
        results_json = self.__convert_to_format_required_for_json(summary,results)
        self.render_json(results_json)
