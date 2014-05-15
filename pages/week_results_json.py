import webapp2
import logging
from code.update import *
from handler import *

# TODO: JSON tests
# - bad year, week

class WeekResultsJson(Handler):

    def __convert_to_format_required_for_json(self,results):
        result_list = []
        for result in results:
            result_list.append(result.get_dict())
        return result_list

    def get(self,year_param,week_number_param):

        year = int(year_param)
        week_number = int(week_number_param)

        u = Update()
        results = u.get_week_results(year,week_number)
        results_json = self.__convert_to_format_required_for_json(results)
        self.render_json(results_json)
