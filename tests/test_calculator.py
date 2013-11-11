from code.update import *
from code.calculator import *
from code.database import *
from models.games import *

import unittest

class TestCalculator(unittest.TestCase):

    def __load_test_week(self):
        database = Database()
        week,games,picks = database.load_week_data(2013,1)
        self.calc = CalculateResults(week,games,picks)
        self.week = week
        self.games = games
        self.picks = picks

    def setUp(self):
        self.__load_test_week()

    def test_t1_get_team_player_picked_to_win(self):
        self.__t1_invalid_player_name()
        self.__t1_game_missing()
        self.__t1_home_winner()
        self.__t1_away_winner()

    def test_t2_get_team_name_player_picked_to_win(self):
        #self.__t2_invalid_player_name()
        #self.__t2_game_missing()
        #self.__t2_home_winner()
        #self.__t2_away_winner()
        pass

    def test_t3_is_home_team_winning_pool(self):
        #self.__t3_bad_game_favored_value()
        #self.__t3_home_team_ahead()
        #self.__t3_away_team_ahead()
        #self.__t3_home_team_ahead_in_pool_behind_in_game()
        #self.__t3_away_team_ahead_in_pool_behind_in_game()
        #self.__t3_home_team_ahead_boundary_case()
        #self.__t3_away_team_ahead_boundary_case()
        pass

    def test_t2_is_away_team_winning_pool(self):
        pass

    def __t1_invalid_player_name(self):
        with self.assertRaises(AssertionError):
            self.calc.get_team_player_picked_to_win("playerxxx",self.games[0])

    def __t1_game_missing(self):
        with self.assertRaises(AssertionError):
            self.calc.get_team_player_picked_to_win("Brent H.",None)

    def __t1_home_winner(self):
        game = self.__find_game("North Carolina","South Carolina")
        team = self.get_team_player_picked_to_win("Brent H.",game)
        self.assertEqual(team,"home")

    def __t1_away_winner(self):
        game = self.__find_game("LSU","TCU")
        team = self.get_team_player_picked_to_win("Brent H.",game)
        self.assertEqual(team,"away")

    def __find_game(self,away_team,home,team):
        for g in self.games:
            same_teams = away_team == g.away_team.name and home_team == g.home_team.name
            if same_teams:
                return g
        raise AssertionError, "Could not find game"

    def __t2_invalid_player_name(self):
        with self.assertRaises(AssertionError):
            self.calc.get_team_name_player_picked_to_win("playerxxx",self.games[0])

    def __t2_game_missing(self):
        with self.assertRaises(AssertionError):
            self.calc.get_team_name_player_picked_to_win("Brent H.",None)

    def __t2_home_winner(self):
        game = self.__find_game("North Carolina","South Carolina")
        team = self.get_team_name_player_picked_to_win("Brent H.",game)
        self.assertEqual(team,"South Carolina")

    def __t2_away_winner(self):
        game = self.__find_game("LSU","TCU")
        team = self.get_team_name_player_picked_to_win("Brent H.",game)
        self.assertEqual(team,"LSU")

    def __t3_bad_game_favored_value(self):
        g = Game()
        g.home_score = 0
        g.away_score = 0
        g.favored = "bad value"
        g.spread = 0.5
        with self.assertRaises(AssertionError):
            self.calc.is_home_team_winning_pool(g)

    def __t3_home_team_ahead(self):
        g = Game()
        g.home_score = 20 
        g.away_score = 10 
        g.favored = "home"
        g.spread = 5.5 
        self.assertTrue(self.calc.is_home_team_winning_pool(g))

    def __t3_away_team_ahead(self):
        g = Game()
        g.home_score = 10 
        g.away_score = 35 
        g.favored = "away"
        g.spread = 10.5 
        self.assertFalse(self.calc.is_home_team_winning_pool(g))

    def __t3_home_team_ahead_in_pool_behind_in_game(self):
        g = Game()
        g.home_score = 14 
        g.away_score = 17 
        g.favored = "away"
        g.spread = 3.5 
        self.assertTrue(self.calc.is_home_team_winning_pool(g))

    def __t3_away_team_ahead_in_pool_behind_in_game(self):
        g = Game()
        g.home_score = 17 
        g.away_score = 14 
        g.favored = "home"
        g.spread = 3.5 
        self.assertFalse(self.calc.is_home_team_winning_pool(g))

    def __t3_home_team_ahead_boundary_case(self):
        g = Game()
        g.home_score = 17 
        g.away_score = 16 
        g.favored = "home"
        g.spread = 0.5 
        self.assertTrue(self.calc.is_home_team_winning_pool(g))

    def __t3_away_team_ahead_boundary_case(self):
        g = Game()
        g.home_score = 16 
        g.away_score = 17 
        g.favored = "away"
        g.spread = 0.5 
        self.assertFalse(self.calc.is_home_team_winning_pool(g))


