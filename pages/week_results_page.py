import webapp2
import logging
from code.update import *
from handler import *
import string
import re
from utils.utils import *

class WeekResultsPage(Handler):

    def get(self,year_param,week_number_param):
        year = int(year_param)
        week_number = int(week_number_param)

        weeks_in_year = self.__get_weeks_in_year(year,week_number)
        if not(weeks_in_year):
            self.error(400)
            self.render("bad_week.html",year=year,week_number=week_number)
            return

        u = Update()
        results = u.get_week_results(year,week_number)
        week_state = u.get_week_state(year,week_number)
        winner_info = u.get_winner_info(year,week_number)

        if week_state == "final":
            self.__render_file = "week_final_results.html"
        elif week_state == "in_progress":
            self.__render_file = "week_in_progress_results.html"
        elif week_state == "not_started":
            self.__render_file = "week_not_started_results.html"
        else:
            raise AssertionError,"Invalid week state %s" % (week_state)

        params = dict()
        params['year'] = year
        params['week_number'] = week_number
        params['weeks_in_year'] = weeks_in_year
        params['content'] = self.__initial_content(results,winner_info)
        params['sorted_by_wins'] = self.__sort_by_wins(results,winner_info)
        params['sorted_by_wins_reversed'] = self.__sort_by_wins_reversed(results,winner_info)
        params['sorted_by_losses'] = self.__sort_by_losses(results,winner_info)
        params['sorted_by_losses_reversed'] = self.__sort_by_losses_reversed(results,winner_info)
        params['sorted_by_players'] = self.__sort_by_players(results,winner_info)
        params['sorted_by_players_reversed'] = self.__sort_by_players_reversed(results,winner_info)

        if week_state == "in_progress":
            params['sorted_by_projected_wins'] = self.__sort_by_projected_wins(results,winner_info)
            params['sorted_by_projected_wins_reversed'] = self.__sort_by_projected_wins_reversed(results,winner_info)
            params['sorted_by_possible_wins'] = self.__sort_by_possible_wins(results,winner_info)
            params['sorted_by_possible_wins_reversed'] = self.__sort_by_possible_wins_reversed(results,winner_info)
        elif week_state == "not_started":
            params['sorted_by_possible_wins'] = self.__sort_by_possible_wins(results,winner_info)
            params['sorted_by_possible_wins_reversed'] = self.__sort_by_possible_wins_reversed(results,winner_info)

        self.render("week_results.html",**params)

    def __initial_content(self,results,winner_info):
        return self.__sort_by_wins(results,winner_info,escape=False)

    def __get_weeks_in_year(self,year,week_number):
        d = Database()
        weeks_and_years = d.load_weeks_and_years()
        if self.__invalid_year_or_week_number(weeks_and_years,year,week_number):
            return None
        weeks_in_year = sorted(weeks_and_years[year])
        return weeks_in_year

    def __invalid_year_or_week_number(self,weeks_and_years,year,week_number):
        weeks_in_year = weeks_and_years.get(year)
        if not(weeks_in_year):
            return True
        return week_number not in weeks_in_year

    def __find_player_id(self,player_id,data):
        for i,item in enumerate(data):
            if player_id == item.player_id:
                return i
        raise AssertionError

    def __move_winner_to_top(self,sorted_data,results):
        for result in results:
            if result.winner != None and result.winner != "":
                index = self.__find_player_id(result.player_id,sorted_data)
                item = sorted_data.pop(index)
                sorted_data.insert(0,item)

    def __move_winner_to_bottom(self,sorted_data,results):
        for result in results:
            if result.winner != None and result.winner != "":
                index = self.__find_player_id(result.player_id,sorted_data)
                item = sorted_data.pop(index)
                sorted_data.append(item)

    def __sort_by_wins(self,results,winner_info,escape=True):
        sorted_by_players = sorted(results,key=lambda result:result.player_name)
        sorted_by_wins = sorted(sorted_by_players,key=lambda result:result.rank)
        self.__move_winner_to_top(sorted_by_wins,results)
        highlight = self.__highlight_column('wins')
        content = self.render_str(self.__render_file,results=sorted_by_wins,winner=winner_info,**highlight)
        if escape:
            html_str = escape_string(content)
            return compress_html(html_str)
        return content

    def __sort_by_wins_reversed(self,results,winner_info):
        sorted_by_players = sorted(results,key=lambda result:result.player_name,reverse=True)
        sorted_by_wins = sorted(sorted_by_players,key=lambda result:result.rank,reverse=True)
        self.__move_winner_to_bottom(sorted_by_wins,results)
        highlight = self.__highlight_column('wins')
        content = self.render_str(self.__render_file,results=sorted_by_wins,winner=winner_info,**highlight)
        html_str = escape_string(content)
        return compress_html(html_str)

    def __sort_by_losses(self,results,winner_info):
        sorted_by_players = sorted(results,key=lambda result:result.player_name,reverse=False)
        sorted_by_losses = sorted(sorted_by_players,key=lambda result:result.rank,reverse=True)
        highlight = self.__highlight_column('losses')
        content = self.render_str(self.__render_file,results=sorted_by_losses,winner=winner_info,**highlight)
        html_str = escape_string(content)
        return compress_html(html_str)

    def __sort_by_losses_reversed(self,results,winner_info):
        sorted_by_players = sorted(results,key=lambda result:result.player_name,reverse=True)
        sorted_by_losses = sorted(sorted_by_players,key=lambda result:result.rank)
        highlight = self.__highlight_column('losses')
        content = self.render_str(self.__render_file,results=sorted_by_losses,winner=winner_info,**highlight)
        html_str = escape_string(content)
        return compress_html(html_str)

    def __sort_by_players(self,results,winner_info):
        sorted_by_players = sorted(results,key=lambda result:result.player_name)
        highlight = self.__highlight_no_columns()
        content = self.render_str(self.__render_file,results=sorted_by_players,winner=winner_info,**highlight)
        html_str = escape_string(content)
        return compress_html(html_str)

    def __sort_by_players_reversed(self,results,winner_info):
        sorted_by_players = sorted(results,key=lambda result:result.player_name,reverse=True)
        highlight = self.__highlight_no_columns()
        content = self.render_str(self.__render_file,results=sorted_by_players,winner=winner_info,**highlight)
        html_str = escape_string(content)
        return compress_html(html_str)

    def __sort_by_projected_wins(self,results,winner_info):
        sorted_by_players = sorted(results,key=lambda result:result.player_name,reverse=False)
        sorted_by_wins = sorted(sorted_by_players,key=lambda result:result.projected_rank)
        highlight = self.__highlight_column('projected_wins')
        content = self.render_str(self.__render_file,results=sorted_by_wins,use_projected_rank=True,winner=winner_info,**highlight)
        html_str = escape_string(content)
        return compress_html(html_str)

    def __sort_by_projected_wins_reversed(self,results,winner_info):
        sorted_by_players = sorted(sorted_by_players,key=lambda result:result.player_name,reverse=True)
        sorted_by_wins = sorted(results,key=lambda result:result.projected_rank,reverse=True)
        highlight = self.__highlight_column('projected_wins')
        content = self.render_str(self.__render_file,results=sorted_by_wins,use_projected_rank=True,winner=winner_info,**highlight)
        html_str = escape_string(content)
        return compress_html(html_str)

    def __sort_by_possible_wins(self,results,winner_info):
        sorted_by_players = sorted(results,key=lambda result:result.player_name,reverse=False)
        sorted_by_wins = sorted(sorted_by_players,key=lambda result:result.possible_wins,reverse=True)
        highlight = self.__highlight_column('possible_wins')
        content = self.render_str(self.__render_file,results=sorted_by_wins,winner=winner_info,**highlight)
        html_str = escape_string(content)
        return compress_html(html_str)

    def __sort_by_possible_wins_reversed(self,results,winner_info):
        sorted_by_players = sorted(results,key=lambda result:result.player_name,reverse=True)
        sorted_by_wins = sorted(sorted_by_players,key=lambda result:result.possible_wins)
        highlight = self.__highlight_column('possible_wins')
        content = self.render_str(self.__render_file,results=sorted_by_wins,winner=winner_info,**highlight)
        html_str = escape_string(content)
        return compress_html(html_str)

    def __highlight_no_columns(self):
        return self.__highlight_column(None)

    def __highlight_column(self,name):
        d = dict()

        if name == "wins":
            d['wins_id'] = "highlight-content"
        else:
            d['wins_id'] = "content"

        if name == "losses":
            d['losses_id'] = "highlight-content"
        else:
            d['losses_id'] = "content"

        if name == "projected_wins":
            d['projected_id'] = "highlight-content"
        else:
            d['projected_id'] = "content"

        if name == "possible_wins":
            d['possible_id'] = "highlight-content"
        else:
            d['possible_id'] = "content"

        return d
