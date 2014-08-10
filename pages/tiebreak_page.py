import webapp2
import logging
from code.tiebreak import *
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
        params['summary'] = tiebreak.get_tiebreaker_summary()
        params['tiebreaker0_details'] = tiebreak.get_tiebreaker0_details()
        params['tiebreaker1_details'] = tiebreak.get_tiebreaker1_details()
        params['tiebreaker2_details'] = tiebreak.get_tiebreaker2_details()
        params['tiebreaker3_details'] = tiebreak.get_tiebreaker3_details()
        params['tiebreaker1_summary'] = tiebreak.get_tiebreaker1_summary()
        params['tiebreaker2_summary'] = tiebreak.get_tiebreaker2_summary()
        params['tiebreaker3_summary'] = tiebreak.get_tiebreaker3_summary()

        self.render("tiebreak.html",**params)
