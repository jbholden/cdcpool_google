ROOT_PATH = '../../.'
import sys
sys.path.append(ROOT_PATH)

import unittest
import socket
import logging
from scripts.api.fbpool_api import *
from scripts.api.fbpool_api_exception import *


class TestWeek(unittest.TestCase):

    def setUp(self):
        url = "http://localhost:10090"
        self.fbpool = FBPoolAPI(url=url)

    def test_create_week(self):
        data = dict()
        data['year'] = 1980
        data['number'] = 1
        data['winner'] = None
        data['games'] = []
        data['lock_picks'] = None
        data['lock_scores'] = None

        try:
            self.fbpool.deleteWeekIfExists(year=1980,week_number=1)
            week = self.fbpool.createWeek(data)
            self.fbpool.deleteWeekByID(week['id'])
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            self.assertTrue(False)
            return

        self.__verify_week(week,data)

    def test_create_week_2(self):
        # setup info for week
        try:
            self.fbpool.deletePlayerIfExists("Player1")
            winner = self.fbpool.createPlayer("Player1",[1980])
            self.fbpool.deleteAllGames()
            game_keys = self.__create_10_test_games()
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            self.assertTrue(False)
            return

        data = dict()
        data['year'] = 1980
        data['number'] = 1
        data['winner'] = winner['key']
        data['games'] = game_keys
        data['lock_picks'] = "05/05/2014 19:00"
        data['lock_scores'] = "05/10/2014 21:00"

        try:
            self.fbpool.deleteWeekIfExists(year=1980,week_number=1)
            week = self.fbpool.createWeek(data)
            self.fbpool.deleteWeekByID(week['id'])
            self.fbpool.deletePlayerByID(winner['id'])
            for game_key in game_keys:
                self.fbpool.deleteGameByKey(game_key)
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            self.assertTrue(False)
            return

        self.__verify_week(week,data)

    def test_create_existing_week(self):
        data = dict()
        data['year'] = 1980
        data['number'] = 1
        data['winner'] = None
        data['games'] = []
        data['lock_picks'] = None
        data['lock_scores'] = None

        try:
            self.fbpool.deleteWeekIfExists(year=1980,week_number=1)
            week = self.fbpool.createWeek(data)
            week_again = self.fbpool.createWeek(data)
        except FBAPIException as e:
            if e.http_code != 409 or e.errmsg != "week already exists":
                print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
                self.assertTrue(False)
                return

        try:
            self.fbpool.deleteWeekByID(week['id'])
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            self.assertTrue(False)
            return

    def test_get_week_by_key(self):
        try:
            self.fbpool.deleteWeekIfExists(year=1978,week_number=1)
            created_week = self.__create_test_week(1978,1)
            week = self.fbpool.getWeekByKey(created_week['key'])
            self.fbpool.deleteWeekByID(created_week['id'])
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            self.assertTrue(False)
            return

        self.__verify_week(week,created_week)

    def test_get_week_by_id(self):
        try:
            self.fbpool.deleteWeekIfExists(year=1978,week_number=1)
            created_week = self.__create_test_week(1978,1)
            week = self.fbpool.getWeekByID(created_week['id'])
            self.fbpool.deleteWeekByID(created_week['id'])
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            self.assertTrue(False)
            return

        self.__verify_week(week,created_week)

    def test_get_all_weeks(self):
        try:
            self.fbpool.deleteAllWeeks()
            week_1980_1 = self.__create_test_week(1980,1)
            week_1980_2 = self.__create_test_week(1980,2)
            week_1980_3 = self.__create_test_week(1980,3)
            week_1981_1 = self.__create_test_week(1981,1)
            week_1981_2 = self.__create_test_week(1981,2)
            week_1981_3 = self.__create_test_week(1981,3)
            weeks = self.fbpool.getAllWeeks()
            self.fbpool.deleteAllWeeks()
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            self.assertTrue(False)
            return

        week_keys = sorted([ week['key'] for week in weeks ])
        expected = []
        expected.append(week_1980_1['key'])
        expected.append(week_1980_2['key'])
        expected.append(week_1980_3['key'])
        expected.append(week_1981_1['key'])
        expected.append(week_1981_2['key'])
        expected.append(week_1981_3['key'])
        expected.sort()

        self.assertEquals(week_keys,expected)

    def test_get_weeks_in_year(self):
        try:
            self.fbpool.deleteAllWeeks()
            week_1980_1 = self.__create_test_week(1980,1)
            week_1980_2 = self.__create_test_week(1980,2)
            week_1980_3 = self.__create_test_week(1980,3)
            week_1981_1 = self.__create_test_week(1981,1)
            week_1981_2 = self.__create_test_week(1981,2)
            week_1981_3 = self.__create_test_week(1981,3)
            weeks = self.fbpool.getWeeksInYear(year=1981)
            self.fbpool.deleteAllWeeks()
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            self.assertTrue(False)
            return

        week_keys = sorted([ week['key'] for week in weeks ])
        expected = []
        expected.append(week_1981_1['key'])
        expected.append(week_1981_2['key'])
        expected.append(week_1981_3['key'])
        expected.sort()

        self.assertEquals(week_keys,expected)

    def test_get_week_by_year_and_number(self):
        try:
            self.fbpool.deleteAllWeeks()
            week_1980_1 = self.__create_test_week(1980,1)
            week_1980_2 = self.__create_test_week(1980,2)
            week_1980_3 = self.__create_test_week(1980,3)
            week_1981_1 = self.__create_test_week(1981,1)
            week_1981_2 = self.__create_test_week(1981,2)
            week_1981_3 = self.__create_test_week(1981,3)
            week = self.fbpool.getWeek(year=1980,week_number=3)
            self.fbpool.deleteAllWeeks()
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            self.assertTrue(False)
            return

        self.__verify_week(week,week_1980_3)

    def test_delete_week_by_key(self):
        try:
            self.fbpool.deleteWeekIfExists(year=1980,week_number=1)
            week = self.__create_test_week(1980,1)
            self.fbpool.deleteWeekByKey(week['key'])
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            self.assertTrue(False)
            return

        try:
            week = self.fbpool.getWeekByID(week['id'])
            self.assertTrue(False)
        except FBAPIException as e:
            if e.http_code != 404 or e.errmsg != "could not find week":
                self.assertTrue(False)
                return

    def test_delete_week_by_id(self):
        try:
            self.fbpool.deleteWeekIfExists(year=1980,week_number=1)
            week = self.__create_test_week(1980,1)
            self.fbpool.deleteWeekByID(week['id'])
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            self.assertTrue(False)
            return

        try:
            week = self.fbpool.getWeekByID(week['id'])
            self.assertTrue(False)
        except FBAPIException as e:
            if e.http_code != 404 or e.errmsg != "could not find week":
                self.assertTrue(False)
                return

    def test_delete_all_weeks(self):
        try:
            self.fbpool.deleteAllWeeks()
            week_1980_1 = self.__create_test_week(1980,1)
            week_1980_2 = self.__create_test_week(1980,2)
            week_1980_3 = self.__create_test_week(1980,3)
            week_1981_1 = self.__create_test_week(1981,1)
            week_1981_2 = self.__create_test_week(1981,2)
            week_1981_3 = self.__create_test_week(1981,3)
            self.fbpool.deleteAllWeeks()
            weeks = self.fbpool.getAllWeeks()
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            self.assertTrue(False)
            return

        self.assertEquals(len(weeks),0)

    def test_edit_week_by_id(self):
        try:
            self.fbpool.deletePlayerIfExists("Player1")
            winner = self.fbpool.createPlayer("Player1",[1980,1981])
            self.fbpool.deleteAllGames()
            game_keys = self.__create_10_test_games()
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            self.assertTrue(False)
            return

        edit = dict()
        edit['year'] = 1981
        edit['number'] = 2 
        edit['winner'] = winner['key']
        edit['games'] = game_keys
        edit['lock_picks'] = "05/05/2014 19:00"
        edit['lock_scores'] = "05/10/2014 21:00"

        try:
            self.fbpool.deleteWeekIfExists(year=1980,week_number=1)
            self.fbpool.deleteWeekIfExists(year=1981,week_number=2)
            week = self.__create_test_week(1980,1)
            self.fbpool.editWeekByID(week['id'],edit)
            edited_week = self.fbpool.getWeekByID(week['id'])

            # cleanup
            self.fbpool.deleteWeekByID(week['id'])
            self.fbpool.deletePlayerByID(winner['id'])
            for game_key in game_keys:
                self.fbpool.deleteGameByKey(game_key)

        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            self.assertTrue(False)
            return

        self.__verify_week(edited_week,edit)

    def test_edit_week_by_key(self):
        try:
            self.fbpool.deletePlayerIfExists("Player1")
            winner = self.fbpool.createPlayer("Player1",[1980,1981])
            self.fbpool.deleteAllGames()
            game_keys = self.__create_10_test_games()
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            self.assertTrue(False)
            return

        edit = dict()
        edit['year'] = 1981
        edit['number'] = 2 
        edit['winner'] = winner['key']
        edit['games'] = game_keys
        edit['lock_picks'] = "05/05/2014 19:00"
        edit['lock_scores'] = "05/10/2014 21:00"

        try:
            self.fbpool.deleteWeekIfExists(year=1980,week_number=1)
            self.fbpool.deleteWeekIfExists(year=1981,week_number=2)
            week = self.__create_test_week(1980,1)
            self.fbpool.editWeekByKey(week['key'],edit)
            edited_week = self.fbpool.getWeekByID(week['id'])

            # cleanup
            self.fbpool.deleteWeekByID(week['id'])
            self.fbpool.deletePlayerByID(winner['id'])
            for game_key in game_keys:
                self.fbpool.deleteGameByKey(game_key)

        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            self.assertTrue(False)
            return

        self.__verify_week(edited_week,edit)

    def test_edit_week_to_one_already_existing(self):
        edit = dict()
        edit['year'] = 1981
        edit['number'] = 2 
        edit['winner'] = None
        edit['games'] = None
        edit['lock_picks'] = "05/05/2014 19:00"
        edit['lock_scores'] = "05/10/2014 21:00"

        try:
            self.fbpool.deleteWeekIfExists(year=1980,week_number=1)
            self.fbpool.deleteWeekIfExists(year=1981,week_number=2)
            week_1980_1 = self.__create_test_week(1980,1)
            week_1981_2 = self.__create_test_week(1981,2)
            self.fbpool.editWeekByID(week_1980_1['id'],edit)
            self.assertTrue(False)
        except FBAPIException as e:
            if e.http_code != 409 or e.errmsg != "week already exists":
                self.assertTrue(False)
                return

        try:
            self.fbpool.deleteWeekByID(week_1980_1['id'])
            self.fbpool.deleteWeekByID(week_1981_2['id'])
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            self.assertTrue(False)
            return

    def __verify_week(self,week,expected):
        self.assertIn('id',week)
        self.assertIn('key',week)

        fields = [ 'year', 'number', 'winner', 'games', 'lock_picks', 'lock_scores' ]
        for field in fields:
            self.assertIn(field,week)

        for field in fields:
            if field != "games":
                self.assertEquals(week[field],expected[field])

        self.assertEquals(len(week['games']),len(expected['games']))
        week_games = sorted(week['games'])
        expected_games = sorted(expected['games'])
        for i in range(len(week_games)):
            self.assertEquals(str(week_games[i]),str(expected_games[i]))


    def __create_test_week(self,year,number):
        data = dict()
        data['year'] = year
        data['number'] = number
        data['winner'] = None
        data['games'] = []
        data['lock_picks'] = None
        data['lock_scores'] = None
        return self.fbpool.createWeek(data)

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

    def __create_10_test_games(self):
        game1 = self.__create_test_game(1)
        game2 = self.__create_test_game(2)
        game3 = self.__create_test_game(3)
        game4 = self.__create_test_game(4)
        game5 = self.__create_test_game(5)
        game6 = self.__create_test_game(6)
        game7 = self.__create_test_game(7)
        game8 = self.__create_test_game(8)
        game9 = self.__create_test_game(9)
        game10 = self.__create_test_game(10)

        games = []
        games.append(game1['key'])
        games.append(game2['key'])
        games.append(game3['key'])
        games.append(game4['key'])
        games.append(game5['key'])
        games.append(game6['key'])
        games.append(game7['key'])
        games.append(game8['key'])
        games.append(game9['key'])
        games.append(game10['key'])

        return games


if __name__ == "__main__":
    unittest.main()
