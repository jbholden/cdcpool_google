from code.update import *
from code.calculator import *
from code.database import *
from models.games import *
import time
import logging
import unittest

# TODO:  known issue:  self.picks[player][i].games not the same as self.games
#        changing to stringproperties will fix this issue
#        (games as a dict use games[key])
# TODO:  add more invalid game tests


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

    def test_t14_did_player_win_game(self):
        self.__t14_game_none()
        self.__t14_invalid_player_name()
        self.__t14_player_missing_pick()
        self.__t14_game_in_progress()
        self.__t14_game_not_started()
        self.__t14_player_won_game()
        self.__t14_player_lost_game()

    def test_t15_did_player_lose_game(self):
        self.__t15_game_none()
        self.__t15_invalid_player_name()
        self.__t15_player_missing_pick()
        self.__t15_game_in_progress()
        self.__t15_game_not_started()
        self.__t15_player_won_game()
        self.__t15_player_lost_game()

    def test_t16_get_number_of_wins(self):
        self.__t16_invalid_player_name()
        self.__t16_no_games_started()
        self.__t16_some_games_in_progress()
        self.__t16_mixed_game_states()
        self.__t16_all_games_final()
        self.__t16_player_with_no_picks()
        self.__t16_player_0_wins()
        self.__t16_player_10_wins()

    def test_t17_get_number_of_wins(self):
        self.__t17_invalid_player_name()
        self.__t17_no_games_started()
        self.__t17_some_games_in_progress()
        self.__t17_mixed_game_states()
        self.__t17_all_games_final()
        self.__t17_player_with_no_picks()
        self.__t17_player_0_losses()
        self.__t17_player_10_losses()

    def test_t18_is_player_winning_game(self):
        self.__t18_game_none()
        self.__t18_invalid_player_name()
        self.__t18_player_pick_missing_game_not_started()
        self.__t18_player_pick_missing_game_in_progress()
        self.__t18_player_pick_missing_game_final()
        self.__t18_game_not_started()
        self.__t18_game_final()
        self.__t18_player_ahead_in_game_and_pool()
        self.__t18_player_behind_in_game_and_pool()
        self.__t18_player_ahead_in_game_and_behind_in_pool()
        self.__t18_player_behind_in_game_and_ahead_in_pool()

    def test_t19_is_player_losing_game(self):
        self.__t19_game_none()
        self.__t19_invalid_player_name()
        self.__t19_player_pick_missing_game_not_started()
        self.__t19_player_pick_missing_game_in_progress()
        self.__t19_player_pick_missing_game_final()
        self.__t19_game_not_started()
        self.__t19_game_final()
        self.__t19_player_ahead_in_game_and_pool()
        self.__t19_player_behind_in_game_and_pool()
        self.__t19_player_ahead_in_game_and_behind_in_pool()
        self.__t19_player_behind_in_game_and_ahead_in_pool()

    def test_t20_is_player_projected_to_win_game(self):
        self.__t20_game_none()
        self.__t20_invalid_player_name()
        self.__t20_player_pick_missing()
        self.__t20_game_final_player_ahead_in_game_and_pool()
        self.__t20_game_final_player_behind_in_game_and_pool()
        self.__t20_game_final_player_ahead_in_game_and_behind_in_pool()
        self.__t20_game_final_player_behind_in_game_and_ahead_in_pool()
        self.__t20_game_in_progress_player_ahead_in_game_and_pool()
        self.__t20_game_in_progress_player_behind_in_game_and_pool()
        self.__t20_game_in_progress_player_ahead_in_game_and_behind_in_pool()
        self.__t20_game_in_progress_player_behind_in_game_and_ahead_in_pool()
        self.__t20_game_not_started_player_ahead_in_game_and_pool()
        self.__t20_game_not_started_player_behind_in_game_and_pool()
        self.__t20_game_not_started_player_ahead_in_game_and_behind_in_pool()
        self.__t20_game_not_started_player_behind_in_game_and_ahead_in_pool()

    def test_t21_is_player_possible_to_win_game(self):
        self.__t21_game_none()
        self.__t21_invalid_player_name()
        self.__t21_player_pick_missing()
        self.__t21_game_final_player_ahead_in_game_and_pool()
        self.__t21_game_final_player_behind_in_game_and_pool()
        self.__t21_game_final_player_ahead_in_game_and_behind_in_pool()
        self.__t21_game_final_player_behind_in_game_and_ahead_in_pool()
        self.__t21_game_in_progress_player_ahead_in_game_and_pool()
        self.__t21_game_in_progress_player_behind_in_game_and_pool()
        self.__t21_game_in_progress_player_ahead_in_game_and_behind_in_pool()
        self.__t21_game_in_progress_player_behind_in_game_and_ahead_in_pool()
        self.__t21_game_not_started_player_ahead_in_game_and_pool()
        self.__t21_game_not_started_player_behind_in_game_and_pool()
        self.__t21_game_not_started_player_ahead_in_game_and_behind_in_pool()
        self.__t21_game_not_started_player_behind_in_game_and_ahead_in_pool()

    def test_t22_get_number_of_projected_wins(self):
        self.__t22_invalid_player_name()
        self.__t22_no_games_started()
        self.__t22_some_games_in_progress()
        self.__t22_mixed_game_states()
        self.__t22_all_games_final()
        self.__t22_player_with_no_picks()
        self.__t22_game_not_started_player_0_wins()
        self.__t22_game_not_started_player_10_wins()
        self.__t22_game_in_progress_player_0_wins()
        self.__t22_game_in_progress_player_10_wins()
        self.__t22_game_final_player_0_wins()
        self.__t22_game_final_player_10_wins()

    def test_t23_get_number_of_possible_wins(self):
        self.__t23_invalid_player_name()
        self.__t23_no_games_started()
        self.__t23_some_games_in_progress()
        self.__t23_mixed_game_states()
        self.__t23_all_games_final()
        self.__t23_player_with_no_picks()
        self.__t23_game_not_started_player_0_wins()
        self.__t23_game_not_started_player_10_wins()
        self.__t23_game_in_progress_player_0_wins()
        self.__t23_game_in_progress_player_10_wins()
        self.__t23_game_final_player_0_wins()
        self.__t23_game_final_player_10_wins()

    def test_t24_all_games_final(self):
        self.__t24_no_games_started()
        self.__t24_some_games_in_progress()
        self.__t24_mixed_game_states()
        self.__t24_all_games_final()

    def test_t25_no_games_started(self):
        self.__t25_no_games_started()
        self.__t25_some_games_in_progress()
        self.__t25_mixed_game_states()
        self.__t25_all_games_final()

    def test_t26_at_least_one_game_in_progress(self):
        self.__t26_no_games_started()
        self.__t26_one_game_in_progress()
        self.__t26_some_games_in_progress()
        self.__t26_mixed_game_states()
        self.__t26_all_games_final()

    def test_t27_get_summary_state_of_all_games(self):
        self.__t27_no_games_started()
        self.__t27_one_game_in_progress()
        self.__t27_some_games_in_progress()
        self.__t27_mixed_game_states()
        self.__t27_all_games_final()

    def test_t28_get_game_result_string(self):
        self.__t28_game_none()
        self.__t28_invalid_player_name()
        self.__t28_player_pick_missing()
        self.__t28_game_win()
        self.__t28_game_loss()
        self.__t28_game_ahead()
        self.__t28_game_behind()
        self.__t28_game_not_started()

    def test_t29_get_favored_team_name(self):
        self.__t29_game_none()
        self.__t29_invalid_favored()
        self.__t29_team1_favored()
        self.__t29_team2_favored()

    def test_t30_get_game_score_spread(self):
        self.__t30_game_none()
        self.__t30_game_not_started()
        self.__t30_game_in_progress()
        self.__t30_tied_score()
        self.__t30_team1_ahead()
        self.__t30_team2_ahead()

    def test_t31_get_pick_score_spread(self):
        self.__t31_pick_none()
        self.__t31_pick_team1_score_none()
        self.__t31_pick_team2_score_none()
        self.__t31_tied_score()
        self.__t31_team1_ahead()
        self.__t31_team2_ahead()

    def test_t32_get_featured_game(self):
        self.__t32_featured_game_missing()
        self.__t32_featured_game()

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
        pick = self.__create_a_player_pick_with_winner_missing('Temporary Player')
        self.assertTrue(self.calc.player_did_not_pick("Temporary Player",pick.game))
        self.__restore_missing_winner('Temporary Player')

    def __t13_player_made_pick(self):
        self.assertFalse(self.calc.player_did_not_pick("Brent H.",self.games[0]))

    def __t14_game_none(self):
        with self.assertRaises(AssertionError):
            self.calc.did_player_win_game('Brent H.',None)

    def __t14_invalid_player_name(self):
        with self.assertRaises(AssertionError):
            self.calc.did_player_win_game("playerxxx",self.games[0])

    def __t14_player_missing_pick(self):
        pick = self.__create_a_player_pick_with_winner_missing('Temporary Player')
        self.assertFalse(self.calc.did_player_win_game("Temporary Player",pick.game))
        self.__restore_missing_winner('Temporary Player')

    def __t14_game_in_progress(self):
        game = self.picks['Brent H.'][0].game
        saved_state = game.state
        self.picks['Brent H.'][0].game.state = "in_progress"
        self.assertFalse(self.calc.did_player_win_game('Brent H.',game))
        self.picks['Brent H.'][0].game.state = saved_state

    def __t14_game_not_started(self):
        game = self.picks['Brent H.'][0].game
        saved_state = game.state
        self.picks['Brent H.'][0].game.state = "not_started"
        self.assertFalse(self.calc.did_player_win_game('Brent H.',game))
        self.picks['Brent H.'][0].game.state = saved_state

    def __t14_player_won_game(self):
        game = self.__find_game("North Carolina","South Carolina")
        self.assertTrue(self.calc.did_player_win_game('Brent H.',game))

    def __t14_player_lost_game(self):
        game = self.__find_game("Penn State","Syracuse")
        self.assertFalse(self.calc.did_player_win_game('Brent H.',game))

    def __create_a_player_pick_with_winner_missing(self,player_name):
        pick = self.picks['Brent H.'][0]
        self.__saved_winner = pick.winner
        pick.winner = None
        self.picks[player_name] = [pick]
        return pick

    def __restore_missing_winner(self,player_name):
        self.picks['Brent H.'][0].winner = self.__saved_winner
        del self.picks[player_name]

    def __t15_game_none(self):
        with self.assertRaises(AssertionError):
            self.calc.did_player_lose_game('Brent H.',None)

    def __t15_invalid_player_name(self):
        with self.assertRaises(AssertionError):
            self.calc.did_player_lose_game("playerxxx",self.games[0])

    def __t15_player_missing_pick(self):
        pick = self.__create_a_player_pick_with_winner_missing('Temporary Player')
        self.assertTrue(self.calc.did_player_lose_game("Temporary Player",pick.game))
        self.__restore_missing_winner('Temporary Player')

    def __t15_game_in_progress(self):
        game = self.picks['Brent H.'][0].game
        saved_state = game.state
        self.picks['Brent H.'][0].game.state = "in_progress"
        self.assertFalse(self.calc.did_player_lose_game('Brent H.',game))
        self.picks['Brent H.'][0].game.state = saved_state

    def __t15_game_not_started(self):
        game = self.picks['Brent H.'][0].game
        saved_state = game.state
        self.picks['Brent H.'][0].game.state = "not_started"
        self.assertFalse(self.calc.did_player_lose_game('Brent H.',game))
        self.picks['Brent H.'][0].game.state = saved_state

    def __t15_player_won_game(self):
        game = self.__find_game("North Carolina","South Carolina")
        self.assertFalse(self.calc.did_player_lose_game('Brent H.',game))

    def __t15_player_lost_game(self):
        game = self.__find_game("Penn State","Syracuse")
        self.assertTrue(self.calc.did_player_lose_game('Brent H.',game))

    def __t16_invalid_player_name(self):
        with self.assertRaises(AssertionError):
            self.calc.get_number_of_wins("playerxxx")

    def __t16_no_games_started(self):
        saved_states = self.__modify_game_states(['not_started']*10)
        self.assertEqual(self.calc.get_number_of_wins('Brent H.'),0)
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t16_some_games_in_progress(self):
        states = ['not_started']*3 + ['in_progress']*7
        saved_states = self.__modify_game_states(states)
        self.assertEqual(self.calc.get_number_of_wins('Brent H.'),0)
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t16_mixed_game_states(self):
        num_wins_in_first_3_games_2013_week_1 = 2

        states = ['final']*3 + ['not_started']*3 + ['in_progress']*4
        saved_states = self.__modify_game_states(states)
        self.assertEqual(self.calc.get_number_of_wins('Brent H.'),num_wins_in_first_3_games_2013_week_1)
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t16_all_games_final(self):
        num_wins_2013_week_1 = 5
        self.assertEqual(self.calc.get_number_of_wins('Brent H.'),num_wins_2013_week_1)

    def __t16_player_with_no_picks(self):
        saved = self.__make_all_player_picks_not_entered('Brent H.')
        self.assertEqual(self.calc.get_number_of_wins('Brent H.'),0)
        self.__restore_player_picks_winners('Brent H.',saved)

    def __t16_player_0_wins(self):
        self.__make_dale_0_wins()
        self.assertEqual(self.calc.get_number_of_wins('Dale R.'),0)
        self.__restore_dale_picks()

    def __t16_player_10_wins(self):
        self.__make_william_10_wins()
        self.assertEqual(self.calc.get_number_of_wins('William M.'),10)
        self.__restore_william_picks()

    def __make_william_10_wins(self):
        game1 = self.__find_game("Colorado","Colorado State")
        self.__change_player_pick("William M.",game1)

    def __restore_william_picks(self):
        game1 = self.__find_game("Colorado","Colorado State")
        self.__change_player_pick("William M.",game1)

    def __make_dale_0_wins(self):
        game1 = self.__find_game("North Carolina","South Carolina")
        game2 = self.__find_game("Utah State","Utah")
        game3 = self.__find_game("Georgia","Clemson")
        self.__change_player_pick("Dale R.",game1)
        self.__change_player_pick("Dale R.",game2)
        self.__change_player_pick("Dale R.",game3)

    def __restore_dale_picks(self):
        game1 = self.__find_game("North Carolina","South Carolina")
        game2 = self.__find_game("Utah State","Utah")
        game3 = self.__find_game("Georgia","Clemson")
        self.__change_player_pick("Dale R.",game1)
        self.__change_player_pick("Dale R.",game2)
        self.__change_player_pick("Dale R.",game3)


    def __change_player_pick(self,player_name,game):
        player_picks = self.picks[player_name]
        for i,pick in enumerate(player_picks):
            if pick.game.key() == game.key():
                if pick.winner == "team1":
                    self.picks[player_name][i].winner = "team2"
                elif pick.winner == "team2":
                    self.picks[player_name][i].winner = "team1"

    def __modify_game_states(self,states):
        assert len(states) == 10
        assert len(self.games) == 10
        saved = []
        for i,game in enumerate(self.games):
            saved.append(game.state)
            self.games[i].state = states[i]
        return saved

    def __make_all_player_picks_not_entered(self,player_name):
        return self.__set_player_picks_winners(player_name,[None]*10)

    def __restore_player_picks_winners(self,player_name,saved_winners):
        ignore_return_value = self.__set_player_picks_winners(player_name,saved_winners)

    def __set_player_picks_winners(self,player_name,winners):
        assert len(winners) == len(self.picks[player_name])
        saved = []
        for i,pick in enumerate(self.picks[player_name]):
            saved.append(pick.winner)
            self.picks[player_name][i].winner = winners[i]
        return saved

    def __t17_invalid_player_name(self):
        with self.assertRaises(AssertionError):
            self.calc.get_number_of_losses("playerxxx")

    def __t17_no_games_started(self):
        saved_states = self.__modify_game_states(['not_started']*10)
        self.assertEqual(self.calc.get_number_of_losses('Brent H.'),0)
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t17_some_games_in_progress(self):
        states = ['not_started']*3 + ['in_progress']*7
        saved_states = self.__modify_game_states(states)
        self.assertEqual(self.calc.get_number_of_losses('Brent H.'),0)
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t17_mixed_game_states(self):
        num_losses_in_first_3_games_2013_week_1 = 1

        states = ['final']*3 + ['not_started']*3 + ['in_progress']*4
        saved_states = self.__modify_game_states(states)
        self.assertEqual(self.calc.get_number_of_losses('Brent H.'),num_losses_in_first_3_games_2013_week_1)
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t17_all_games_final(self):
        num_losses_2013_week_1 = 4
        self.assertEqual(self.calc.get_number_of_losses('Byron R.'),num_losses_2013_week_1)

    def __t17_player_with_no_picks(self):
        saved = self.__make_all_player_picks_not_entered('Brent H.')
        self.assertEqual(self.calc.get_number_of_losses('Brent H.'),10)
        self.__restore_player_picks_winners('Brent H.',saved)

    def __t17_player_0_losses(self):
        self.__make_william_10_wins()
        self.assertEqual(self.calc.get_number_of_losses('William M.'),0)
        self.__restore_william_picks()

    def __t17_player_10_losses(self):
        self.__make_dale_0_wins()
        self.assertEqual(self.calc.get_number_of_losses('Dale R.'),10)
        self.__restore_dale_picks()

    def __t18_game_none(self):
        with self.assertRaises(AssertionError):
            self.calc.is_player_winning_game('Brent H.',None)

    def __t18_invalid_player_name(self):
        with self.assertRaises(AssertionError):
            self.calc.is_player_winning_game("playerxxx",self.games[0])

    def __t18_player_pick_missing_game_not_started(self):
        player_name = "Brent H."
        self.picks[player_name][0].winner = None
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 25
        self.picks[player_name][0].game.team2_score = 10
        self.picks[player_name][0].game.state = "not_started"

        self.assertFalse(self.calc.is_player_winning_game(player_name,self.picks[player_name][0].game))

    def __t18_player_pick_missing_game_in_progress(self):
        player_name = "Brent H."
        self.picks[player_name][0].winner = None
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 25
        self.picks[player_name][0].game.team2_score = 10
        self.picks[player_name][0].game.state = "in_progress"

        self.assertFalse(self.calc.is_player_winning_game(player_name,self.picks[player_name][0].game))

    def __t18_player_pick_missing_game_final(self):
        player_name = "Brent H."
        self.picks[player_name][0].winner = None
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 25
        self.picks[player_name][0].game.team2_score = 10
        self.picks[player_name][0].game.state = "final"

        self.assertFalse(self.calc.is_player_winning_game(player_name,self.picks[player_name][0].game))

    def __t18_player_ahead_in_game_and_pool(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 25
        self.picks[player_name][0].game.team2_score = 10
        self.picks[player_name][0].game.state = "in_progress"

        self.assertTrue(self.calc.is_player_winning_game(player_name,self.picks[player_name][0].game))

    def __t18_player_behind_in_game_and_pool(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 10
        self.picks[player_name][0].game.team2_score = 30
        self.picks[player_name][0].game.state = "in_progress"

        self.assertFalse(self.calc.is_player_winning_game(player_name,self.picks[player_name][0].game))

    def __t18_player_ahead_in_game_and_behind_in_pool(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team2"
        self.picks[player_name][0].game.favored = "team2"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 20 
        self.picks[player_name][0].game.team2_score = 25
        self.picks[player_name][0].game.state = "in_progress"

        self.assertFalse(self.calc.is_player_winning_game(player_name,self.picks[player_name][0].game))

    def __t18_player_behind_in_game_and_ahead_in_pool(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team2"
        self.picks[player_name][0].game.spread = 1.5
        self.picks[player_name][0].game.team1_score = 20 
        self.picks[player_name][0].game.team2_score = 21
        self.picks[player_name][0].game.state = "in_progress"

        self.assertTrue(self.calc.is_player_winning_game(player_name,self.picks[player_name][0].game))

    def __t18_game_not_started(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team2"
        self.picks[player_name][0].game.spread = 1.5
        self.picks[player_name][0].game.team1_score = 20 
        self.picks[player_name][0].game.team2_score = 21
        self.picks[player_name][0].game.state = "not_started"

        self.assertFalse(self.calc.is_player_winning_game(player_name,self.picks[player_name][0].game))

    def __t18_game_final(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team2"
        self.picks[player_name][0].game.spread = 1.5
        self.picks[player_name][0].game.team1_score = 20 
        self.picks[player_name][0].game.team2_score = 21
        self.picks[player_name][0].game.state = "final"

        self.assertFalse(self.calc.is_player_winning_game(player_name,self.picks[player_name][0].game))

    def __t19_game_none(self):
        with self.assertRaises(AssertionError):
            self.calc.is_player_losing_game('Brent H.',None)

    def __t19_invalid_player_name(self):
        with self.assertRaises(AssertionError):
            self.calc.is_player_losing_game("playerxxx",self.games[0])

    def __t19_game_not_started(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team2"
        self.picks[player_name][0].game.spread = 1.5
        self.picks[player_name][0].game.team1_score = 20 
        self.picks[player_name][0].game.team2_score = 21
        self.picks[player_name][0].game.state = "not_started"

        self.assertFalse(self.calc.is_player_losing_game(player_name,self.picks[player_name][0].game))

    def __t19_game_final(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team2"
        self.picks[player_name][0].game.spread = 1.5
        self.picks[player_name][0].game.team1_score = 20 
        self.picks[player_name][0].game.team2_score = 21
        self.picks[player_name][0].game.state = "final"

        self.assertFalse(self.calc.is_player_losing_game(player_name,self.picks[player_name][0].game))

    def __t19_player_pick_missing_game_not_started(self):
        player_name = "Brent H."
        self.picks[player_name][0].winner = None
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 25
        self.picks[player_name][0].game.team2_score = 10
        self.picks[player_name][0].game.state = "not_started"

        self.assertTrue(self.calc.is_player_losing_game(player_name,self.picks[player_name][0].game))

    def __t19_player_pick_missing_game_in_progress(self):
        player_name = "Brent H."
        self.picks[player_name][0].winner = None
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 25
        self.picks[player_name][0].game.team2_score = 10
        self.picks[player_name][0].game.state = "in_progress"

        self.assertTrue(self.calc.is_player_losing_game(player_name,self.picks[player_name][0].game))

    def __t19_player_pick_missing_game_final(self):
        player_name = "Brent H."
        self.picks[player_name][0].winner = None
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 10
        self.picks[player_name][0].game.team2_score = 25
        self.picks[player_name][0].game.state = "final"

        self.assertFalse(self.calc.is_player_losing_game(player_name,self.picks[player_name][0].game))

    def __t19_player_ahead_in_game_and_pool(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 25
        self.picks[player_name][0].game.team2_score = 10
        self.picks[player_name][0].game.state = "in_progress"

        self.assertFalse(self.calc.is_player_losing_game(player_name,self.picks[player_name][0].game))

    def __t19_player_behind_in_game_and_pool(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 10
        self.picks[player_name][0].game.team2_score = 30
        self.picks[player_name][0].game.state = "in_progress"

        self.assertTrue(self.calc.is_player_losing_game(player_name,self.picks[player_name][0].game))

    def __t19_player_ahead_in_game_and_behind_in_pool(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team2"
        self.picks[player_name][0].game.favored = "team2"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 20 
        self.picks[player_name][0].game.team2_score = 25
        self.picks[player_name][0].game.state = "in_progress"

        self.assertTrue(self.calc.is_player_losing_game(player_name,self.picks[player_name][0].game))

    def __t19_player_behind_in_game_and_ahead_in_pool(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team2"
        self.picks[player_name][0].game.spread = 1.5
        self.picks[player_name][0].game.team1_score = 20 
        self.picks[player_name][0].game.team2_score = 21
        self.picks[player_name][0].game.state = "in_progress"

        self.assertFalse(self.calc.is_player_losing_game(player_name,self.picks[player_name][0].game))

    def __t20_game_none(self):
        with self.assertRaises(AssertionError):
            self.calc.is_player_projected_to_win_game('Brent H.',None)

    def __t20_invalid_player_name(self):
        with self.assertRaises(AssertionError):
            self.calc.is_player_projected_to_win_game("playerxxx",self.games[0])

    def __t20_player_pick_missing(self):
        player_name = "Brent H."
        self.picks[player_name][0].winner = None
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 10
        self.picks[player_name][0].game.team2_score = 25
        self.picks[player_name][0].game.state = "in_progress"

        self.assertFalse(self.calc.is_player_projected_to_win_game(player_name,self.picks[player_name][0].game))

    def __t20_game_final_player_ahead_in_game_and_pool(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 25
        self.picks[player_name][0].game.team2_score = 10
        self.picks[player_name][0].game.state = "final"

        self.assertTrue(self.calc.is_player_projected_to_win_game(player_name,self.picks[player_name][0].game))

    def __t20_game_final_player_behind_in_game_and_pool(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 10
        self.picks[player_name][0].game.team2_score = 30
        self.picks[player_name][0].game.state = "final"

        self.assertFalse(self.calc.is_player_projected_to_win_game(player_name,self.picks[player_name][0].game))


    def __t20_game_final_player_ahead_in_game_and_behind_in_pool(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team2"
        self.picks[player_name][0].game.favored = "team2"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 20 
        self.picks[player_name][0].game.team2_score = 25
        self.picks[player_name][0].game.state = "final"

        self.assertFalse(self.calc.is_player_projected_to_win_game(player_name,self.picks[player_name][0].game))

    def __t20_game_final_player_behind_in_game_and_ahead_in_pool(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team2"
        self.picks[player_name][0].game.spread = 1.5
        self.picks[player_name][0].game.team1_score = 20 
        self.picks[player_name][0].game.team2_score = 21
        self.picks[player_name][0].game.state = "final"

        self.assertTrue(self.calc.is_player_projected_to_win_game(player_name,self.picks[player_name][0].game))

    def __t20_game_in_progress_player_ahead_in_game_and_pool(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 25
        self.picks[player_name][0].game.team2_score = 10
        self.picks[player_name][0].game.state = "in_progress"

        self.assertTrue(self.calc.is_player_projected_to_win_game(player_name,self.picks[player_name][0].game))

    def __t20_game_in_progress_player_behind_in_game_and_pool(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 10
        self.picks[player_name][0].game.team2_score = 30
        self.picks[player_name][0].game.state = "in_progress"

        self.assertFalse(self.calc.is_player_projected_to_win_game(player_name,self.picks[player_name][0].game))


    def __t20_game_in_progress_player_ahead_in_game_and_behind_in_pool(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team2"
        self.picks[player_name][0].game.favored = "team2"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 20 
        self.picks[player_name][0].game.team2_score = 25
        self.picks[player_name][0].game.state = "in_progress"

        self.assertFalse(self.calc.is_player_projected_to_win_game(player_name,self.picks[player_name][0].game))

    def __t20_game_in_progress_player_behind_in_game_and_ahead_in_pool(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team2"
        self.picks[player_name][0].game.spread = 1.5
        self.picks[player_name][0].game.team1_score = 20 
        self.picks[player_name][0].game.team2_score = 21
        self.picks[player_name][0].game.state = "in_progress"

        self.assertTrue(self.calc.is_player_projected_to_win_game(player_name,self.picks[player_name][0].game))

    def __t20_game_not_started_player_ahead_in_game_and_pool(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 25
        self.picks[player_name][0].game.team2_score = 10
        self.picks[player_name][0].game.state = "not_started"

        self.assertTrue(self.calc.is_player_projected_to_win_game(player_name,self.picks[player_name][0].game))

    def __t20_game_not_started_player_behind_in_game_and_pool(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 10
        self.picks[player_name][0].game.team2_score = 30
        self.picks[player_name][0].game.state = "not_started"

        self.assertTrue(self.calc.is_player_projected_to_win_game(player_name,self.picks[player_name][0].game))


    def __t20_game_not_started_player_ahead_in_game_and_behind_in_pool(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team2"
        self.picks[player_name][0].game.favored = "team2"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 20 
        self.picks[player_name][0].game.team2_score = 25
        self.picks[player_name][0].game.state = "not_started"

        self.assertTrue(self.calc.is_player_projected_to_win_game(player_name,self.picks[player_name][0].game))

    def __t20_game_not_started_player_behind_in_game_and_ahead_in_pool(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team2"
        self.picks[player_name][0].game.spread = 1.5
        self.picks[player_name][0].game.team1_score = 20 
        self.picks[player_name][0].game.team2_score = 21
        self.picks[player_name][0].game.state = "not_started"

        self.assertTrue(self.calc.is_player_projected_to_win_game(player_name,self.picks[player_name][0].game))

    def __t21_game_none(self):
        with self.assertRaises(AssertionError):
            self.calc.is_player_possible_to_win_game('Brent H.',None)

    def __t21_invalid_player_name(self):
        with self.assertRaises(AssertionError):
            self.calc.is_player_possible_to_win_game("playerxxx",self.games[0])

    def __t21_player_pick_missing(self):
        player_name = "Brent H."
        self.picks[player_name][0].winner = None
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 10
        self.picks[player_name][0].game.team2_score = 25
        self.picks[player_name][0].game.state = "in_progress"

        self.assertFalse(self.calc.is_player_possible_to_win_game(player_name,self.picks[player_name][0].game))

    def __t21_game_final_player_ahead_in_game_and_pool(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 25
        self.picks[player_name][0].game.team2_score = 10
        self.picks[player_name][0].game.state = "final"

        self.assertTrue(self.calc.is_player_possible_to_win_game(player_name,self.picks[player_name][0].game))

    def __t21_game_final_player_behind_in_game_and_pool(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 10
        self.picks[player_name][0].game.team2_score = 30
        self.picks[player_name][0].game.state = "final"

        self.assertFalse(self.calc.is_player_possible_to_win_game(player_name,self.picks[player_name][0].game))


    def __t21_game_final_player_ahead_in_game_and_behind_in_pool(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team2"
        self.picks[player_name][0].game.favored = "team2"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 20 
        self.picks[player_name][0].game.team2_score = 25
        self.picks[player_name][0].game.state = "final"

        self.assertFalse(self.calc.is_player_possible_to_win_game(player_name,self.picks[player_name][0].game))

    def __t21_game_final_player_behind_in_game_and_ahead_in_pool(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team2"
        self.picks[player_name][0].game.spread = 1.5
        self.picks[player_name][0].game.team1_score = 20 
        self.picks[player_name][0].game.team2_score = 21
        self.picks[player_name][0].game.state = "final"

        self.assertTrue(self.calc.is_player_possible_to_win_game(player_name,self.picks[player_name][0].game))

    def __t21_game_in_progress_player_ahead_in_game_and_pool(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 25
        self.picks[player_name][0].game.team2_score = 10
        self.picks[player_name][0].game.state = "in_progress"

        self.assertTrue(self.calc.is_player_possible_to_win_game(player_name,self.picks[player_name][0].game))

    def __t21_game_in_progress_player_behind_in_game_and_pool(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 10
        self.picks[player_name][0].game.team2_score = 30
        self.picks[player_name][0].game.state = "in_progress"

        self.assertTrue(self.calc.is_player_possible_to_win_game(player_name,self.picks[player_name][0].game))


    def __t21_game_in_progress_player_ahead_in_game_and_behind_in_pool(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team2"
        self.picks[player_name][0].game.favored = "team2"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 20 
        self.picks[player_name][0].game.team2_score = 25
        self.picks[player_name][0].game.state = "in_progress"

        self.assertTrue(self.calc.is_player_possible_to_win_game(player_name,self.picks[player_name][0].game))

    def __t21_game_in_progress_player_behind_in_game_and_ahead_in_pool(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team2"
        self.picks[player_name][0].game.spread = 1.5
        self.picks[player_name][0].game.team1_score = 20 
        self.picks[player_name][0].game.team2_score = 21
        self.picks[player_name][0].game.state = "in_progress"

        self.assertTrue(self.calc.is_player_possible_to_win_game(player_name,self.picks[player_name][0].game))

    def __t21_game_not_started_player_ahead_in_game_and_pool(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 25
        self.picks[player_name][0].game.team2_score = 10
        self.picks[player_name][0].game.state = "not_started"

        self.assertTrue(self.calc.is_player_possible_to_win_game(player_name,self.picks[player_name][0].game))

    def __t21_game_not_started_player_behind_in_game_and_pool(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 10
        self.picks[player_name][0].game.team2_score = 30
        self.picks[player_name][0].game.state = "not_started"

        self.assertTrue(self.calc.is_player_possible_to_win_game(player_name,self.picks[player_name][0].game))


    def __t21_game_not_started_player_ahead_in_game_and_behind_in_pool(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team2"
        self.picks[player_name][0].game.favored = "team2"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 20 
        self.picks[player_name][0].game.team2_score = 25
        self.picks[player_name][0].game.state = "not_started"

        self.assertTrue(self.calc.is_player_possible_to_win_game(player_name,self.picks[player_name][0].game))

    def __t21_game_not_started_player_behind_in_game_and_ahead_in_pool(self):
        player_name = 'Brent H.'
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team2"
        self.picks[player_name][0].game.spread = 1.5
        self.picks[player_name][0].game.team1_score = 20 
        self.picks[player_name][0].game.team2_score = 21
        self.picks[player_name][0].game.state = "not_started"

        self.assertTrue(self.calc.is_player_possible_to_win_game(player_name,self.picks[player_name][0].game))

    def __t22_invalid_player_name(self):
        with self.assertRaises(AssertionError):
            self.calc.get_number_of_projected_wins("playerxxx")

    def __t22_no_games_started(self):
        saved_states = self.__modify_game_states(['not_started']*10)
        self.assertEqual(self.calc.get_number_of_projected_wins('Brent H.'),10)
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t22_some_games_in_progress(self):
        num_projected_wins_last_7_games_2013_week_1 = 6

        states = ['not_started']*3 + ['in_progress']*7
        saved_states = self.__modify_game_states(states)
        self.assertEqual(self.calc.get_number_of_projected_wins('Brent H.'),num_projected_wins_last_7_games_2013_week_1)
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t22_mixed_game_states(self):
        num_projected_wins_first_3_games = 2
        num_projected_wins_next_3_games = 3
        num_projected_wins_last_4_games = 2
        num_projected_wins_2013_week_1 = num_projected_wins_first_3_games + num_projected_wins_next_3_games + num_projected_wins_last_4_games

        states = ['final']*3 + ['not_started']*3 + ['in_progress']*4
        saved_states = self.__modify_game_states(states)
        self.assertEqual(self.calc.get_number_of_projected_wins('Brent H.'),num_projected_wins_2013_week_1)
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t22_all_games_final(self):
        num_projected_wins_2013_week_1 = 6
        self.assertEqual(self.calc.get_number_of_projected_wins('Byron R.'),num_projected_wins_2013_week_1)

    def __t22_player_with_no_picks(self):
        saved = self.__make_all_player_picks_not_entered('Brent H.')
        self.assertEqual(self.calc.get_number_of_projected_wins('Brent H.'),0)
        self.__restore_player_picks_winners('Brent H.',saved)

    def __t22_game_final_player_0_wins(self):
        self.__make_dale_0_wins()
        saved_states = self.__modify_game_states(['final']*10)
        self.assertEqual(self.calc.get_number_of_projected_wins('Dale R.'),0)
        self.__restore_dale_picks()
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t22_game_final_player_10_wins(self):
        self.__make_william_10_wins()
        saved_states = self.__modify_game_states(['final']*10)
        self.assertEqual(self.calc.get_number_of_projected_wins('William M.'),10)
        self.__restore_william_picks()
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t22_game_in_progress_player_0_wins(self):
        self.__make_dale_0_wins()
        saved_states = self.__modify_game_states(['in_progress']*10)
        self.assertEqual(self.calc.get_number_of_projected_wins('Dale R.'),0)
        self.__restore_dale_picks()
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t22_game_in_progress_player_10_wins(self):
        self.__make_william_10_wins()
        saved_states = self.__modify_game_states(['in_progress']*10)
        self.assertEqual(self.calc.get_number_of_projected_wins('William M.'),10)
        self.__restore_william_picks()
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t22_game_not_started_player_0_wins(self):
        self.__make_dale_0_wins()
        saved_states = self.__modify_game_states(['not_started']*10)
        self.assertEqual(self.calc.get_number_of_projected_wins('Dale R.'),10)
        self.__restore_dale_picks()
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t22_game_not_started_player_10_wins(self):
        self.__make_william_10_wins()
        saved_states = self.__modify_game_states(['not_started']*10)
        self.assertEqual(self.calc.get_number_of_projected_wins('William M.'),10)
        self.__restore_william_picks()
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t23_invalid_player_name(self):
        with self.assertRaises(AssertionError):
            self.calc.get_number_of_possible_wins("playerxxx")

    def __t23_no_games_started(self):
        saved_states = self.__modify_game_states(['not_started']*10)
        self.assertEqual(self.calc.get_number_of_possible_wins('Brent H.'),10)
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t23_some_games_in_progress(self):
        states = ['not_started']*3 + ['in_progress']*7
        saved_states = self.__modify_game_states(states)
        self.assertEqual(self.calc.get_number_of_possible_wins('Brent H.'),10)
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t23_mixed_game_states(self):
        num_possible_wins_first_3_games = 2
        num_possible_wins_next_3_games = 3
        num_possible_wins_last_4_games = 4
        num_possible_wins_2013_week_1 = num_possible_wins_first_3_games + num_possible_wins_next_3_games + num_possible_wins_last_4_games

        states = ['final']*3 + ['not_started']*3 + ['in_progress']*4
        saved_states = self.__modify_game_states(states)
        self.assertEqual(self.calc.get_number_of_possible_wins('Brent H.'),num_possible_wins_2013_week_1)
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t23_all_games_final(self):
        num_possible_wins_2013_week_1 = 6
        self.assertEqual(self.calc.get_number_of_possible_wins('Byron R.'),num_possible_wins_2013_week_1)

    def __t23_player_with_no_picks(self):
        saved = self.__make_all_player_picks_not_entered('Brent H.')
        self.assertEqual(self.calc.get_number_of_possible_wins('Brent H.'),0)
        self.__restore_player_picks_winners('Brent H.',saved)

    def __t23_game_final_player_0_wins(self):
        self.__make_dale_0_wins()
        saved_states = self.__modify_game_states(['final']*10)
        self.assertEqual(self.calc.get_number_of_possible_wins('Dale R.'),0)
        self.__restore_dale_picks()
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t23_game_final_player_10_wins(self):
        self.__make_william_10_wins()
        saved_states = self.__modify_game_states(['final']*10)
        self.assertEqual(self.calc.get_number_of_possible_wins('William M.'),10)
        self.__restore_william_picks()
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t23_game_in_progress_player_0_wins(self):
        self.__make_dale_0_wins()
        saved_states = self.__modify_game_states(['in_progress']*10)
        self.assertEqual(self.calc.get_number_of_possible_wins('Dale R.'),10)
        self.__restore_dale_picks()
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t23_game_in_progress_player_10_wins(self):
        self.__make_william_10_wins()
        saved_states = self.__modify_game_states(['in_progress']*10)
        self.assertEqual(self.calc.get_number_of_possible_wins('William M.'),10)
        self.__restore_william_picks()
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t23_game_not_started_player_0_wins(self):
        self.__make_dale_0_wins()
        saved_states = self.__modify_game_states(['not_started']*10)
        self.assertEqual(self.calc.get_number_of_possible_wins('Dale R.'),10)
        self.__restore_dale_picks()
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t23_game_not_started_player_10_wins(self):
        self.__make_william_10_wins()
        saved_states = self.__modify_game_states(['not_started']*10)
        self.assertEqual(self.calc.get_number_of_possible_wins('William M.'),10)
        self.__restore_william_picks()
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t24_no_games_started(self):
        saved_states = self.__modify_game_states(['not_started']*10)
        self.assertFalse(self.calc.all_games_final())
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t24_some_games_in_progress(self):
        states = ['not_started']*3 + ['in_progress']*7
        saved_states = self.__modify_game_states(states)
        self.assertFalse(self.calc.all_games_final())
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t24_mixed_game_states(self):
        states = ['final']*3 + ['not_started']*3 + ['in_progress']*4
        saved_states = self.__modify_game_states(states)
        self.assertFalse(self.calc.all_games_final())
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t24_all_games_final(self):
        self.assertTrue(self.calc.all_games_final())

    def __t25_no_games_started(self):
        saved_states = self.__modify_game_states(['not_started']*10)
        self.assertTrue(self.calc.no_games_started())
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t25_some_games_in_progress(self):
        states = ['not_started']*3 + ['in_progress']*7
        saved_states = self.__modify_game_states(states)
        self.assertFalse(self.calc.no_games_started())
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t25_mixed_game_states(self):
        states = ['final']*3 + ['not_started']*3 + ['in_progress']*4
        saved_states = self.__modify_game_states(states)
        self.assertFalse(self.calc.no_games_started())
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t25_all_games_final(self):
        self.assertFalse(self.calc.no_games_started())

    def __t26_no_games_started(self):
        saved_states = self.__modify_game_states(['not_started']*10)
        self.assertFalse(self.calc.at_least_one_game_in_progress())
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t26_one_game_in_progress(self):
        states = ['not_started']*1 + ['in_progress']*9
        saved_states = self.__modify_game_states(states)
        self.assertTrue(self.calc.at_least_one_game_in_progress())
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t26_some_games_in_progress(self):
        states = ['not_started']*3 + ['in_progress']*7
        saved_states = self.__modify_game_states(states)
        self.assertTrue(self.calc.at_least_one_game_in_progress())
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t26_mixed_game_states(self):
        states = ['final']*3 + ['not_started']*3 + ['in_progress']*4
        saved_states = self.__modify_game_states(states)
        self.assertTrue(self.calc.at_least_one_game_in_progress())
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t26_all_games_final(self):
        self.assertFalse(self.calc.at_least_one_game_in_progress())

    def __t27_no_games_started(self):
        saved_states = self.__modify_game_states(['not_started']*10)
        self.assertEqual(self.calc.get_summary_state_of_all_games(),"not_started")
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t27_one_game_in_progress(self):
        states = ['not_started']*1 + ['in_progress']*9
        saved_states = self.__modify_game_states(states)
        self.assertEqual(self.calc.get_summary_state_of_all_games(),"in_progress")
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t27_some_games_in_progress(self):
        states = ['not_started']*3 + ['in_progress']*7
        saved_states = self.__modify_game_states(states)
        self.assertEqual(self.calc.get_summary_state_of_all_games(),"in_progress")
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t27_mixed_game_states(self):
        states = ['final']*3 + ['not_started']*3 + ['in_progress']*4
        saved_states = self.__modify_game_states(states)
        self.assertEqual(self.calc.get_summary_state_of_all_games(),"in_progress")
        ignore_return_value = self.__modify_game_states(saved_states)

    def __t27_all_games_final(self):
        self.assertEqual(self.calc.get_summary_state_of_all_games(),"final")

    def __t28_game_none(self):
        with self.assertRaises(AssertionError):
            self.calc.get_game_result_string("Brent H.",None)

    def __t28_invalid_player_name(self):
        with self.assertRaises(AssertionError):
            self.calc.get_game_result_string("playerxxx",self.games[0])

    def __t28_player_pick_missing(self):
        player_name = "Brent H."
        self.picks[player_name][0].winner = None
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 10
        self.picks[player_name][0].game.team2_score = 25
        self.picks[player_name][0].game.state = "in_progress"

        self.assertEqual(self.calc.get_game_result_string(player_name,self.picks[player_name][0].game),"loss")

    def __t28_game_win(self):
        player_name = "Brent H."
        self.picks[player_name][0].winner = "team2"
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 10
        self.picks[player_name][0].game.team2_score = 25
        self.picks[player_name][0].game.state = "final"

        self.assertEqual(self.calc.get_game_result_string(player_name,self.picks[player_name][0].game),"win")

    def __t28_game_loss(self):
        player_name = "Brent H."
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 10
        self.picks[player_name][0].game.team2_score = 25
        self.picks[player_name][0].game.state = "final"

        self.assertEqual(self.calc.get_game_result_string(player_name,self.picks[player_name][0].game),"loss")

    def __t28_game_ahead(self):
        player_name = "Brent H."
        self.picks[player_name][0].winner = "team2"
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 10
        self.picks[player_name][0].game.team2_score = 25
        self.picks[player_name][0].game.state = "in_progress"

        self.assertEqual(self.calc.get_game_result_string(player_name,self.picks[player_name][0].game),"ahead")

    def __t28_game_behind(self):
        player_name = "Brent H."
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 10
        self.picks[player_name][0].game.team2_score = 25
        self.picks[player_name][0].game.state = "in_progress"

        self.assertEqual(self.calc.get_game_result_string(player_name,self.picks[player_name][0].game),"behind")

    def __t28_game_not_started(self):
        player_name = "Brent H."
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 10
        self.picks[player_name][0].game.team2_score = 25
        self.picks[player_name][0].game.state = "not_started"

        self.assertEqual(self.calc.get_game_result_string(player_name,self.picks[player_name][0].game),"")

    def __t29_game_none(self):
        with self.assertRaises(AssertionError):
            self.calc.get_favored_team_name(None)

    def __t29_invalid_favored(self):
        player_name = "Brent H."
        self.picks[player_name][0].game.favored = "invalid"
        with self.assertRaises(AssertionError):
            self.calc.get_favored_team_name(self.picks[player_name][0].game)

    def __t29_team1_favored(self):
        game = self.__find_game("LSU","TCU")
        self.assertEqual(self.calc.get_favored_team_name(game),"LSU")

    def __t29_team2_favored(self):
        game = self.__find_game("North Carolina","South Carolina")
        self.assertEqual(self.calc.get_favored_team_name(game),"South Carolina")

    def __t30_game_none(self):
        with self.assertRaises(AssertionError):
            self.calc.get_game_score_spread(None)

    def __t30_game_not_started(self):
        player_name = "Brent H."
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 10
        self.picks[player_name][0].game.team2_score = 25
        self.picks[player_name][0].game.state = "not_started"

        with self.assertRaises(AssertionError):
            self.calc.get_game_score_spread(self.picks[player_name][0].game)

    def __t30_game_in_progress(self):
        player_name = "Brent H."
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 10
        self.picks[player_name][0].game.team2_score = 25
        self.picks[player_name][0].game.state = "in_progress"

        self.assertEqual(self.calc.get_game_score_spread(self.picks[player_name][0].game),15)

    def __t30_tied_score(self):
        player_name = "Brent H."
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 13 
        self.picks[player_name][0].game.team2_score = 13
        self.picks[player_name][0].game.state = "final"

        self.assertEqual(self.calc.get_game_score_spread(self.picks[player_name][0].game),0)

    def __t30_team1_ahead(self):
        player_name = "Brent H."
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 24
        self.picks[player_name][0].game.team2_score = 11
        self.picks[player_name][0].game.state = "final"

        self.assertEqual(self.calc.get_game_score_spread(self.picks[player_name][0].game),13)

    def __t30_team2_ahead(self):
        player_name = "Brent H."
        self.picks[player_name][0].winner = "team1"
        self.picks[player_name][0].game.favored = "team1"
        self.picks[player_name][0].game.spread = 5.5
        self.picks[player_name][0].game.team1_score = 9
        self.picks[player_name][0].game.team2_score = 31
        self.picks[player_name][0].game.state = "final"
        self.assertEqual(self.calc.get_game_score_spread(self.picks[player_name][0].game),22)

    def __t31_pick_none(self):
        with self.assertRaises(AssertionError):
            self.calc.get_pick_score_spread(None)

    def __t31_pick_team1_score_none(self):
        player_name = "Brent H."
        self.picks[player_name][0].team1_score = None
        self.picks[player_name][0].team2_score = 10
        with self.assertRaises(AssertionError):
            self.calc.get_pick_score_spread(self.picks[player_name][0])

    def __t31_pick_team2_score_none(self):
        player_name = "Brent H."
        self.picks[player_name][0].team1_score = 10
        self.picks[player_name][0].team2_score = None
        with self.assertRaises(AssertionError):
            self.calc.get_pick_score_spread(self.picks[player_name][0])

    def __t31_tied_score(self):
        player_name = "Brent H."
        self.picks[player_name][0].team1_score = 15 
        self.picks[player_name][0].team2_score = 15
        self.assertEqual(self.calc.get_pick_score_spread(self.picks[player_name][0]),0)

    def __t31_team1_ahead(self):
        player_name = "Brent H."
        self.picks[player_name][0].team1_score = 20 
        self.picks[player_name][0].team2_score = 11
        self.assertEqual(self.calc.get_pick_score_spread(self.picks[player_name][0]),9)

    def __t31_team2_ahead(self):
        player_name = "Brent H."
        self.picks[player_name][0].team1_score = 3
        self.picks[player_name][0].team2_score = 11
        self.assertEqual(self.calc.get_pick_score_spread(self.picks[player_name][0]),8)

    def __t32_featured_game(self):
        game = self.calc.get_featured_game()
        self.assertEqual(game.number,10)

    def __t32_featured_game_missing(self):
        for i,game in enumerate(self.games):
            if game.number == 10:
                self.games[i].number = 11
        with self.assertRaises(AssertionError):
            self.calc.get_featured_game()
        self.games[i].number = 10

