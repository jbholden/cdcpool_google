from google.appengine.ext import db
from google.appengine.api import memcache
import logging
import unittest
import urllib2
import datetime
from pages.player_results_page import *
from code.database import *
from code.update import *
from google.appengine.api import urlfetch
from collections import namedtuple
from utils.utils import *


class GameStatusTestData:
    date = None
    state = None
    timezone = None
    time_left = None
    quarter = None
    top_id = None
    top_status = None
    bottom_id = None
    bottom_status = None


class TestPlayerResults(unittest.TestCase):

    def test_t1_game_status(self):
        self.__t1_game_not_started_status_no_date()
        self.__t1_game_not_started_status_date_est()
        self.__t1_game_not_started_status_date_edt()
        self.__t1_game_not_started_status_date_pst()
        self.__t1_game_not_started_status_date_pdt()
        self.__t1_game_in_progress()
        self.__t1_game_in_progress_quarter()
        self.__t1_game_in_progress_time()
        self.__t1_game_in_progress_quarter_time()

    def __t1_game_not_started_status_no_date(self):
        testdata = GameStatusTestData()
        testdata.date = None
        testdata.timezone = "US/Eastern"
        testdata.state = "not_started"
        testdata.top_id = "status-empty"
        testdata.top_status = ""
        testdata.bottom_id = "status-empty"
        testdata.bottom_status = ""
        self.__test_game_status(testdata)

    def __t1_game_not_started_status_date_est(self):
        testdata = GameStatusTestData()
        testdata.date = self.get_naive_utc_date(datetime.datetime(2010,2,24,19,30),'US/Eastern')
        testdata.state = "not_started"
        testdata.timezone = "US/Eastern"
        testdata.top_id = "game-time"
        testdata.top_status = "Wed 02/24"
        testdata.bottom_id = "game-time"
        testdata.bottom_status = "07:30 PM EST"
        self.__test_game_status(testdata)

    def __t1_game_not_started_status_date_edt(self):
        testdata = GameStatusTestData()
        testdata.date = self.get_naive_utc_date(datetime.datetime(2014,8,24,19,30),'US/Eastern')
        testdata.state = "not_started"
        testdata.timezone = "US/Eastern"
        testdata.top_id = "game-time"
        testdata.top_status = "Sun 08/24"
        testdata.bottom_id = "game-time"
        testdata.bottom_status = "07:30 PM EDT"
        self.__test_game_status(testdata)

    def __t1_game_not_started_status_date_pst(self):
        testdata = GameStatusTestData()
        testdata.date = self.get_naive_utc_date(datetime.datetime(2010,2,24,19,30),'US/Eastern')
        testdata.state = "not_started"
        testdata.timezone = "US/Pacific"
        testdata.top_id = "game-time"
        testdata.top_status = "Wed 02/24"
        testdata.bottom_id = "game-time"
        testdata.bottom_status = "04:30 PM PST"
        self.__test_game_status(testdata)

    def __t1_game_not_started_status_date_pdt(self):
        testdata = GameStatusTestData()
        testdata.date = self.get_naive_utc_date(datetime.datetime(2014,8,24,19,30),'US/Eastern')
        testdata.state = "not_started"
        testdata.timezone = "US/Pacific"
        testdata.top_id = "game-time"
        testdata.top_status = "Sun 08/24"
        testdata.bottom_id = "game-time"
        testdata.bottom_status = "04:30 PM PDT"
        self.__test_game_status(testdata)

    def __t1_game_in_progress_quarter_time(self):
        testdata = GameStatusTestData()
        testdata.date = self.get_naive_utc_date(datetime.datetime(2014,8,24,19,30),'US/Eastern')
        testdata.state = "in_progress"
        testdata.timezone = "US/Eastern"
        testdata.time_left = "15:00"
        testdata.quarter = "3rd"
        testdata.top_id = "game-quarter"
        testdata.top_status = "3rd"
        testdata.bottom_id = "game-time-in-progress"
        testdata.bottom_status = "15:00"
        self.__test_game_status(testdata)

    def __t1_game_in_progress_quarter(self):
        testdata = GameStatusTestData()
        testdata.date = self.get_naive_utc_date(datetime.datetime(2014,8,24,19,30),'US/Eastern')
        testdata.state = "in_progress"
        testdata.timezone = "US/Eastern"
        testdata.time_left = ""
        testdata.quarter = "Halftime"
        testdata.top_id = "status-empty"
        testdata.top_status = ""
        testdata.bottom_id = "game-quarter"
        testdata.bottom_status = "Halftime"
        self.__test_game_status(testdata)

    def __t1_game_in_progress_time(self):
        testdata = GameStatusTestData()
        testdata.date = self.get_naive_utc_date(datetime.datetime(2014,8,24,19,30),'US/Eastern')
        testdata.state = "in_progress"
        testdata.timezone = "US/Eastern"
        testdata.time_left = "3:25"
        testdata.quarter = ""
        testdata.top_id = "status-empty"
        testdata.top_status = ""
        testdata.bottom_id = "game-time-in-progress"
        testdata.bottom_status = "3:25"
        self.__test_game_status(testdata)

    def __t1_game_in_progress(self):
        testdata = GameStatusTestData()
        testdata.date = self.get_naive_utc_date(datetime.datetime(2014,8,24,19,30),'US/Eastern')
        testdata.state = "in_progress"
        testdata.timezone = "US/Eastern"
        testdata.time_left = ""
        testdata.quarter = ""
        testdata.top_id = "status-empty"
        testdata.top_status = ""
        testdata.bottom_id = "game-in-progress"
        testdata.bottom_status = "in progress"
        self.__test_game_status(testdata)

    def __t1_game_final(self):
        testdata = GameStatusTestData()
        testdata.date = self.get_naive_utc_date(datetime.datetime(2014,8,24,19,30),'US/Eastern')
        testdata.state = "final"
        testdata.timezone = "US/Eastern"
        testdata.time_left = ""
        testdata.quarter = ""
        testdata.top_id = "status-empty"
        testdata.top_status = ""
        testdata.bottom_id = "game-final"
        testdata.bottom_status = "final"
        self.__test_game_status(testdata)

    def get_naive_utc_date(self,local_date,timezone): 
        utc_date = get_datetime_in_utc(local_date,timezone)
        return datetime.datetime(utc_date.year,utc_date.month,utc_date.day,utc_date.hour,utc_date.minute)

    def __test_game_status(self,test_data):
        page = PlayerResultsPage()
        result = PlayerResult()
        result.game_date = test_data.date
        result.game_state = test_data.state
        result.game_time_left = test_data.time_left
        result.game_quarter = test_data.quarter
        page.set_timezone_for_testing(test_data.timezone)
        top_status,bottom_status,top_id,bottom_id = page.get_game_status(result)
        self.assertEqual(top_status,test_data.top_status)
        self.assertEqual(top_id,test_data.top_id)
        self.assertEqual(bottom_status,test_data.bottom_status)
        self.assertEqual(bottom_id,test_data.bottom_id)
