import unittest
from google.appengine.ext import db
import logging
import datetime
from weeks_in_database import *
from code.database import *
from google.appengine.api import memcache

class TestWeekLoad(unittest.TestCase):

    #@staticmethod
    #def run_subset():
        #return ["test_get_week_numbers_with_populated_cache"]

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
                week_data = self.__test_week_load(year,week_number)
                self.__check_load_week_state(year,week_number,week_data)

    def test_weeks_with_cache_populated(self):
        logging.info("load populated cache week testing...")
        memcache.flush_all()
        self.__load_memcache_with_all_weeks()
        for year in self.weeks:
            for week_number in self.weeks[year]:
                logging.info("load populated cache week testing:  %d week %d..." % (year,week_number))
                start = time.time()
                week_data = self.__test_week_load(year,week_number)
                elapsed_time = time.time()-start
                self.__check_load_week_state(year,week_number,week_data)
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

    def test_load_teams_with_empty_cache(self):
        logging.info("load teams empty cache testing...")
        memcache.flush_all()
        self.__load_teams_test()

    def test_load_teams_with_populated_cache(self):
        logging.info("load teams populated cache testing...")
        memcache.flush_all()
        self.__load_memcache_with_teams()
        self.__load_teams_test()

    def test_load_players_with_empty_cache(self):
        logging.info("load players empty cache testing...")
        memcache.flush_all()
        self.__load_players_test(2012)
        self.__load_players_test(2013)

    def test_load_players_with_populated_cache(self):
        logging.info("load players populated cache testing...")
        memcache.flush_all()
        self.__load_memcache_with_players()
        self.__load_players_test(2012)
        self.__load_players_test(2013)

    def test_load_weeks_and_years_with_empty_cache(self):
        logging.info("load weeks and years empty cache...")
        memcache.flush_all()
        self.__load_weeks_and_years_test()

    def test_load_weeks_and_years_with_populated_cache(self):
        logging.info("load weeks and years populated cache...")
        memcache.flush_all()
        self.__load_memcache_with_weeks_and_years()
        self.__load_weeks_and_years_test()

    def test_get_years_with_empty_cache(self):
        logging.info("load get_years empty cache...")
        memcache.flush_all()
        self.__get_years_test()

    def test_get_years_with_populated_cache(self):
        logging.info("load get_years populated cache...")
        memcache.flush_all()
        self.__load_memcache_with_years()
        self.__get_years_test()

    def test_get_week_numbers_with_empty_cache(self):
        logging.info("load get_weeks empty cache...")
        memcache.flush_all()
        self.__get_weeks_test(2012,[1,2,3,4,5,6,7,8,9,10,11,12,13])
        memcache.flush_all()
        self.__get_weeks_test(2013,[1,2,3,4,5,6,7,8,9,10,11,12,13])
        memcache.flush_all()
        self.__get_weeks_invalid_year_test()

    def test_get_week_numbers_with_populated_cache(self):
        logging.info("load get_weeks populated cache...")
        memcache.flush_all()
        self.__load_memcache_with_weeks()
        self.__get_weeks_test(2012,[1,2,3,4,5,6,7,8,9,10,11,12,13])
        self.__get_weeks_test(2013,[1,2,3,4,5,6,7,8,9,10,11,12,13])
        self.__get_weeks_invalid_year_test()

    def __load_memcache_with_all_weeks(self):
        logging.info("loading memcache with all weeks (make take a few minutes)...")
        for year in self.weeks:
            for week_number in self.weeks[year]:
                #logging.info("loading week into memcache:  %d week %d..." % (year,week_number))
                d = Database()
                week_data = d.load_week_data(year,week_number,update=True)

    def __load_memcache_with_teams(self):
        d = Database()
        ignore_return_value = d.load_teams('teams',update=True)

    def __load_memcache_with_players(self):
        d = Database()
        ignore_return_value = d.load_players(year=2012,update=True)
        ignore_return_value = d.load_players(year=2013,update=True)

    def __test_week_load(self,year,week_number):
        d = Database()
        week_data = d.load_week_data(year,week_number)
        self.assertIsNotNone(week_data.week)
        self.assertIsNotNone(week_data.games)
        self.assertIsNotNone(week_data.picks)
        self.assertIsNotNone(week_data.player_picks)
        self.assertIsNotNone(week_data.players)
        self.assertIsNotNone(week_data.teams)
        return week_data

    def __check_load_week_state(self,year,week_number,week_data):
        self.__check_week_state(week_data.week,year,week_number)

        self.assertEqual(len(week_data.games),10)
        for game_key in week_data.games:
            game = week_data.games[game_key]
            self.__check_game_state(game)

        week_key = str(week_data.week.key())

        self.assertGreater(len(week_data.picks.keys()),0)
        for pick_key in week_data.picks:
            self.__check_pick_state(week_data.picks[pick_key],week_key)

        self.assertGreater(len(week_data.player_picks.keys()),0)
        for player_key in week_data.player_picks:
            for pick in week_data.player_picks[player_key]:
                self.__check_pick_state(pick,week_key)

        self.assertGreater(len(week_data.players.keys()),0)
        self.assertGreater(len(week_data.teams.keys()),0)


    def __test_invalid_week_query(self,year,week_number):
        d = Database()
        with self.assertRaises(AssertionError):
            week_data = d.load_week_data(year,week_number)

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

    def __check_game_state(self,game):
        self.assertIsNotNone(game.number)
        self.assertIn(game.number,range(1,11))
        self.assertIsNotNone(game.team1)
        self.assertIsNotNone(game.team2)
        self.__check_team_key_exists(game.team1)
        self.__check_team_key_exists(game.team2)
        self.assertIsNotNone(game.favored)
        self.assertIn(game.favored,['team1','team2'])
        self.assertIsNotNone(game.spread)
        self.__ensure_spread_value_is_a_half(game.spread)
        self.assertIsNotNone(game.state)
        self.assertIn(game.state,['not_started','in_progress','final'])

    def __check_team_key_exists(self,key_value):
        dbkey = db.Key(key_value)
        value = db.get(dbkey)
        self.assertIsNotNone(value)
        self.assertEqual(dbkey.kind(),'Team')

    def __ensure_spread_value_is_a_half(self,spread):
        fraction = spread - int(spread)
        return self.assertEqual(fraction,0.5)

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

    def __load_teams_test(self):
        d = Database()
        teams = d.load_teams('teams')
        self.assertIsNotNone(teams)
        self.assertGreater(len(teams),0)
        for team_key in teams:
            team = teams[team_key]
            self.assertIsNotNone(team.name)
            self.assertIsNotNone(team.conference)

    def __load_players_test(self,year):
        d = Database()
        players = d.load_players(year)
        self.assertIsNotNone(players)
        self.assertGreater(len(players),0)
        for player_key in players:
            player = players[player_key]
            self.assertIsNotNone(player.name)
            self.assertIn(year,player.years)

    def __load_memcache_with_weeks_and_years(self):
        d = Database()
        ignore_return_value = d.load_weeks_and_years(update=True)

    def __load_memcache_with_years(self):
        d = Database()
        ignore_return_value = d.get_years(update=True)

    def __load_memcache_with_weeks(self):
        d = Database()
        ignore_return_value = d.get_week_numbers(2013,update=True)

    def __load_weeks_and_years_test(self):
        d = Database()
        weeks_and_years = d.load_weeks_and_years()
        self.assertIsNotNone(weeks_and_years)
        self.assertIn(2012,weeks_and_years)
        self.assertIn(2013,weeks_and_years)
        self.assertEqual(sorted(weeks_and_years[2012]),[1,2,3,4,5,6,7,8,9,10,11,12,13])
        self.assertEqual(sorted(weeks_and_years[2013]),[1,2,3,4,5,6,7,8,9,10,11,12,13])

    def __get_years_test(self):
        d = Database()
        years = d.get_years()
        self.assertIsNotNone(years)
        self.assertIn(2012,years)
        self.assertIn(2013,years)

    def __get_weeks_test(self,year,expected_weeks):
        d = Database()
        weeks = d.get_week_numbers(year)
        self.assertIsNotNone(weeks)
        self.assertEqual(weeks,expected_weeks)

    def __get_weeks_invalid_year_test(self):
        d = Database()
        with self.assertRaises(Exception):
            weeks = d.get_week_numbers(1900)
        

