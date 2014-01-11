import unittest
from google.appengine.ext import db
import logging
import datetime
from code.database import *
from google.appengine.api import memcache
from tests.data.overall_results.pool_not_started import *

# test data required (this module):
# - year with 1 week with no games
# - year with 1 week enter_picks, week_not_started, in_progress, final
# - year with week numbers between 2-13, different states


class TestPoolState(unittest.TestCase):

    def test_end_of_year(self):
        self.assertEqual(self.__get_pool_state(year=2013),"end_of_year")
        self.assertEqual(self.__get_pool_state(year=2012),"end_of_year")

    def test_invalid(self):
        self.assertEqual(self.__get_pool_state(year=1900),"invalid")
        self.assertEqual(self.__get_pool_state(year=1950),"invalid")

    def test_pool_not_started(self):
        test_data = PoolNotStarted()
        test_data.setup()
        self.assertEqual(self.__get_pool_state(year=test_data.year,update=True),"not_started")
        test_data.cleanup()

    def __get_pool_state(self,year,update=False):
        d = Database()
        pool_state = d.get_pool_state(year,update)
        return pool_state
