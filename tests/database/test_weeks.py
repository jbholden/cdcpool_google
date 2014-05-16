import unittest
from google.appengine.ext import db
import logging
import datetime
from code.database import *

class TestWeeks(unittest.TestCase):

    # all this __init__ code is necessary to pass in weeks_to_test parameter
    # http://eli.thegreenplace.net/2011/08/02/python-unit-testing-parametrized-test-cases/
    # this will run only the passed in weeks instead of all the weeks in the database
    def __init__(self,methodName='runTest',weeks_to_test=None):
        super(TestWeeks,self).__init__(methodName)
        if weeks_to_test == None:
            d = Database()
            self.weeks = d.load_weeks_and_years(update=True)
        else:
            assert isinstance(weeks_to_test,dict)
            self.weeks = weeks_to_test

    def test_weeks(self):
        for year in self.weeks:
            for week_number in self.weeks[year]:
                logging.info("week testing:  %d week %d..." % (year,week_number))
                week = self.__test_week_query(year,week_number)
                self.__check_week_state(week,year,week_number)

    def test_invalid_weeks_in_database(self):
        self.__test_invalid_week_query(year=2012,week_number=14)
        self.__test_invalid_week_query(year=2012,week_number=0)
        self.__test_invalid_week_query(year=1900,week_number=1)

    def __test_week_query(self,year,week_number):
        week_query = db.GqlQuery('SELECT * FROM Week WHERE year=:year and number=:number',year=year,number=week_number)
        self.assertIsNotNone(week_query)
        weeks = list(week_query)
        self.assertEqual(len(weeks),1)
        week = weeks[0]
        return week

    def __check_week_state(self,week,year,week_number):
        self.assertIsNotNone(week.year)
        self.assertIsNotNone(week.number)
        self.assertIsNotNone(week.games)
        self.assertEqual(week.year,year)
        self.assertEqual(week.number,week_number)
        self.assertEqual(len(week.games),10)
        if week.winner != None:
            self.__check_player_key_exists(week.winner)
        for game in week.games:
            self.__check_game_key_exists(game)

    def __check_player_key_exists(self,key_value):
        dbkey = db.Key(key_value)
        value = db.get(dbkey)
        self.assertIsNotNone(value)
        self.assertEqual(dbkey.kind(),'Player')

    def __check_game_key_exists(self,game):
        value = db.get(game)
        self.assertIsNotNone(value)
        self.assertEqual(game.kind(),'Game')

    def __test_invalid_week_query(self,year,week_number):
        week_query = db.GqlQuery('SELECT * FROM Week WHERE year=:year and number=:number',year=year,number=week_number)
        self.assertIsNotNone(week_query)
        weeks = list(week_query)
        self.assertEqual(len(weeks),0)
