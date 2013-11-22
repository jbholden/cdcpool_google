from code.update import *
from code.calculator import *
from code.database import *
from models.games import *
import time
import logging
import unittest

class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.__load_test_data()

    def __load_test_data(self):
        database = Database()

        self.teams = database.load_teams()

        week,games,picks = database.load_week_data(2013,1)
        self.calc = CalculateResults(week,games,picks)
        self.week = week
        self.games = games
        self.picks = picks

        week2,games2,picks2 = database.load_week_data(2013,2)
        self.week2 = week2
        self.games2 = games2
        self.picks2 = picks2

    # function name decode:  
    # test_ : each function to test must start with test_ (unittest requirement)
    # _t<number>_ : unique identifier used to specify this test function
    # _<name> : this is the name of the function in calculator.py that is being tested
    def test_t1_get_team_player_picked_to_win(self):
        self.__t1_invalid_player_name()
        self.__t1_invalid_game()
        self.__t1_game_none()
        self.__t1_team1_winner()
        self.__t1_team2_winner()

    def test_t2_get_team_name_player_picked_to_win(self):
        self.__t2_invalid_player_name()
        self.__t2_invalid_game()
        self.__t2_game_none()
        self.__t2_team1_winner()
        self.__t2_team2_winner()


    def test_t3_is_team1_winning_pool(self):
        self.__t3_bad_game_favored_value()
        self.__t3_team1_ahead()
        self.__t3_team1_behind()
        self.__t3_team1_ahead_in_pool_behind_in_game()
        self.__t3_team1_behind_in_pool_ahead_in_game()
        self.__t3_team1_boundary_case1()
        self.__t3_team1_boundary_case2()
        self.__t3_team1_boundary_case3()
        self.__t3_team1_boundary_case4()


    def test_t4_is_team2_winning_pool(self):
        self.__t4_bad_game_favored_value()
        self.__t4_team2_ahead()
        self.__t4_team2_behind()
        self.__t4_team2_ahead_in_pool_behind_in_game()
        self.__t4_team2_behind_in_pool_ahead_in_game()
        self.__t4_team2_boundary_case1()
        self.__t4_team2_boundary_case2()
        self.__t4_team2_boundary_case3()
        self.__t4_team2_boundary_case4()

    def test_t5_get_pool_game_winner(self):
        self.__t5_game_none()
        self.__t5_game_in_progress()
        self.__t5_game_not_started()
        self.__t5_team1_won()
        self.__t5_team2_won()

    def test_t6_get_pool_game_winner_team_name(self):
        self.__t6_game_none()
        self.__t6_game_in_progress()
        self.__t6_game_not_started()
        self.__t6_team1_won()
        self.__t6_team2_won()

    def test_t7_get_game_winner(self):
        self.__t7_game_none()
        self.__t7_game_in_progress()
        self.__t7_game_not_started()
        self.__t7_same_score()
        self.__t7_team1_won()
        self.__t7_team2_won()
        self.__t7_team1_won_but_not_favored()
        self.__t7_team2_won_but_not_favored()

    def test_t8_get_game_winner_team_name(self):
        self.__t8_game_none()
        self.__t8_game_in_progress()
        self.__t8_game_not_started()
        self.__t8_same_score()
        self.__t8_team1_won()
        self.__t8_team2_won()

    def test_t9_get_team_winning_pool_game(self):
        self.__t9_game_none()
        self.__t9_game_final()
        self.__t9_game_not_started()
        self.__t9_same_score()
        self.__t9_team1_ahead()
        self.__t9_team2_ahead()

    def test_t10_get_team_name_winning_pool_game(self):
        self.__t10_game_none()
        self.__t10_game_final()
        self.__t10_game_not_started()
        self.__t10_same_score()
        self.__t10_team1_ahead()
        self.__t10_team2_ahead()

    def test_t11_get_team_winning_game(self):
        self.__t11_game_none()
        self.__t11_game_final()
        self.__t11_game_not_started()
        self.__t11_same_score()
        self.__t11_team1_ahead()
        self.__t11_team2_ahead()

    def test_t12_get_team_name_winning_game(self):
        self.__t12_game_none()
        self.__t12_game_final()
        self.__t12_game_not_started()
        self.__t12_same_score()
        self.__t12_team1_ahead()
        self.__t12_team2_ahead()

    def test_t13_player_did_not_pick(self):
        self.__t13_game_none()
        self.__t13_invalid_player_name()
        self.__t13_player_missing_all_week_picks()
        self.__t13_player_missing_pick_for_game()
        self.__t13_player_missing_pick_winner()
        self.__t13_player_made_pick()

    def __t1_invalid_player_name(self):
        with self.assertRaises(AssertionError):
            self.calc.get_team_player_picked_to_win("playerxxx",self.games[0])

    def __t1_invalid_game(self):
        invalid_game = self.games2[0]
        with self.assertRaises(AssertionError):
            self.calc.get_team_player_picked_to_win("Brent H.",invalid_game)

    def __t1_game_none(self):
        with self.assertRaises(AssertionError):
            self.calc.get_team_player_picked_to_win("Brent H.",None)

    def __t1_team2_winner(self):
        game = self.__find_game("North Carolina","South Carolina")
        team = self.calc.get_team_player_picked_to_win("Brent H.",game)
        self.assertEqual(team,"team2")

    def __t1_team1_winner(self):
        game = self.__find_game("LSU","TCU")
        team = self.calc.get_team_player_picked_to_win("Brent H.",game)
        self.assertEqual(team,"team1")

    def __find_game(self,team1,team2):
        for g in self.games:
            same_teams = team1 == g.team1.name and team2 == g.team2.name
            if same_teams:
                return g
        raise AssertionError, "Could not find game"

    def __find_week2_game(self,team1,team2):
        for g in self.games2:
            same_teams = team1 == g.team1.name and team2 == g.team2.name
            if same_teams:
                return g
        raise AssertionError, "Could not find game"

    def __find_team(self,name):
        for t in self.teams:
            if t.name == name:
                return t
        raise AssertionError,"Could not find team %s" % (name)

    def __t2_invalid_player_name(self):
        with self.assertRaises(AssertionError):
            self.calc.get_team_name_player_picked_to_win("playerxxx",self.games[0])

    def __t2_invalid_game(self):
        invalid_game = self.games2[0]
        with self.assertRaises(AssertionError):
            self.calc.get_team_name_player_picked_to_win("Brent H.",invalid_game)

    def __t2_game_none(self):
        with self.assertRaises(AssertionError):
            self.calc.get_team_name_player_picked_to_win("Brent H.",None)

    def __t2_team2_winner(self):
        game = self.__find_game("North Carolina","South Carolina")
        team = self.calc.get_team_name_player_picked_to_win("Brent H.",game)
        self.assertEqual(team,"South Carolina")

    def __t2_team1_winner(self):
        game = self.__find_game("LSU","TCU")
        team = self.calc.get_team_name_player_picked_to_win("Brent H.",game)
        self.assertEqual(team,"LSU")

    def __t3_bad_game_favored_value(self):
        g = Game()
        g.team1_score = 0
        g.team2_score = 0
        g.favored = "bad value"
        g.spread = 0.5
        with self.assertRaises(AssertionError):
            self.calc.is_team1_winning_pool(g)

    def __t3_team1_ahead(self):
        g = Game()
        g.team1_score = 20 
        g.team2_score = 10 
        g.favored = "team1"
        g.spread = 5.5 
        self.assertTrue(self.calc.is_team1_winning_pool(g))

    def __t3_team1_behind(self):
        g = Game()
        g.team1_score = 10 
        g.team2_score = 20 
        g.favored = "team1"
        g.spread = 5.5 
        self.assertFalse(self.calc.is_team1_winning_pool(g))

    def __t3_team1_ahead_in_pool_behind_in_game(self):
        g = Game()
        g.team1_score = 14 
        g.team2_score = 17 
        g.favored = "team2"
        g.spread = 3.5 
        self.assertTrue(self.calc.is_team1_winning_pool(g))

    def __t3_team1_behind_in_pool_ahead_in_game(self):
        g = Game()
        g.team1_score = 21 
        g.team2_score = 17 
        g.favored = "team1"
        g.spread = 4.5 
        self.assertFalse(self.calc.is_team1_winning_pool(g))

    def __t3_team1_boundary_case1(self):
        g = Game()
        g.team1_score = 17 
        g.team2_score = 16 
        g.favored = "team1"
        g.spread = 0.5 
        self.assertTrue(self.calc.is_team1_winning_pool(g))

    def __t3_team1_boundary_case2(self):
        g = Game()
        g.team1_score = 16 
        g.team2_score = 17 
        g.favored = "team1"
        g.spread = 0.5 
        self.assertFalse(self.calc.is_team1_winning_pool(g))

    def __t3_team1_boundary_case3(self):
        g = Game()
        g.team1_score = 17 
        g.team2_score = 16 
        g.favored = "team2"
        g.spread = 0.5 
        self.assertTrue(self.calc.is_team1_winning_pool(g))

    def __t3_team1_boundary_case4(self):
        g = Game()
        g.team1_score = 16 
        g.team2_score = 17 
        g.favored = "team2"
        g.spread = 0.5 
        self.assertFalse(self.calc.is_team1_winning_pool(g))

    def __t4_bad_game_favored_value(self):
        g = Game()
        g.team1_score = 0
        g.team2_score = 0
        g.favored = "bad value"
        g.spread = 0.5
        with self.assertRaises(AssertionError):
            self.calc.is_team2_winning_pool(g)

    def __t4_team2_ahead(self):
        g = Game()
        g.team1_score = 10 
        g.team2_score = 20 
        g.favored = "team2"
        g.spread = 5.5 
        self.assertTrue(self.calc.is_team2_winning_pool(g))

    def __t4_team2_behind(self):
        g = Game()
        g.team1_score = 20 
        g.team2_score = 10 
        g.favored = "team2"
        g.spread = 5.5 
        self.assertFalse(self.calc.is_team2_winning_pool(g))

    def __t4_team2_ahead_in_pool_behind_in_game(self):
        g = Game()
        g.team1_score = 17 
        g.team2_score = 14 
        g.favored = "team1"
        g.spread = 3.5 
        self.assertTrue(self.calc.is_team2_winning_pool(g))

    def __t4_team2_behind_in_pool_ahead_in_game(self):
        g = Game()
        g.team1_score = 17
        g.team2_score = 21
        g.favored = "team2"
        g.spread = 4.5 
        self.assertFalse(self.calc.is_team2_winning_pool(g))

    def __t4_team2_boundary_case1(self):
        g = Game()
        g.team1_score = 16 
        g.team2_score = 17 
        g.favored = "team2"
        g.spread = 0.5 
        self.assertTrue(self.calc.is_team2_winning_pool(g))

    def __t4_team2_boundary_case2(self):
        g = Game()
        g.team1_score = 17 
        g.team2_score = 16 
        g.favored = "team2"
        g.spread = 0.5 
        self.assertFalse(self.calc.is_team2_winning_pool(g))

    def __t4_team2_boundary_case3(self):
        g = Game()
        g.team1_score = 16 
        g.team2_score = 17 
        g.favored = "team1"
        g.spread = 0.5 
        self.assertTrue(self.calc.is_team2_winning_pool(g))

    def __t4_team2_boundary_case4(self):
        g = Game()
        g.team1_score = 17 
        g.team2_score = 16 
        g.favored = "team1"
        g.spread = 0.5 
        self.assertFalse(self.calc.is_team2_winning_pool(g))

    def __t5_game_none(self):
        with self.assertRaises(AssertionError):
            self.calc.get_pool_game_winner(None)

    def __t5_game_in_progress(self):
        g = Game()
        g.state = "in_progress"
        self.assertIsNone(self.calc.get_pool_game_winner(g))

    def __t5_game_not_started(self):
        g = Game()
        g.state = "not_started"
        self.assertIsNone(self.calc.get_pool_game_winner(g))

    def __t5_team1_won(self):
        g = Game()
        g.team1_score = 30 
        g.team2_score = 10 
        g.favored = "team1"
        g.spread = 10.5
        g.state = "final"
        self.assertEqual(self.calc.get_pool_game_winner(g),"team1")

    def __t5_team2_won(self):
        g = Game()
        g.team1_score = 30 
        g.team2_score = 25 
        g.favored = "team1"
        g.spread = 10.5
        g.state = "final"
        self.assertEqual(self.calc.get_pool_game_winner(g),"team2")

    def __t6_game_none(self):
        with self.assertRaises(AssertionError):
            self.calc.get_pool_game_winner_team_name(None)

    def __t6_game_in_progress(self):
        g = Game()
        g.state = "in_progress"
        self.assertIsNone(self.calc.get_pool_game_winner_team_name(g))

    def __t6_game_not_started(self):
        g = Game()
        g.state = "not_started"
        self.assertIsNone(self.calc.get_pool_game_winner_team_name(g))

    def __t6_team1_won(self):
        game = self.__find_game("LSU","TCU")
        self.assertEqual(self.calc.get_pool_game_winner_team_name(game),"LSU")

    def __t6_team2_won(self):
        game = self.__find_game("Utah State","Utah")
        self.assertEqual(self.calc.get_pool_game_winner_team_name(game),"Utah")

    def __t7_game_none(self):
        with self.assertRaises(AssertionError):
            self.calc.get_game_winner(None)

    def __t7_game_in_progress(self):
        g = Game()
        g.state = "in_progress"
        self.assertIsNone(self.calc.get_game_winner(g))

    def __t7_game_not_started(self):
        g = Game()
        g.state = "not_started"
        self.assertIsNone(self.calc.get_game_winner(g))

    def __t7_same_score(self):
        g = Game()
        g.team1_score = 21
        g.team2_score = 21
        g.favored = "team1"
        g.spread = 10.5
        g.state = "final"
        with self.assertRaises(AssertionError):
            self.calc.get_game_winner(g)

    def __t7_team1_won(self):
        g = Game()
        g.team1_score = 31
        g.team2_score = 21
        g.favored = "team1"
        g.spread = 10.5
        g.state = "final"
        self.assertEqual(self.calc.get_game_winner(g),"team1")

    def __t7_team2_won(self):
        g = Game()
        g.team1_score = 10 
        g.team2_score = 24 
        g.favored = "team2"
        g.spread = 14.5
        g.state = "final"
        self.assertEqual(self.calc.get_game_winner(g),"team2")

    def __t7_team1_won_but_not_favored(self):
        g = Game()
        g.team1_score = 24
        g.team2_score = 21
        g.favored = "team2"
        g.spread = 5.5
        g.state = "final"
        self.assertEqual(self.calc.get_game_winner(g),"team1")

    def __t7_team2_won_but_not_favored(self):
        g = Game()
        g.team1_score = 41
        g.team2_score = 48
        g.favored = "team1"
        g.spread = 7.5
        g.state = "final"
        self.assertEqual(self.calc.get_game_winner(g),"team2")

    def __t8_game_none(self):
        with self.assertRaises(AssertionError):
            self.calc.get_game_winner_team_name(None)

    def __t8_game_in_progress(self):
        g = Game()
        g.state = "in_progress"
        self.assertIsNone(self.calc.get_game_winner_team_name(g))

    def __t8_game_not_started(self):
        g = Game()
        g.state = "not_started"
        self.assertIsNone(self.calc.get_game_winner_team_name(g))

    def __t8_same_score(self):
        g = Game()
        g.team1_score = 21
        g.team2_score = 21
        g.favored = "team1"
        g.spread = 10.5
        g.state = "final"
        with self.assertRaises(AssertionError):
            self.calc.get_game_winner_team_name(g)

    def __t8_team1_won(self):
        game = self.__find_game("Penn State","Syracuse")
        self.assertEqual(self.calc.get_game_winner_team_name(game),"Penn State")

    def __t8_team2_won(self):
        game = self.__find_week2_game("West Virginia","Oklahoma")
        self.assertEqual(self.calc.get_game_winner_team_name(game),"Oklahoma")

    def __t9_game_none(self):
        with self.assertRaises(AssertionError):
            self.calc.get_team_winning_pool_game(None)

    def __t9_game_final(self):
        g = Game()
        g.state = "final"
        self.assertIsNone(self.calc.get_team_winning_pool_game(g))

    def __t9_game_not_started(self):
        g = Game()
        g.state = "not_started"
        self.assertIsNone(self.calc.get_team_winning_pool_game(g))

    def __t9_same_score(self):
        g = Game()
        g.team1_score = 35
        g.team2_score = 35
        g.favored = "team1"
        g.spread = 0.5
        g.state = "in_progress"
        self.assertEqual(self.calc.get_team_winning_pool_game(g),"team2")

    def __t9_team1_ahead(self):
        g = Game()
        g.team1_score = 44
        g.team2_score = 48
        g.favored = "team2"
        g.spread = 4.5
        g.state = "in_progress"
        self.assertEqual(self.calc.get_team_winning_pool_game(g),"team1")

    def __t9_team2_ahead(self):
        g = Game()
        g.team1_score = 21
        g.team2_score = 18
        g.favored = "team1"
        g.spread = 3.5
        g.state = "in_progress"
        self.assertEqual(self.calc.get_team_winning_pool_game(g),"team2")

    def __t10_game_none(self):
        with self.assertRaises(AssertionError):
            self.calc.get_team_name_winning_pool_game(None)

    def __t10_game_final(self):
        g = Game()
        g.state = "final"
        self.assertIsNone(self.calc.get_team_name_winning_pool_game(g))

    def __t10_game_not_started(self):
        g = Game()
        g.state = "not_started"
        self.assertIsNone(self.calc.get_team_name_winning_pool_game(g))

    def __t10_same_score(self):
        g = Game()
        g.team1 = self.__find_team("Georgia Tech")
        g.team2 = self.__find_team("Clemson")
        g.team1_score = 35
        g.team2_score = 35
        g.favored = "team1"
        g.spread = 0.5
        g.state = "in_progress"
        self.assertEqual(self.calc.get_team_name_winning_pool_game(g),"Clemson")

    def __t10_team1_ahead(self):
        g = Game()
        g.team1 = self.__find_team("Georgia Tech")
        g.team2 = self.__find_team("Clemson")
        g.team1_score = 44
        g.team2_score = 48
        g.favored = "team2"
        g.spread = 4.5
        g.state = "in_progress"
        self.assertEqual(self.calc.get_team_name_winning_pool_game(g),"Georgia Tech")

    def __t10_team2_ahead(self):
        g = Game()
        g.team1 = self.__find_team("Georgia Tech")
        g.team2 = self.__find_team("Clemson")
        g.team1_score = 21
        g.team2_score = 18
        g.favored = "team1"
        g.spread = 3.5
        g.state = "in_progress"
        self.assertEqual(self.calc.get_team_name_winning_pool_game(g),"Clemson")

    def __t11_game_none(self):
        with self.assertRaises(AssertionError):
            self.calc.get_team_winning_game(None)

    def __t11_game_final(self):
        g = Game()
        g.state = "final"
        self.assertIsNone(self.calc.get_team_winning_game(g))

    def __t11_game_not_started(self):
        g = Game()
        g.state = "not_started"
        self.assertIsNone(self.calc.get_team_winning_game(g))

    def __t11_same_score(self):
        g = Game()
        g.team1 = self.__find_team("Georgia Tech")
        g.team2 = self.__find_team("Clemson")
        g.team1_score = 35
        g.team2_score = 35
        g.favored = "team1"
        g.spread = 0.5
        g.state = "in_progress"
        self.assertEqual(self.calc.get_team_winning_game(g),"tied")

    def __t11_team1_ahead(self):
        g = Game()
        g.team1 = self.__find_team("Georgia Tech")
        g.team2 = self.__find_team("Clemson")
        g.team1_score = 31
        g.team2_score = 24
        g.favored = "team2"
        g.spread = 4.5
        g.state = "in_progress"
        self.assertEqual(self.calc.get_team_winning_game(g),"team1")

    def __t11_team2_ahead(self):
        g = Game()
        g.team1 = self.__find_team("Georgia Tech")
        g.team2 = self.__find_team("Clemson")
        g.team1_score = 17
        g.team2_score = 31
        g.favored = "team1"
        g.spread = 3.5
        g.state = "in_progress"
        self.assertEqual(self.calc.get_team_winning_game(g),"team2")

    def __t12_game_none(self):
        with self.assertRaises(AssertionError):
            self.calc.get_team_name_winning_game(None)

    def __t12_game_final(self):
        g = Game()
        g.state = "final"
        self.assertIsNone(self.calc.get_team_name_winning_game(g))

    def __t12_game_not_started(self):
        g = Game()
        g.state = "not_started"
        self.assertIsNone(self.calc.get_team_name_winning_game(g))

    def __t12_same_score(self):
        g = Game()
        g.team1 = self.__find_team("Georgia Tech")
        g.team2 = self.__find_team("Clemson")
        g.team1_score = 35
        g.team2_score = 35
        g.favored = "team1"
        g.spread = 0.5
        g.state = "in_progress"
        self.assertEqual(self.calc.get_team_name_winning_game(g),"tied")

    def __t12_team1_ahead(self):
        g = Game()
        g.team1 = self.__find_team("Georgia Tech")
        g.team2 = self.__find_team("Clemson")
        g.team1_score = 31
        g.team2_score = 24
        g.favored = "team2"
        g.spread = 4.5
        g.state = "in_progress"
        self.assertEqual(self.calc.get_team_name_winning_game(g),"Georgia Tech")

    def __t12_team2_ahead(self):
        g = Game()
        g.team1 = self.__find_team("Georgia Tech")
        g.team2 = self.__find_team("Clemson")
        g.team1_score = 17
        g.team2_score = 31
        g.favored = "team1"
        g.spread = 3.5
        g.state = "in_progress"
        self.assertEqual(self.calc.get_team_name_winning_game(g),"Clemson")

    def __t13_game_none(self):
        with self.assertRaises(AssertionError):
            self.calc.player_did_not_pick('Brent H.',None)

    def __t13_invalid_player_name(self):
        with self.assertRaises(AssertionError):
            self.calc.player_did_not_pick("playerxxx",self.games[0])

    def __t13_player_missing_all_week_picks(self):
        self.picks['Temporary Player'] = []
        self.assertTrue(self.calc.player_did_not_pick("Temporary Player",self.games[0]))

    def __t13_player_missing_pick_for_game(self):
        self.picks['Temporary Player'] = []
        for i,pick in enumerate(self.picks['Brent H.']):
            game0_pick = pick.game.key() == self.games[0].key()
            if not(game0_pick):
                self.picks['Temporary Player'].append(pick)
        self.assertTrue(self.calc.player_did_not_pick("Temporary Player",self.games[0]))

    def __t13_player_missing_pick_winner(self):
        pick = self.picks['Brent H.'][0]
        saved_winner = pick.winner
        pick.winner = None
        self.picks['Temporary Player'] = [pick]
        self.assertTrue(self.calc.player_did_not_pick("Temporary Player",pick.game))
        pick.winner = saved_winner

    def __t13_player_made_pick(self):
        self.assertFalse(self.calc.player_did_not_pick("Brent H.",self.games[0]))
