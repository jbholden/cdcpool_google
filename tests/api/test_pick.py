ROOT_PATH = '../../.'
import sys
sys.path.append(ROOT_PATH)

import unittest
import socket
from scripts.api.fbpool_api import *
from scripts.api.fbpool_api_exception import *

class TestPick(unittest.TestCase):

    def setUp(self):
        url = "http://localhost:10090"
        self.fbpool = FBPoolAPI(url=url)

    def test_create_pick(self):
        week,game,player = self.__setup_pick_data(1984,1,"Player1")

        data = dict()
        data['week'] = week['key']
        data['player'] = player['key']
        data['game'] = game['key']
        data['winner'] = "team1"
        data['team1_score'] = None
        data['team2_score'] = None

        try:
            pick = self.fbpool.createPick(data)
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            self.assertTrue(False)
            return

        self.__verify_pick(pick,data)
        self.__cleanup_pick(pick,week,game,player)

    def test_delete_pick_by_id(self):
        pick,week,game,player = self.__setup_pick(1984,1,"Player1")

        try:
            self.fbpool.deletePickByID(pick['id'])
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            self.assertTrue(False)
            return

        self.assertFalse(self.__does_pick_exist(pick['id']))
        self.__cleanup_pick(week=week,game=game,player=player)

    def test_delete_pick_by_key(self):
        pick,week,game,player = self.__setup_pick(1984,1,"Player1")

        try:
            self.fbpool.deletePickByKey(pick['key'])
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            self.assertTrue(False)
            return

        self.assertFalse(self.__does_pick_exist(pick['id']))
        self.__cleanup_pick(week=week,game=game,player=player)

    def test_delete_all_picks(self):
        try:
            self.fbpool.deleteAllPicks()
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            self.assertTrue(False)
            return

        game = self.__setup_game(1)
        week = self.__setup_week(1980,1,game)
        player1 = self.__setup_player("Player1",1980)
        player2 = self.__setup_player("Player2",1980)
        player3 = self.__setup_player("Player3",1980)

        pick1 = self.__setup_pick_only(week,player1,game)
        pick2 = self.__setup_pick_only(week,player2,game)
        pick3 = self.__setup_pick_only(week,player3,game)

        try:
            self.fbpool.deleteAllPicks()
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            self.assertTrue(False)
            return

        self.assertFalse(self.__does_pick_exist(pick1['id']))
        self.assertFalse(self.__does_pick_exist(pick2['id']))
        self.assertFalse(self.__does_pick_exist(pick3['id']))

        self.__cleanup_pick(week=week,game=game)
        self.__cleanup_pick(player=player1)
        self.__cleanup_pick(player=player2)
        self.__cleanup_pick(player=player3)

    def test_get_pick_by_id(self):
        pick,week,game,player = self.__setup_pick(1984,1,"Player1")

        try:
            pick_get = self.fbpool.getPickByID(pick['id'])
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            self.assertTrue(False)
            return

        self.__verify_pick(pick_get,pick)
        self.__cleanup_pick(pick,week,game,player)

    def test_get_pick_by_key(self):
        pick,week,game,player = self.__setup_pick(1984,1,"Player1")

        try:
            pick_get = self.fbpool.getPickByKey(pick['key'])
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            self.assertTrue(False)
            return

        self.__verify_pick(pick_get,pick)
        self.__cleanup_pick(pick,week,game,player)

    def test_get_week_picks(self):
        try:
            self.fbpool.deleteAllPicks()
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            self.assertTrue(False)
            return

        game1 = self.__setup_game(1)
        game2 = self.__setup_game(2)
        week1 = self.__setup_week(1980,1,game1)
        week2 = self.__setup_week(1980,2,game2)
        player1 = self.__setup_player("Player1",1980)
        player2 = self.__setup_player("Player2",1980)
        player3 = self.__setup_player("Player3",1980)

        pick1 = self.__setup_pick_only(week1,player1,game1)
        pick2 = self.__setup_pick_only(week1,player2,game1)
        pick3 = self.__setup_pick_only(week1,player3,game1)
        pick4 = self.__setup_pick_only(week2,player3,game2)

        try:
            picks = self.fbpool.getWeekPicks(year=1980,week_number=1)
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            self.assertTrue(False)
            return

        pick_ids = sorted([ pick['id'] for pick in picks ])
        expected = sorted([ pick1['id'], pick2['id'], pick3['id']])

        self.assertEquals(pick_ids,expected)

        self.__cleanup_pick(week=week1,game=game1)
        self.__cleanup_pick(week=week2,game=game2)
        self.__cleanup_pick(player=player1)
        self.__cleanup_pick(player=player2)
        self.__cleanup_pick(player=player3)


    def test_get_player_picks(self):
        try:
            self.fbpool.deleteAllPicks()
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            self.assertTrue(False)
            return

        game1 = self.__setup_game(1)
        game2 = self.__setup_game(2)
        week1 = self.__setup_week(1980,1,game1)
        week2 = self.__setup_week(1980,2,game2)
        player1 = self.__setup_player("Player1",1980)
        player2 = self.__setup_player("Player2",1980)

        pick1 = self.__setup_pick_only(week1,player1,game1)
        pick2 = self.__setup_pick_only(week1,player2,game1)
        pick3 = self.__setup_pick_only(week1,player2,game1)
        pick4 = self.__setup_pick_only(week2,player2,game2)

        try:
            picks = self.fbpool.getPlayerPicks(year=1980,week_number=1,player="Player2")
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            self.assertTrue(False)
            return

        pick_ids = sorted([ pick['id'] for pick in picks ])
        expected = sorted([ pick2['id'], pick3['id']])

        self.assertEquals(pick_ids,expected)

        self.__cleanup_pick(week=week1,game=game1)
        self.__cleanup_pick(week=week2,game=game2)
        self.__cleanup_pick(player=player1)
        self.__cleanup_pick(player=player2)

    def test_edit_pick_by_id(self):
        pick,week,game,player = self.__setup_pick(1984,1,"Player1")

        data = dict()
        data['week'] = week['key']
        data['player'] = player['key']
        data['game'] = game['key']
        data['winner'] = "team2"
        data['team1_score'] = 33
        data['team2_score'] = 30

        try:
            self.fbpool.editPickByID(pick['id'],data)
            pick_edit = self.fbpool.getPickByID(pick['id'])
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            self.assertTrue(False)
            return

        self.__verify_pick(pick_edit,data)
        self.__cleanup_pick(pick,week,game,player)


    def test_edit_pick_by_key(self):
        pick,week,game,player = self.__setup_pick(1984,1,"Player1")

        data = dict()
        data['week'] = week['key']
        data['player'] = player['key']
        data['game'] = game['key']
        data['winner'] = "team2"
        data['team1_score'] = 33
        data['team2_score'] = 30

        try:
            self.fbpool.editPickByKey(pick['id'],data)
            pick_edit = self.fbpool.getPickByID(pick['id'])
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            self.assertTrue(False)
            return

        self.__verify_pick(pick_edit,data)
        self.__cleanup_pick(pick,week,game,player)


    def test_delete_picks_cache(self):
        try:
            self.fbpool.deletePicksCache()
        except FBAPIException as e:
            print e
            self.assertTrue(False)
            return

    def __setup_pick(self,year=1984,week_number=1,player="Player1"):
        week,game,player = self.__setup_pick_data(year,week_number,player)

        data = dict()
        data['week'] = week['key']
        data['player'] = player['key']
        data['game'] = game['key']
        data['winner'] = "team1"
        data['team1_score'] = None
        data['team2_score'] = None

        try:
            pick = self.fbpool.createPick(data)
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            self.assertTrue(False)
            return

        return pick,week,game,player

    def __setup_pick_only(self,week,player,game):
        data = dict()
        data['week'] = week['key']
        data['player'] = player['key']
        data['game'] = game['key']
        data['winner'] = "team1"
        data['team1_score'] = None
        data['team2_score'] = None

        try:
            pick = self.fbpool.createPick(data)
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            self.assertTrue(False)
            return

        return pick

    def __setup_pick_data(self,year,week_number,player,game_number=1):
        try:
            self.fbpool.deleteWeekIfExists(year=year,week_number=week_number)
            self.fbpool.deletePlayerIfExists(player)

            game = self.__create_test_game(game_number)
            week = self.__create_test_week(year,week_number,[game['key']])
            player = self.__create_test_player(player,year)

        except FBAPIException as e:
            print e
            self.assertTrue(False)
            return
        return week,game,player

    def __setup_player(self,name,year):
        try:
            self.fbpool.deletePlayerIfExists(name)
            player = self.__create_test_player(name,year)
        except FBAPIException as e:
            print e
            self.assertTrue(False)
            return
        return player

    def __setup_game(self,game_number):
        try:
            game = self.__create_test_game(game_number)
        except FBAPIException as e:
            print e
            self.assertTrue(False)
            return
        return game

    def __setup_week(self,year,week_number,game):
        try:
            self.fbpool.deleteWeekIfExists(year=year,week_number=week_number)
            week = self.__create_test_week(year,week_number,[game['key']])
        except FBAPIException as e:
            print e
            self.assertTrue(False)
            return
        return week


    def __cleanup_pick(self,pick=None,week=None,game=None,player=None):
        try:
            if pick != None:
                self.fbpool.deletePickByID(pick['id'])

            if week != None:
                self.fbpool.deleteWeekByID(week['id'])

            if game != None:
                self.fbpool.deleteGameByID(game['id'])

            if player != None:
                self.fbpool.deletePlayerByID(player['id'])

        except FBAPIException as e:
            print e
            self.assertTrue(False)
            return

    def __create_test_week(self,year,number,games=[]):
        data = dict()
        data['year'] = year
        data['number'] = number
        data['winner'] = None
        data['games'] = games
        data['lock_picks'] = None
        data['lock_scores'] = None
        return self.fbpool.createWeek(data)

    def __create_test_player(self,name,year):
        return self.fbpool.createPlayer(name,[year])

    def __create_test_game(self,number):
        data = dict()
        data['number'] = number
        data['team1'] = ""
        data['team2'] = ""
        data['team1_score'] = 0
        data['team2_score'] = 0
        data['favored'] = "team1"
        data['spread'] = 0.5
        data['state'] = "not_started"
        data['quarter'] = ""
        data['time_left'] = ""
        data['date'] = None
        return self.fbpool.createGame(data)

    def __verify_pick(self,pick,expected):
        self.assertIn('id',pick)
        self.assertIn('key',pick)

        fields = [ 'week', 'player', 'game', 'winner', 'team1_score', 'team2_score' ]
        for field in fields:
            self.assertIn(field,pick)

        for field in fields:
            self.assertEquals(pick[field],expected[field])

    def __does_pick_exist(self,pick_id):
        try:
            pick = self.fbpool.getPickByID(pick_id)
            return True
        except FBAPIException as e:
            if e.http_code != 404 or e.errmsg != "could not find pick":
                return False
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            self.assertTrue(False)
            return
        raise AssertionError


if __name__ == "__main__":
    unittest.main()
