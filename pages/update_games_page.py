import webapp2
import logging
from code.update import *
from code.database import *
from handler import *
import string
import re
from utils.utils import *

class UpdateGamesPage(Handler):

    def get(self,year_param,week_number_param):
        year = int(year_param)
        week_number = int(week_number_param)

        weeks_in_year = self.__get_weeks_in_year(year,week_number)
        if not(weeks_in_year):
            self.error(400)
            self.render("bad_week.html",year=year,week_number=week_number)
            return

        u = Update()

        params = dict()
        params['year'] = year
        params['week_number'] = week_number
        params['weeks_in_year'] = weeks_in_year
        params['games'] = u.get_week_games(year,week_number)

        self.render("update_games.html",**params)

    def __get_game_data(self):
        database = Database()
        week_data = database.load_week_data(year,week_number)
        #week_data.games # game_key:game object

        games = []
        for game in week_data.games.values():
            pass

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
