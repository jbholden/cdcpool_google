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

        d = Database()
        pool_state = d.get_pool_state(year)

        if pool_state == "not_started":
            players = d.load_players(year)
            params = dict()
            params['year'] = year
            params['num_players'] = len(players)
            self.render("overall_not_started.html",**params)
            return

        u = Update()
        results = u.get_overall_results(year)

        weeks_in_year = database.get_week_numbers(year)

        content_params = dict()
        content_params['year'] = year
        content_params['weeks_in_year'] = weeks_in_year
        content_params['pool_state'] = pool_state
        content_params['results'] = results

        if pool_state == "enter_picks":
            self.__render_file = "overall_enter_picks_results.html"
        elif pool_state == "week_not_started":
            self.__render_file = "overall_week_not_started_results.html"
        elif pool_state == "week_in_progress":
            self.__render_file = "overall_week_in_progress_results.html"
        elif pool_state == "week_final":
            self.__render_file = "overall_week_final_results.html"
        elif pool_state == "end_of_year":
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

        if pool_state == "week_not_started":
            params['sorted_by_projected'] = ""
            params['sorted_by_projected_reversed'] = ""
            params['sorted_by_possible'] = self.__sort_by_overall_possible(content_params)
            params['sorted_by_possible_reversed'] = self.__sort_by_overall_possible_reversed(content_params)
        elif pool_state == "week_final":
            params['sorted_by_projected'] = ""
            params['sorted_by_projected_reversed'] = ""
            params['sorted_by_possible'] = self.__sort_by_overall_possible(content_params)
            params['sorted_by_possible_reversed'] = self.__sort_by_overall_possible_reversed(content_params)
        elif pool_state == "week_in_progress":
            params['sorted_by_projected'] = self.__sort_by_overall_projected(content_params)
            params['sorted_by_projected_reversed'] = self.__sort_by_overall_projected_reversed(content_params)
            params['sorted_by_possible'] = self.__sort_by_overall_possible(content_params)
            params['sorted_by_possible_reversed'] = self.__sort_by_overall_possible_reversed(content_params)
        else:
            params['sorted_by_projected'] = ""
            params['sorted_by_projected_reversed'] = ""
            params['sorted_by_possible'] = ""
            params['sorted_by_possible_reversed'] = ""

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

    def __sort_by_overall_projected(self,content_params,escape=True):
        sorted_by_overall_projected = sorted(content_params['results'],key=lambda result:result.projected_rank)

        params = dict()
        params['year'] = content_params['year']
        params['weeks_in_year'] = content_params['weeks_in_year']
        params['pool_state'] = content_params['pool_state']
        params['results'] = sorted_by_overall_projected
        params['rank'] = "projected"

        self.__highlight_column('projected',params)

        content = self.render_str(self.__render_file,**params)

        if escape:
            html_str = escape_string(content)
            return compress_html(html_str)
        return content

    def __sort_by_overall_projected_reversed(self,content_params):
        sorted_by_overall_projected_reversed = sorted(content_params['results'],key=lambda result:result.projected_rank,reverse=True)

        params = dict()
        params['year'] = content_params['year']
        params['weeks_in_year'] = content_params['weeks_in_year']
        params['pool_state'] = content_params['pool_state']
        params['results'] = sorted_by_overall_projected_reversed
        params['rank'] = "projected"

        self.__highlight_column('projected',params)

        content = self.render_str(self.__render_file,**params)
        html_str = escape_string(content)
        return compress_html(html_str)

    def __sort_by_overall_possible(self,content_params,escape=True):
        sorted_by_overall_possible = sorted(content_params['results'],key=lambda result:result.possible,reverse=True)

        params = dict()
        params['year'] = content_params['year']
        params['weeks_in_year'] = content_params['weeks_in_year']
        params['pool_state'] = content_params['pool_state']
        params['results'] = sorted_by_overall_possible

        self.__highlight_column('possible',params)

        content = self.render_str(self.__render_file,**params)

        if escape:
            html_str = escape_string(content)
            return compress_html(html_str)
        return content

    def __sort_by_overall_possible_reversed(self,content_params):
        sorted_by_overall_possible_reversed = sorted(content_params['results'],key=lambda result:result.possible)

        params = dict()
        params['year'] = content_params['year']
        params['weeks_in_year'] = content_params['weeks_in_year']
        params['pool_state'] = content_params['pool_state']
        params['results'] = sorted_by_overall_possible_reversed

        self.__highlight_column('possible',params)

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

        if name == "projected":
            params['projected_id'] = "highlight-content"
        else:
            params['projected_id'] = "content"

        if name == "possible":
            params['possible_id'] = "highlight-content"
        else:
            params['possible_id'] = "content"
