import webapp2
import logging
from code.update import *
from handler import *

# TODO: JSON tests
# - bad year
# - different pool state (invalid, not started, ...)

class OverallResultsJson(Handler):

    def __convert_to_format_required_for_json(self,pool_state,results):
        result_list = []
        for result in results:
            result_list.append(result.get_dict())

        overall_results = dict()
        overall_results['pool_state'] = pool_state
        overall_results['overall_results'] = result_list
        return overall_results


    def get(self,year_param):

        year = int(year_param)

        u = Update()
        results = u.get_overall_results(year)

        d = Database()
        pool_state = d.get_pool_state(year)

        results_json = self.__convert_to_format_required_for_json(pool_state,results)
        self.render_json(results_json)
