import webapp2
import logging
from code.update import *
from code.database import *
from handler import *
from utils.utils import *

# Test list
# - bad year
# - different pool states

class OverallResultsPage(Handler):

    def get(self,year_param):
        year = int(year_param)

        database = Database()

        if not(database.is_year_valid(year)):
            self.error(400)
            self.render("bad_year.html",year=year)
            return

        u = Update()
        results = u.get_overall_results(year)

        d = Database()
        pool_state = d.get_pool_state(year)

        weeks_in_year = database.get_week_numbers(year)

        content_params = dict()
        content_params['year'] = year
        content_params['weeks_in_year'] = weeks_in_year
        content_params['pool_state'] = pool_state
        content_params['results'] = results

        self.__render_file = "overall_final_results.html"

        params = dict()
        params['year'] = year
        params['weeks_in_year'] = weeks_in_year
        params['pool_state'] = pool_state
        params['results'] = results
        params['content'] = self.__initial_content(content_params)
        params['sorted_by_overall'] = self.__sort_by_overall(content_params)
        params['sorted_by_overall_reversed'] = self.__sort_by_overall_reversed(content_params)
        params['sorted_by_players'] = self.__sort_by_players(content_params)
        params['sorted_by_players_reversed'] = self.__sort_by_players_reversed(content_params)

        self.render("overall_results.html",**params)

    def __initial_content(self,content_params):
        return self.__sort_by_overall(content_params,escape=False)

    def __sort_by_overall(self,content_params,escape=True):
        sorted_by_overall = sorted(content_params['results'],key=lambda result:result.rank)

        params = dict()
        params['year'] = content_params['year']
        params['weeks_in_year'] = content_params['weeks_in_year']
        params['pool_state'] = content_params['pool_state']
        params['results'] = sorted_by_overall

        self.__highlight_column('overall',params)

        content = self.render_str(self.__render_file,**params)

        if escape:
            html_str = escape_string(content)
            return compress_html(html_str)
        return content

    def __sort_by_overall_reversed(self,content_params):
        sorted_by_overall_reversed = sorted(content_params['results'],key=lambda result:result.rank,reverse=True)

        params = dict()
        params['year'] = content_params['year']
        params['weeks_in_year'] = content_params['weeks_in_year']
        params['pool_state'] = content_params['pool_state']
        params['results'] = sorted_by_overall_reversed

        self.__highlight_column('overall',params)

        content = self.render_str(self.__render_file,**params)
        html_str = escape_string(content)
        return compress_html(html_str)


    def __sort_by_players(self,content_params):
        sorted_by_players = sorted(content_params['results'],key=lambda result:result.player_name)

        params = dict()
        params['year'] = content_params['year']
        params['weeks_in_year'] = content_params['weeks_in_year']
        params['pool_state'] = content_params['pool_state']
        params['results'] = sorted_by_players

        self.__highlight_no_columns(params)

        content = self.render_str(self.__render_file,**params)
        html_str = escape_string(content)
        return compress_html(html_str)


    def __sort_by_players_reversed(self,content_params):
        sorted_by_players_reversed = sorted(content_params['results'],key=lambda result:result.player_name,reverse=True)

        params = dict()
        params['year'] = content_params['year']
        params['weeks_in_year'] = content_params['weeks_in_year']
        params['pool_state'] = content_params['pool_state']
        params['results'] = sorted_by_players_reversed

        self.__highlight_no_columns(params)

        content = self.render_str(self.__render_file,**params)
        html_str = escape_string(content)
        return compress_html(html_str)

    def __highlight_no_columns(self,params):
        return self.__highlight_column(None,params)

    def __highlight_column(self,name,params):
        if name == "overall":
            params['overall_id'] = "highlight-content"
        else:
            params['overall_id'] = "content"
