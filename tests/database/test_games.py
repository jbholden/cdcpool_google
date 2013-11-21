import unittest
from google.appengine.ext import db
import logging
import datetime
from weeks_in_database import *

class TestGames(unittest.TestCase):

    # all this __init__ code is necessary to pass in weeks_to_test parameter
    # http://eli.thegreenplace.net/2011/08/02/python-unit-testing-parametrized-test-cases/
    # this will run only the passed in weeks instead of all the weeks in the database
    def __init__(self,methodName='runTest',weeks_to_test=None):
        super(TestGames,self).__init__(methodName)
        if weeks_to_test == None:
            self.weeks = WeeksInDatabase.get_all_weeks()
        else:
            assert isinstance(weeks_to_test,dict)
            self.weeks = weeks_to_test

    def test_all_games_query(self):
        games_query = db.GqlQuery('select * from Game')
        self.assertIsNotNone(games_query)
        games = list(games_query)
        self.assertGreater(len(games),0)
        for game in games:
            self.__check_game_state(game)

    def test_games_not_linked_to_a_week(self):
        games_query = db.GqlQuery('select * from Game')
        self.assertIsNotNone(games_query)
        games = list(games_query)
        self.assertEqual(len(games),self.__count_week_games())

    def __count_week_games(self):
        weeks_query = db.GqlQuery('select * from Week')
        self.assertIsNotNone(weeks_query)
        weeks = list(weeks_query)
        count = 0
        for week in weeks:
            count += len(week.games)
        return count

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
