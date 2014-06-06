ROOT_PATH = '../../.'
import sys
sys.path.append(ROOT_PATH)

import unittest
import socket
import logging
from scripts.api.fbpool_api import *
from scripts.api.fbpool_api_exception import *


class TestPlayer(unittest.TestCase):

    def setUp(self):
        url = "http://localhost:10090"
        self.fbpool = FBPoolAPI(url=url)

    def test_create_player(self):
        try:
            self.fbpool.deletePlayerIfExists("Player1")
            player = self.fbpool.createPlayer("Player1",[1980,1990,2000])
            self.fbpool.deletePlayerByID(player['id'])
        except FBAPIException as e:
            print str(e)
            self.assertTrue(False)
            return

        self.__verify_player(player,"Player1",[1980,1990,2000])

    def test_create_existing_player(self):
        try:
            self.fbpool.deletePlayerIfExists("Player1")
            player1 = self.fbpool.createPlayer("Player1",[1980,1990,2000])
            player2 = self.fbpool.createPlayer("Player1",[1980,1990,2000])
            self.assertTrue(False)
        except FBAPIException as e:
            if e.http_code != 409 or e.errmsg != "player already exists":
                self.assertTrue(False)
                return

        try:
            self.fbpool.deletePlayerByID(player['id'])
        except FBAPIException as e:
            self.assertTrue(False)
            return

    def test_get_player_by_name(self):
        try:
            self.fbpool.createPlayerIfDoesNotExist("Player1",[2014])
            player = self.fbpool.getPlayer("Player1")
            self.fbpool.deletePlayerByID(player['id'])
        except FBAPIException as e:
            print str(e)
            self.assertTrue(False)
            return

        self.__verify_player(player,"Player1",[2014])

    def test_get_player_by_id(self):
        try:
            self.fbpool.createPlayerIfDoesNotExist("Player2",[2014])
            player = self.fbpool.getPlayerByID("Player2")
            self.fbpool.deletePlayerByID(player['id'])
        except FBAPIException as e:
            print str(e)
            self.assertTrue(False)
            return

        self.__verify_player(player,"Player2",[2014])

    def test_get_player_by_key(self):
        try:
            self.fbpool.createPlayerIfDoesNotExist("Player2",[2014])
            player = self.fbpool.getPlayerByKey("Player2")
            self.fbpool.deletePlayerByID(player['id'])
        except FBAPIException as e:
            print str(e)
            self.assertTrue(False)
            return

        self.__verify_player(player,"Player2",[2014])

    def test_get_all_players(self):
        try:
            self.fbpool.deleteAllPlayers()
            player1 = self.fbpool.createPlayer("Player1",[2014])
            player2 = self.fbpool.createPlayer("Player2",[2014])
            player3 = self.fbpool.createPlayer("Player3",[2000])
            player4 = self.fbpool.createPlayer("Player4",[2000])
            player5 = self.fbpool.createPlayer("Player5",[2010])
            players = self.fbpool.getAllPlayers()
            self.fbpool.deleteAllPlayers()
        except FBAPIException as e:
            print str(e)
            self.assertTrue(False)
            return

        player_names = sorted([player.name for player in players ])
        self.assertEquals(["Player1","Player2","Player3","Player4","Player5"],player_names)

    def test_get_players_in_year(self):
        try:
            self.fbpool.deleteAllPlayers()
            player1 = self.fbpool.createPlayer("Player1",[2014])
            player2 = self.fbpool.createPlayer("Player2",[2014])
            player3 = self.fbpool.createPlayer("Player3",[2000])
            player4 = self.fbpool.createPlayer("Player4",[2000])
            player5 = self.fbpool.createPlayer("Player5",[2010])
            players = self.fbpool.getPlayersInYear(2000)
            self.fbpool.deleteAllPlayers()
        except FBAPIException as e:
            print str(e)
            self.assertTrue(False)
            return

        player_names = sorted([player.name for player in players ])
        self.assertEquals(["Player3","Player4"],player_names)

    def test_delete_all_players(self):
        try:
            self.fbpool.deleteAllPlayers()
            player1 = self.fbpool.createPlayer("Player1",[2014])
            player2 = self.fbpool.createPlayer("Player2",[2014])
            player3 = self.fbpool.createPlayer("Player3",[2000])
            player4 = self.fbpool.createPlayer("Player4",[2000])
            player5 = self.fbpool.createPlayer("Player5",[2010])
            self.fbpool.deleteAllPlayers()
            players = self.fbpool.getAllPlayers()
        except FBAPIException as e:
            print str(e)
            self.assertTrue(False)
            return

        self.assertEquals(len(players),0)

    def test_delete_player_by_id(self):
        try:
            self.fbpool.deleteAllPlayers()
            player1 = self.fbpool.createPlayer("Player1",[2014])
            player2 = self.fbpool.createPlayer("Player2",[2014])
            player3 = self.fbpool.createPlayer("Player3",[2000])
            player4 = self.fbpool.createPlayer("Player4",[2000])
            player5 = self.fbpool.createPlayer("Player5",[2010])
            self.fbpool.deletePlayerByID(player3['id'])
            players = self.fbpool.getAllPlayers()
            self.fbpool.deleteAllPlayers()
        except FBAPIException as e:
            print str(e)
            self.assertTrue(False)
            return

        player_names = sorted([player.name for player in players ])
        self.assertEquals(["Player1","Player2","Player4","Player5"],player_names)

    def test_delete_player_by_key(self):
        try:
            self.fbpool.deleteAllPlayers()
            player1 = self.fbpool.createPlayer("Player1",[2014])
            player2 = self.fbpool.createPlayer("Player2",[2014])
            player3 = self.fbpool.createPlayer("Player3",[2000])
            player4 = self.fbpool.createPlayer("Player4",[2000])
            player5 = self.fbpool.createPlayer("Player5",[2010])
            self.fbpool.deletePlayerByKey(player3['key'])
            players = self.fbpool.getAllPlayers()
            self.fbpool.deleteAllPlayers()
        except FBAPIException as e:
            print str(e)
            self.assertTrue(False)
            return

        player_names = sorted([player.name for player in players ])
        self.assertEquals(["Player1","Player2","Player4","Player5"],player_names)

    def test_edit_player_by_id(self):
        try:
            self.fbpool.deletePlayerIfExists("Player1")
            self.fbpool.deletePlayerIfExists("Player3")
            player = self.fbpool.createPlayer("Player1",[1980,1990,2000])

            data = dict()
            data['name'] = 'Player3'
            data['years'] = [ 2010,2011,2013 ]

            self.fbpool.editPlayerByID(player['id'],data)
            player = self.fbpool.getPlayerByID(player['id'])
            self.fbpool.deletePlayerByID(player['id'])
        except FBAPIException as e:
            print str(e)
            self.assertTrue(False)
            return

        self.__verify_player(player,"Player3",[2010,2011,2013])

    def test_edit_player_by_key(self):
        try:
            self.fbpool.deletePlayerIfExists("Player1")
            self.fbpool.deletePlayerIfExists("Player3")
            player = self.fbpool.createPlayer("Player1",[1980,1990,2000])

            data = dict()
            data['name'] = 'Player3'
            data['years'] = [ 2010,2011,2013 ]

            self.fbpool.editPlayerByKey(player['key'],data)
            player = self.fbpool.getPlayerByID(player['id'])
            self.fbpool.deletePlayerByID(player['id'])
        except FBAPIException as e:
            print str(e)
            self.assertTrue(False)
            return

    def test_edit_player_existing_name(self):
        try:
            self.fbpool.deletePlayerIfExists("Player1")
            self.fbpool.deletePlayerIfExists("Player3")
            player = self.fbpool.createPlayer("Player1",[1980,1990,2000])
            player = self.fbpool.createPlayer("Player3",[1980,1990,2000])

            data = dict()
            data['name'] = 'Player3'
            data['years'] = [ 2010,2011,2013 ]

            self.fbpool.editPlayerByKey(player['key'],data)
            self.assertTrue(False)  # should get an exception
        except FBAPIException as e:
            if e.http_code != 409 or e.errmsg != "player already exists":
                self.assertTrue(False)
                return

        # cleanup
        try:
            self.fbpool.deletePlayerByID(player['id'])
        except FBAPIException as e:
            self.assertTrue(False)
            return


    def __verify_player(self,player,name,years):
        self.assertIn('id',player)
        self.assertIn('key',player)
        self.assertIn('name',player)
        self.assertIn('years',player)
        self.assertEquals(player['name'],name)
        self.assertEquals(sorted(player['years']),sorted(years))

if __name__ == "__main__":
    unittest.main()
