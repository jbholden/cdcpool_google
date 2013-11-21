import unittest
from google.appengine.ext import db
import logging
import datetime
from weeks_in_database import *

class TestPicks(unittest.TestCase):

    # all this __init__ code is necessary to pass in weeks_to_test parameter
    # http://eli.thegreenplace.net/2011/08/02/python-unit-testing-parametrized-test-cases/
    # this will run only the passed in weeks instead of all the weeks in the database
    def __init__(self,methodName='runTest',weeks_to_test=None):
        super(TestPicks,self).__init__(methodName)
        if weeks_to_test == None:
            self.weeks = WeeksInDatabase.get_all_weeks()
        else:
            assert isinstance(weeks_to_test,dict)
            self.weeks = weeks_to_test

    def test_picks_each_week(self):
        for year in self.weeks:
            for week_number in self.weeks[year]:
                logging.info("picks testing:  %d week %d..." % (year,week_number))
                week = self.__load_week(year,week_number)
                picks = self.__test_week_picks_query(week)
                for pick in picks:
                    self.__check_pick_state(pick,week)

    def test_invalid_week_key(self):
        picks_query = db.GqlQuery('select * from Pick where week=:week',week=None)
        self.assertIsNotNone(picks_query)
        picks = list(picks_query)
        self.assertEqual(len(picks),0)

    def __test_week_picks_query(self,week):
        picks_query = db.GqlQuery('select * from Pick where week=:week',week=week)
        self.assertIsNotNone(picks_query)
        picks = list(picks_query)
        self.assertGreater(len(picks),0)
        return picks

    def __load_week(self,year,week_number):
        weeks_query = db.GqlQuery('SELECT * FROM Week WHERE year=:year and number=:week',year=year,week=week_number)
        assert weeks_query != None
        weeks = list(weeks_query)
        assert len(weeks) == 1
        return weeks[0]

    def __check_pick_state(self,pick,week):
        self.assertIsNotNone(pick.week)
        self.assertEqual(pick.week.year,week.year)
        self.assertEqual(pick.week.number,week.number)
        self.assertIsNotNone(pick.player)
        self.assertIsNotNone(pick.game)
        self.assertIsNotNone(pick.player.name)
        self.assertIsNotNone(pick.game.number)    # just check to see if it can be accessed
        if pick.winner != None:
            self.assertIn(pick.winner,['team1','team2'])
        current_time = datetime.datetime.now()
        self.assertLess(pick.created,current_time)
        self.assertLess(pick.modified,current_time)
