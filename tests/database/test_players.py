import unittest
from google.appengine.ext import db
import logging
import datetime
from code.database import *

class TestPlayers(unittest.TestCase):

    # all this __init__ code is necessary to pass in weeks_to_test parameter
    # http://eli.thegreenplace.net/2011/08/02/python-unit-testing-parametrized-test-cases/
    # this will run only the passed in weeks instead of all the weeks in the database
    def __init__(self,methodName='runTest',weeks_to_test=None):
        super(TestPlayers,self).__init__(methodName)
        if weeks_to_test == None:
            self.weeks = self.load_weeks_and_years(update=True)
        else:
            assert isinstance(weeks_to_test,dict)
            self.weeks = weeks_to_test

    def test_players_in_each_year_query(self):
        for year in self.weeks:
            logging.info("player testing:  %d..." % (year))
            players = self.__test_players_in_a_year_query(year)
            for player in players:
                self.__check_player_state(player,year)

    def test_player_by_name_query(self):
        # assumption:  these players exist in all available years (may have to change)
        names = [ 'Brent H.', 'Byron R.' ]
        for name in names:
            player = self.__test_player_by_name_query(name)
            for year in self.weeks:
                self.__check_player_state(player,year)

    def test_invalid_player_names(self):
        self.__test_invalid_player_name_query(name='playerxxx')
        self.__test_invalid_player_name_query(name='')
        self.__test_invalid_player_name_query(name=None)

    def test_invalid_player_year(self):
        self.__test_invalid_player_year_query(year=1900)
        self.__test_invalid_player_year_query(year=-1)
        self.__test_invalid_player_year_query(year=None)

    def __test_player_by_name_query(self,name):
        players_query = db.GqlQuery('select * from Player where name=:name',name=name)
        self.assertIsNotNone(players_query)
        players = list(players_query)
        self.assertEquals(len(players),1)
        return players[0]

    def __test_invalid_player_name_query(self,name):
        players_query = db.GqlQuery('select * from Player where name=:name',name=name)
        self.assertIsNotNone(players_query)
        players = list(players_query)
        self.assertEqual(len(players),0)

    def __test_players_in_a_year_query(self,year):
        players_query = db.GqlQuery('select * from Player where years IN :year',year=[year])
        self.assertIsNotNone(players_query)
        players = list(players_query)
        self.assertGreater(len(players),0)
        return players

    def __test_invalid_player_year_query(self,year):
        players_query = db.GqlQuery('select * from Player where years IN :year',year=[year])
        self.assertIsNotNone(players_query)
        players = list(players_query)
        self.assertEqual(len(players),0)

    def __check_player_state(self,player,year):
        self.assertIsNotNone(player.name)
        self.assertIsNotNone(player.years)
        self.assertIn(year,player.years)

