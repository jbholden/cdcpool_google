import webapp2
import logging
from code.tiebreak import *
from code.database import *
from handler import *
import string
import re
from utils.utils import *

class TiebreakPage(Handler):

    def get(self,year_param,week_number_param):
        year = int(year_param)
        week_number = int(week_number_param)

        weeks_in_year = self.__get_weeks_in_year(year,week_number)
        if not(weeks_in_year):
            self.error(400)
            self.render("bad_week.html",year=year,week_number=week_number)
            return

        tiebreak = Tiebreak(year,week_number)

        params = dict()
        params['year'] = year
        params['week_number'] = week_number
        params['weeks_in_year'] = weeks_in_year
        params['winner_valid'] = tiebreak.was_able_to_determine_winner()
        params['featured_game_state'] = tiebreak.get_featured_game_state()
        params['summary'] = tiebreak.get_tiebreaker_summary()
        params['tiebreaker0_details'] = tiebreak.get_tiebreaker0_details()
        params['tiebreaker1_details'] = tiebreak.get_tiebreaker1_details()
        params['tiebreaker2_details'] = tiebreak.get_tiebreaker2_details()
        params['tiebreaker3_details'] = tiebreak.get_tiebreaker3_details()
        params['tiebreaker1_summary'] = tiebreak.get_tiebreaker1_summary()
        params['tiebreaker2_summary'] = tiebreak.get_tiebreaker2_summary()
        params['tiebreaker3_summary'] = tiebreak.get_tiebreaker3_summary()
        params['tiebreaker_required'] = params['summary'] != None and len(params['summary']) > 1
        params['tiebreaker0_valid'] = params['tiebreaker0_details'] != None and len(params['tiebreaker0_details']) > 0
        params['tiebreaker1_valid'] = params['tiebreaker1_details'] != None and len(params['tiebreaker1_details']) > 0
        params['tiebreaker2_valid'] = params['tiebreaker2_details'] != None and len(params['tiebreaker2_details']) > 0
        params['tiebreaker3_valid'] = params['tiebreaker3_details'] != None and len(params['tiebreaker3_details']) > 0

        self.render("tiebreak.html",**params)

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

