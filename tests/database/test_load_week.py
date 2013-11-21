import unittest
from google.appengine.ext import db
import logging
import datetime
from weeks_in_database import *
from code.database import *
from google.appengine.api import memcache

class TestWeekLoad(unittest.TestCase):

    # all this __init__ code is necessary to pass in weeks_to_test parameter
    # http://eli.thegreenplace.net/2011/08/02/python-unit-testing-parametrized-test-cases/
    # this will run only the passed in weeks instead of all the weeks in the database
    def __init__(self,methodName='runTest',weeks_to_test=None):
        super(TestWeekLoad,self).__init__(methodName)
        if weeks_to_test == None:
            self.weeks = WeeksInDatabase.get_all_weeks()
        else:
            assert isinstance(weeks_to_test,dict)
            self.weeks = weeks_to_test

    def test_weeks_with_empty_cache(self):
        logging.info("load empty cache week testing...")
        memcache.flush_all()
        for year in self.weeks:
            for week_number in self.weeks[year]:
                logging.info("load empty cache week testing:  %d week %d..." % (year,week_number))
                week,games,picks = self.__test_week_load(year,week_number)
                self.__check_load_week_state(year,week_number,week,games,picks)

    def test_weeks_with_cache_populated(self):
        logging.info("load populated cache week testing...")
        memcache.flush_all()
        self.__load_memcache_with_all_weeks()
        for year in self.weeks:
            for week_number in self.weeks[year]:
                logging.info("load populated cache week testing:  %d week %d..." % (year,week_number))
                start = time.time()
                week,games,picks = self.__test_week_load(year,week_number)
                elapsed_time = time.time()-start
                self.__check_load_week_state(year,week_number,week,games,picks)
                self.assertLess(elapsed_time,1.00)

    def test_invalid_weeks_with_empty_cache(self):
        logging.info("invalid week empty cache testing...")
        memcache.flush_all()
        self.__test_invalid_week_query(year=2012,week_number=14)
        self.__test_invalid_week_query(year=2012,week_number=0)
        self.__test_invalid_week_query(year=1776,week_number=1)

    def test_invalid_weeks_with_populated_cache(self):
        logging.info("invalid week populated cache testing...")
        memcache.flush_all()
        self.__load_memcache_with_all_weeks()
        self.__test_invalid_week_query(year=2012,week_number=14)
        self.__test_invalid_week_query(year=2012,week_number=0)
        self.__test_invalid_week_query(year=1776,week_number=1)

    def __load_memcache_with_all_weeks(self):
        logging.info("loading memcache with all weeks (make take a few minutes)...")
        for year in self.weeks:
            for week_number in self.weeks[year]:
                #logging.info("loading week into memcache:  %d week %d..." % (year,week_number))
                d = Database()
                week,games,picks = d.load_week_data(year,week_number,update=True)

    def __test_week_load(self,year,week_number):
        d = Database()
        week,games,picks = d.load_week_data(year,week_number)
        self.assertIsNotNone(week)
        self.assertIsNotNone(games)
        self.assertIsNotNone(picks)
        return week,games,picks

    def __check_load_week_state(self,year,week_number,week,games,picks):
        self.__check_week_state(week,year,week_number)
        self.assertEqual(len(games),10)
        for game in games:
            self.__check_game_state(game)
        self.assertGreater(len(picks.keys()),0)
        for player in picks:
            player_picks = picks[player]
            for pick in player_picks:
                self.__check_pick_state(pick,week)

    def __test_invalid_week_query(self,year,week_number):
        d = Database()
        with self.assertRaises(AssertionError):
            week,games,picks = d.load_week_data(year,week_number)

    def __check_week_state(self,week,year,week_number):
        self.assertIsNotNone(week.year)
        self.assertIsNotNone(week.number)
        self.assertIsNotNone(week.games)
        self.assertEqual(week.year,year)
        self.assertEqual(week.number,week_number)
        self.assertEqual(len(week.games),10)
        if week.winner != None:
            self.assertIsNotNone(week.winner)
        for game in week.games:
            self.__check_game_key_exists(game)

    def __check_game_key_exists(self,game):
        value = db.get(game)
        self.assertIsNotNone(value)
        self.assertEqual(game.kind(),'Game')

    def __check_game_state(self,game):
        self.assertIsNotNone(game.number)
        self.assertIn(game.number,range(1,11))
        self.assertIsNotNone(game.team1)
        self.assertIsNotNone(game.team2)
        self.assertIsNotNone(game.team1.name)
        self.assertIsNotNone(game.team2.name)
        self.assertIsNotNone(game.favored)
        self.assertIn(game.favored,['team1','team2'])
        self.assertIsNotNone(game.spread)
        self.__ensure_spread_value_is_a_half(game.spread)
        self.assertIsNotNone(game.state)
        self.assertIn(game.state,['not_started','in_progress','final'])

    def __ensure_spread_value_is_a_half(self,spread):
        fraction = spread - int(spread)
        return self.assertEqual(fraction,0.5)

    def __check_pick_state(self,pick,week):
        self.assertIsNotNone(pick.week)
        self.assertEqual(pick.week.number,week.number)
        self.assertEqual(pick.week.year,week.year)
        self.assertIsNotNone(pick.player)
        self.assertIsNotNone(pick.player.name)
        self.assertIsNotNone(pick.game)
        self.assertIsNotNone(pick.game.number)
        if pick.winner != None:
            self.assertIn(pick.winner,['team1','team2'])
        current_time = datetime.datetime.now()
        self.assertLess(pick.created,current_time)
        self.assertLess(pick.modified,current_time)
