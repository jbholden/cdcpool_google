import logging
import unittest
from code.database import *

class TestWeekData(unittest.TestCase):

    def setUp(self):
        database = Database()
        self.week_data = database.load_week_data(2013,1)

    def test_week_data_structure(self):
        self.assertIsNotNone(self.week_data.week)
        self.assertIsNotNone(self.week_data.games)
        self.assertIsNotNone(self.week_data.player_picks)
        self.assertIsNotNone(self.week_data.picks)
        self.assertIsNotNone(self.week_data.players)

    def test_get_game(self):
        self.__test_game_none()
        self.__test_game_key_invalid()
        self.__test_game_key_valid()

    def test_get_pick(self):
        self.__test_pick_none()
        self.__test_pick_key_invalid()
        self.__test_pick_key_valid()

    def test_get_team(self):
        self.__test_team_none()
        self.__test_team_key_invalid()
        self.__test_team_key_valid()

    def test_get_player(self):
        self.__test_player_none()
        self.__test_player_key_invalid()
        self.__test_player_key_valid()

    def test_get_player_key(self):
        self.__test_player_name_none()
        self.__test_player_name_missing()
        self.__test_player_name_valid()

    def test_get_player_picks(self):
        self.__test_player_picks_none()
        self.__test_player_picks_key_invalid()
        self.__test_player_picks_key_valid()

    def test_get_player_name_picks(self):
        self.__test_player_picks_name_none()
        self.__test_player_picks_name_invalid()
        self.__test_player_picks_name_valid()

    def test_get_team1_name(self):
        self.__test_team1_name_game_none()
        self.__test_team1_name_game_key_invalid()
        self.__test_team1_name()

    def test_get_team2_name(self):
        self.__test_team2_name_game_none()
        self.__test_team2_name_game_key_invalid()
        self.__test_team2_name()

    def __test_game_none(self):
        with self.assertRaises(Exception):
            game = self.week_data.get_game(None)

    def __test_game_key_invalid(self):
        with self.assertRaises(Exception):
            game = self.week_data.get_game("bad key")

    def __test_game_key_valid(self):
        valid_key = self.week_data.games.keys()[0]
        game = self.week_data.get_game(valid_key)
        self.assertIsNotNone(game)
        self.assertEqual(game.kind(),"Game")

    def __test_pick_none(self):
        with self.assertRaises(Exception):
            pick = self.week_data.get_pick(None)

    def __test_pick_key_invalid(self):
        with self.assertRaises(Exception):
            pick = self.week_data.get_pick("bad key")

    def __test_pick_key_valid(self):
        valid_key = self.week_data.picks.keys()[0]
        pick = self.week_data.get_pick(valid_key)
        self.assertIsNotNone(pick)
        self.assertEqual(pick.kind(),"Pick")

    def __test_team_none(self):
        with self.assertRaises(Exception):
            team = self.week_data.get_team(None)

    def __test_team_key_invalid(self):
        with self.assertRaises(Exception):
            team = self.week_data.get_team("bad key")

    def __test_team_key_valid(self):
        valid_key = self.week_data.teams.keys()[0]
        team = self.week_data.get_team(valid_key)
        self.assertIsNotNone(team)
        self.assertEqual(team.kind(),"Team")

    def __test_player_none(self):
        with self.assertRaises(Exception):
            player = self.week_data.get_player(None)

    def __test_player_key_invalid(self):
        with self.assertRaises(Exception):
            player = self.week_data.get_player("bad key")

    def __test_player_key_valid(self):
        valid_key = self.week_data.players.keys()[0]
        player = self.week_data.get_player(valid_key)
        self.assertIsNotNone(player)
        self.assertEqual(player.kind(),"Player")

    def __test_player_name_none(self):
        with self.assertRaises(Exception):
            player = self.week_data.get_player_key(None)

    def __test_player_name_missing(self):
        with self.assertRaises(Exception):
            player = self.week_data.get_player_key("bad player name")

    def __test_player_name_valid(self):
        player_key = self.week_data.get_player_key("Brent H.")
        self.assertIsNotNone(player_key)
        player = self.week_data.get_player(player_key)
        self.assertEquals(player.name,"Brent H.")

    def __test_player_picks_none(self):
        with self.assertRaises(Exception):
            picks = self.week_data.get_player_picks(None)

    def __test_player_picks_key_invalid(self):
        with self.assertRaises(Exception):
            picks = self.week_data.get_player_picks("bad key")

    def __test_player_picks_key_valid(self):
        player_key = self.week_data.get_player_key("Brent H.")
        picks = self.week_data.get_player_picks(player_key)
        self.assertIsNotNone(picks)
        self.assertEqual(len(picks),10)
        for pick in picks:
            self.assertEqual(pick.kind(),"Pick")

    def __test_player_picks_name_none(self):
        with self.assertRaises(Exception):
            picks = self.week_data.get_player_name_picks(None)

    def __test_player_picks_name_invalid(self):
        with self.assertRaises(Exception):
            picks = self.week_data.get_player_name_picks("bad key")

    def __test_player_picks_name_valid(self):
        picks = self.week_data.get_player_name_picks("Brent H.")
        self.assertIsNotNone(picks)
        self.assertEqual(len(picks),10)
        for pick in picks:
            self.assertEqual(pick.kind(),"Pick")

    def __test_team1_name_game_none(self):
        with self.assertRaises(Exception):
            game = self.week_data.get_team1_name(None)

    def __test_team1_name_game_key_invalid(self):
        with self.assertRaises(Exception):
            game = self.week_data.get_team1_name("bad key")

    def __test_team1_name(self):
        game_key = self.__find_game_key("North Carolina","South Carolina")
        team = self.week_data.get_team1_name(game_key)
        self.assertEqual(team,"North Carolina")

    def __test_team2_name_game_none(self):
        with self.assertRaises(Exception):
            game = self.week_data.get_team2_name(None)

    def __test_team2_name_game_key_invalid(self):
        with self.assertRaises(Exception):
            game = self.week_data.get_team2_name("bad key")

    def __test_team2_name(self):
        game_key = self.__find_game_key("North Carolina","South Carolina")
        team = self.week_data.get_team2_name(game_key)
        self.assertEqual(team,"South Carolina")

    def __find_game_key(self,team1,team2):
        for game_key in self.week_data.games:
            game = self.week_data.games.get(game_key)
            game_team1 = self.week_data.teams.get(game.team1)
            game_team2 = self.week_data.teams.get(game.team2)

            same_teams = team1 == game_team1.name and team2 == game_team2.name
            if same_teams:
                return game_key
        raise AssertionError, "Could not find game"
