import unittest
from google.appengine.ext import db
import logging
import datetime
from code.database import *

class TestPicks(unittest.TestCase):

    # all this __init__ code is necessary to pass in weeks_to_test parameter
    # http://eli.thegreenplace.net/2011/08/02/python-unit-testing-parametrized-test-cases/
    # this will run only the passed in weeks instead of all the weeks in the database
    def __init__(self,methodName='runTest',weeks_to_test=None):
        super(TestPicks,self).__init__(methodName)
        if weeks_to_test == None:
            d = Database()
            self.weeks = d.load_weeks_and_years(update=True)
        else:
            assert isinstance(weeks_to_test,dict)
            self.weeks = weeks_to_test

    def test_picks_each_week(self):
        for year in self.weeks:
            for week_number in self.weeks[year]:
                logging.info("picks testing:  %d week %d..." % (year,week_number))
                week_key = self.__load_week(year,week_number)
                picks = self.__test_week_picks_query(week_key)
                for pick in picks:
                    self.__check_pick_state(pick,week_key)

    def test_invalid_week_key(self):
        picks_query = db.GqlQuery('select * from Pick where week=:week',week="garbage")
        self.assertIsNotNone(picks_query)
        picks = list(picks_query)
        self.assertEqual(len(picks),0)

    def __test_week_picks_query(self,week_key):
        picks_query = db.GqlQuery('select * from Pick where week=:week',week=week_key)
        self.assertIsNotNone(picks_query)
        picks = list(picks_query)
        self.assertGreater(len(picks),0)
        return picks

    def __load_week(self,year,week_number):
        weeks_query = db.GqlQuery('SELECT * FROM Week WHERE year=:year and number=:week',year=year,week=week_number)
        assert weeks_query != None
        weeks = list(weeks_query)
        assert len(weeks) == 1
        return str(weeks[0].key())

    def __check_pick_state(self,pick,week_key):
        self.assertEqual(pick.week,week_key)
        self.assertIsNotNone(pick.player)
        self.assertIsNotNone(pick.game)
        self.__check_key_exists('Player',pick.player)
        self.__check_key_exists('Game',pick.game)
        if pick.winner != None:
            self.assertIn(pick.winner,['team1','team2'])
        current_time = datetime.datetime.now()
        self.assertLess(pick.created,current_time)
        self.assertLess(pick.modified,current_time)

    def __check_key_exists(self,kind,key_value):
        dbkey = db.Key(key_value)
        value = db.get(dbkey)
        self.assertIsNotNone(value)
        self.assertEqual(dbkey.kind(),kind)
