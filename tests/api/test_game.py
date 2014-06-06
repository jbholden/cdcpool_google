ROOT_PATH = '../../.'
import sys
sys.path.append(ROOT_PATH)

import unittest
import socket
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

            created_game = self.fbpool.createGame(game)
            self.fbpool.deleteGameByID(created_game['id'])
            self.fbpool.deleteTeamIfExists("Team1")
            self.fbpool.deleteTeamIfExists("Team2")

        except FBAPIException as e:
            print e
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

            created_game = self.fbpool.createGame(game)
            self.fbpool.deleteGameByID(created_game['id'])
            self.fbpool.deleteTeamIfExists("Team1")
            self.fbpool.deleteTeamIfExists("Team2")

        except FBAPIException as e:
            print "code=%d, message=%s" % (e.http_code,e.errmsg)
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

            created_game = self.fbpool.createGame(game)
            self.fbpool.deleteGameByID(created_game['id'])
            self.fbpool.deleteTeamIfExists("Team1")
            self.fbpool.deleteTeamIfExists("Team2")

        except FBAPIException as e:
            self.assertTrue(False)
            return

        self.__verify_game(created_game,**game)

    def test_delete_game_by_id(self):
        try:
            created_game = self.__create_game_for_test()
            self.fbpool.deleteGameByID(created_game['id'])
        except FBAPIException as e:
            print e
            self.assertTrue(False)
            return

        try:
            game = self.fbpool.getGameByID(created_game['id'])
            print "Game still exists."
            self.assertTrue(False)
        except FBAPIException as e:
            self.assertEquals(e.http_code,404)
            self.assertEquals(e.errmsg,"could not find the game")
            return

        self.__cleanup_created_game_teams()

    def test_delete_game_by_key(self):
        try:
            created_game = self.__create_game_for_test()
            self.fbpool.deleteGameByKey(created_game['key'])
        except FBAPIException as e:
            print e
            self.assertTrue(False)
            return

        try:
            game = self.fbpool.getGameByID(created_game['id'])
            print "Game still exists."
            self.assertTrue(False)
        except FBAPIException as e:
            self.assertEquals(e.http_code,404)
            self.assertEquals(e.errmsg,"could not find the game")
            return

        self.__cleanup_created_game_teams()

    def test_delete_all_games(self):
        try:
            created_game = self.__create_game_for_test()
            self.fbpool.deleteAllGames()
            games = self.fbpool.getAllGames()
            self.assertEquals(len(games),0)
        except FBAPIException as e:
            print e
            self.assertTrue(False)
            return

        self.__cleanup_created_game_teams()

    def test_get_game_by_id(self):
        try:
            created_game = self.__create_game_for_test()
            game = self.fbpool.getGameByID(created_game['id'])
            self.fbpool.deleteGameByID(created_game['id'])
        except FBAPIException as e:
            print e
            self.assertTrue(False)
            return

        self.assertIn('id',game)
        self.assertEquals(created_game['id'],game['id'])
        self.__cleanup_created_game_teams()

    def test_get_game_by_key(self):
        try:
            created_game = self.__create_game_for_test()
            game = self.fbpool.getGameByKey(created_game['key'])
            self.fbpool.deleteGameByID(created_game['id'])
        except FBAPIException as e:
            print e
            self.assertTrue(False)
            return

        self.assertIn('key',game)
        self.assertEquals(created_game['key'],game['key'])
        self.__cleanup_created_game_teams()

    def test_get_all_games(self):
        try:
            self.fbpool.deleteAllGames()
            created_game1 = self.__create_game_for_test()
            created_game2 = self.__create_game_for_test()
            created_game3 = self.__create_game_for_test()
            games = self.fbpool.getAllGames()
            self.fbpool.deleteAllGames()
        except FBAPIException as e:
            print "code=%d, message=%s" % (e.http_code,e.errmsg)
            self.assertTrue(False)
            return

        self.assertEquals(len(games),3)

        game_ids = sorted([game['id'] for game in games ])
        expected_ids = sorted([ created_game1['id'], created_game2['id'], created_game3['id' ]])

        self.assertEquals(game_ids,expected_ids)
        self.__cleanup_created_game_teams()

    def test_edit_game_by_id(self):
        try:
            created_game = self.__create_game_for_test()

            game = dict()
            game['number'] = 5
            game['team1'] = created_game['team2']
            game['team2'] = created_game['team1']
            game['team1_score'] = 10
            game['team2_score'] = 17 
            game['favored'] = "team1"
            game['spread'] = 9.5
            game['state'] = "in_progress"
            game['quarter'] = "3rd"
            game['time_left'] = "10:10"
            game['date'] = "09/06/2014 19:00"

            self.fbpool.editGameByID(created_game['id'],game)

            edited_game = self.fbpool.getGameByID(created_game['id'])
            self.fbpool.deleteGameByID(created_game['id'])
        except FBAPIException as e:
            print e
            self.assertTrue(False)
            return

        self.__verify_game(edited_game,**game)
    
    def test_edit_game_by_key(self):
        try:
            created_game = self.__create_game_for_test()

            game = dict()
            game['number'] = 5
            game['team1'] = created_game['team2']
            game['team2'] = created_game['team1']
            game['team1_score'] = 10
            game['team2_score'] = 17 
            game['favored'] = "team1"
            game['spread'] = 9.5
            game['state'] = "in_progress"
            game['quarter'] = "3rd"
            game['time_left'] = "10:10"
            game['date'] = "09/06/2014 19:00"

            self.fbpool.editGameByKey(created_game['key'],game)

            edited_game = self.fbpool.getGameByID(created_game['id'])
            self.fbpool.deleteGameByID(created_game['id'])
        except FBAPIException as e:
            print e
            self.assertTrue(False)
            return

        self.__verify_game(edited_game,**game)

    def __create_game_for_test(self):
        team1 = self.fbpool.createTeamIfDoesNotExist("Team1","Conference1")
        team2 = self.fbpool.createTeamIfDoesNotExist("Team2","Conference1")

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

        created_game = self.fbpool.createGame(game)
        return created_game

    def __cleanup_created_game_teams(self):
        try:
            self.fbpool.deleteTeamIfExists("Team1")
            self.fbpool.deleteTeamIfExists("Team2")
        except FBAPIException as e:
            print e
            self.AssertTrue(False)
            return

    def __verify_game(self,game,number=None,team1=None,team2=None,team1_score=None,team2_score=None,favored=None,spread=None,state=None,quarter=None,time_left=None,date=None):
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
