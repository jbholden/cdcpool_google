ROOT_PATH = '../../.'
import sys
sys.path.append(ROOT_PATH)

import unittest
import socket
import logging
from scripts.api.fbpool_api import *
from scripts.api.fbpool_api_exception import *

class TestGame(unittest.TestCase):

    def setUp(self):
        url = "http://localhost:10090"
        self.fbpool = FBPoolAPI(url=url)

    def test_create_not_started_game(self):
        try:
            self.fbpool.deleteTeamIfExists("Team1")
            self.fbpool.deleteTeamIfExists("Team2")
            team1 = self.fbpool.createTeam("Team1","Conference1")
            team2 = self.fbpool.createTeam("Team2","Conference1")

            game = dict()
            game['number'] = 1
            game['team1'] = team1['key']
            game['team2'] = team2['key']
            game['team1_score'] = None
            game['team2_score'] = None
            game['favored'] = "team1"
            game['spread'] = 0.5
            game['state'] = "not_started"
            game['quarter'] = None
            game['time_left'] = None
            game['date'] = None

            created_game = self.fbpool.createGame(**game)
            self.fbpool.deleteGameById(created_game['id'])

        except FBAPIException as e:
            logging.info(e)
            self.assertTrue(False)
            return

        self.__verify_game(created_game,**game)

    def test_create_in_progress_game(self):
        try:
            self.fbpool.deleteTeamIfExists("Team1")
            self.fbpool.deleteTeamIfExists("Team2")
            team1 = self.fbpool.createTeam("Team1","Conference1")
            team2 = self.fbpool.createTeam("Team2","Conference1")

            game = dict()
            game['number'] = 2
            game['team1'] = team1['key']
            game['team2'] = team2['key']
            game['team1_score'] = 31
            game['team2_score'] = 7 
            game['favored'] = "team2"
            game['spread'] = 10.5
            game['state'] = "in_progress"
            game['quarter'] = "3rd"
            game['time_left'] = "9:57"
            game['date'] = "09/05/2014 19:00"

            created_game = self.fbpool.createGame(**game)
            self.fbpool.deleteGameById(created_game['id'])

        except FBAPIException as e:
            logging.info(e)
            self.assertTrue(False)
            return

        self.__verify_game(created_game,**game)


    def test_create_final_game(self):
        try:
            self.fbpool.deleteTeamIfExists("Team1")
            self.fbpool.deleteTeamIfExists("Team2")
            team1 = self.fbpool.createTeam("Team1","Conference1")
            team2 = self.fbpool.createTeam("Team2","Conference1")

            game = dict()
            game['number'] = 2
            game['team1'] = team1['key']
            game['team2'] = team2['key']
            game['team1_score'] = 21
            game['team2_score'] = 20 
            game['favored'] = "team2"
            game['spread'] = 0.5
            game['state'] = "final"
            game['quarter'] = None
            game['time_left'] = None
            game['date'] = "09/05/2014 19:00"

            created_game = self.fbpool.createGame(**game)
            self.fbpool.deleteGameById(created_game['id'])

        except FBAPIException as e:
            logging.info(e)
            self.assertTrue(False)
            return

        self.__verify_game(created_game,**game)


    def __verify_game(self,game,number=None,team1=None,team2=None,team1_score=None,team2_score=None,favored=None,spread=None,quarter=None,time_left=None,date=None):
        self.assertIn('id',game)
        self.assertIn('key',game)
        self.assertIn('number',game)
        self.assertIn('team1',game)
        self.assertIn('team2',game)
        self.assertIn('team1_score',game)
        self.assertIn('team2_score',game)
        self.assertIn('favored',game)
        self.assertIn('spread',game)
        self.assertIn('state',game)
        self.assertIn('quarter',game)
        self.assertIn('time_left',game)
        self.assertIn('date',game)

        self.assertEquals(game['number'],number)
        self.assertEquals(game['team1'],team1)
        self.assertEquals(game['team2'],team2)
        self.assertEquals(game['team1_score'],team1_score)
        self.assertEquals(game['team2_score'],team2_score)
        self.assertEquals(game['favored'],favored)
        self.assertEquals(game['spread'],spread)
        self.assertEquals(game['state'],state)
        self.assertEquals(game['quarter'],quarter)
        self.assertEquals(game['time_left'],time_left)
        self.assertEquals(game['date'],date)


if __name__ == "__main__":
    unittest.main()
