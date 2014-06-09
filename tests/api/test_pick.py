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

        self.assertFalse(self.__does_pick_exist(pick['id'])
        self.__cleanup_pick(pick,week,game,player)

    def test_delete_pick_by_key(self):
        pass

    def test_delete_all_picks(self):
        pass

    def test_get_pick_by_id(self):
        pass

    def test_get_pick_by_key(self):
        pass

    def test_get_week_picks(self):
        pass

    def test_get_player_picks(self):
        pass

    def test_edit_pick_by_id(self):
        pass

    def test_edit_pick_by_key(self):
        pass

    def __setup_pick(self):
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

        return pick,week,game,player

    def __setup_pick_data(self,year,week_number,player,game_number=1):
        try:
            self.fbpool.deleteWeekIfExists(year=year,week_number=week_number)
            self.fbpool.deletePlayerIfExists(player)

            game = self.__create_test_game(game_number)
            week = self.__create_test_week(year,week_number,[game])
            player = self.__create_test_player(player,year)

        except FBAPIException as e:
            print e
            self.assertTrue(False)
            return
        return week,game,player

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
        self.assertIn('id',week)
        self.assertIn('key',week)

        fields = [ 'week', 'player', 'game', 'winner', 'team1_score', 'team2_score' ]
        for field in fields:
            self.assertIn(field,pick)

        for field in fields:
            self.assertEquals(pick[field],expected[field])

    def __does_pick_exist(self,pick_id):
        try:
            pick = self.fbpool.getPickByID(pick['id'])
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
