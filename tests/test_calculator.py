from code.update import *
from code.calculator import *
from code.database import *
from models.games import *
from models.picks import *
import time
import logging
import unittest
import copy

# TODO:  add more bad game key tests


class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.__load_test_data()

    def __load_test_data(self):
        database = Database()
        self.week1 = database.load_week_data(2013,1)
        self.calc = CalculateResults(self.week1)
        self.week2 = database.load_week_data(2013,2)

    # function name decode:  
    # test_ : each function to test must start with test_ (unittest requirement)
    # _t<number>_ : unique identifier used to specify this test function
    # _<name> : this is the name of the function in calculator.py that is being tested
    def test_t1_get_team_player_picked_to_win(self):
        self.__t1_invalid_player()
        self.__t1_invalid_game()
        self.__t1_game_none()
        self.__t1_team1_winner()
        self.__t1_team2_winner()

    def test_t2_get_team_name_player_picked_to_win(self):
        self.__t2_invalid_player()
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
        self.__t13_game_invalid()
        self.__t13_invalid_player()
        self.__t13_player_missing_all_week_picks()
        self.__t13_player_missing_pick_for_game()
        self.__t13_player_missing_pick_winner()
        self.__t13_player_made_pick()

    def test_t14_did_player_win_game(self):
        self.__t14_game_none()
        self.__t14_invalid_player()
        self.__t14_player_missing_pick()
        self.__t14_game_in_progress()
        self.__t14_game_not_started()
        self.__t14_player_won_game()
        self.__t14_player_lost_game()

    def test_t15_did_player_lose_game(self):
        self.__t15_game_none()
        self.__t15_invalid_player()
        self.__t15_player_missing_pick()
        self.__t15_game_in_progress()
        self.__t15_game_not_started()
        self.__t15_player_won_game()
        self.__t15_player_lost_game()

    def test_t16_get_number_of_wins(self):
        self.__t16_invalid_player()
        self.__t16_no_games_started()
        self.__t16_some_games_in_progress()
        self.__t16_mixed_game_states()
        self.__t16_all_games_final()
        self.__t16_player_with_no_picks()
        self.__t16_player_0_wins()
        self.__t16_player_10_wins()

    def test_t17_get_number_of_losses(self):
        self.__t17_invalid_player()
        self.__t17_no_games_started()
        self.__t17_some_games_in_progress()
        self.__t17_mixed_game_states()
        self.__t17_all_games_final()
        self.__t17_player_with_no_picks()
        self.__t17_player_0_losses()
        self.__t17_player_10_losses()

    def test_t18_is_player_winning_game(self):
        self.__t18_game_none()
        self.__t18_invalid_player()
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
        self.__t19_invalid_player()
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
        self.__t20_invalid_player()
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
        self.__t21_invalid_player()
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
        self.__t23_invalid_player()
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
        self.__t28_invalid_player()
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

    def __t1_invalid_player(self):
        game_key = self.__get_a_valid_game_key()
        with self.assertRaises(KeyError):
            self.calc.get_team_player_picked_to_win("bad key",game_key)

    def __t1_invalid_game(self):
        invalid_game_key = self.__get_a_valid_game2_key()
        valid_player_key = self.week1.get_player_key("Brent H.")
        with self.assertRaises(AssertionError):
            self.calc.get_team_player_picked_to_win(valid_player_key,invalid_game_key)

    def __t1_game_none(self):
        valid_player_key = self.week1.get_player_key("Brent H.")
        with self.assertRaises(AssertionError):
            self.calc.get_team_player_picked_to_win(valid_player_key,None)

    def __t1_team2_winner(self):
        game_key = self.__find_game_key("North Carolina","South Carolina")
        brent_key = self.week1.get_player_key("Brent H.")
        team = self.calc.get_team_player_picked_to_win(brent_key,game_key)
        self.assertEqual(team,"team2")

    def __t1_team1_winner(self):
        game_key = self.__find_game_key("LSU","TCU")
        brent_key = self.week1.get_player_key("Brent H.")
        team = self.calc.get_team_player_picked_to_win(brent_key,game_key)
        self.assertEqual(team,"team1")

    def __t2_invalid_player(self):
        game_key = self.__get_a_valid_game_key()
        with self.assertRaises(KeyError):
            self.calc.get_team_name_player_picked_to_win("bad player key",game_key)

    def __t2_invalid_game(self):
        invalid_game_key = self.__get_a_valid_game2_key()
        valid_player_key = self.week1.get_player_key("Brent H.")
        with self.assertRaises(AssertionError):
            self.calc.get_team_name_player_picked_to_win(valid_player_key,invalid_game_key)

    def __t2_game_none(self):
        valid_player_key = self.week1.get_player_key("Brent H.")
        with self.assertRaises(AssertionError):
            self.calc.get_team_name_player_picked_to_win(valid_player_key,None)

    def __t2_team2_winner(self):
        game_key = self.__find_game_key("North Carolina","South Carolina")
        brent_key = self.week1.get_player_key("Brent H.")
        team = self.calc.get_team_name_player_picked_to_win(brent_key,game_key)
        self.assertEqual(team,"South Carolina")

    def __t2_team1_winner(self):
        game_key = self.__find_game_key("LSU","TCU")
        brent_key = self.week1.get_player_key("Brent H.")
        team = self.calc.get_team_name_player_picked_to_win(brent_key,game_key)
        self.assertEqual(team,"LSU")

    def __t3_bad_game_favored_value(self):
        g = Game()
        g.team1_score = 0
        g.team2_score = 0
        g.favored = "bad value"
        g.spread = 0.5
        game_key = self.__edit_existing_game(g)
        with self.assertRaises(AssertionError):
            self.calc.is_team1_winning_pool(game_key)
        self.__restore_game(game_key)

    def __t3_team1_ahead(self):
        g = Game()
        g.team1_score = 20 
        g.team2_score = 10 
        g.favored = "team1"
        g.spread = 5.5 
        game_key = self.__edit_existing_game(g)
        self.assertTrue(self.calc.is_team1_winning_pool(game_key))
        self.__restore_game(game_key)

    def __t3_team1_behind(self):
        g = Game()
        g.team1_score = 10 
        g.team2_score = 20 
        g.favored = "team1"
        g.spread = 5.5 
        game_key = self.__edit_existing_game(g)
        self.assertFalse(self.calc.is_team1_winning_pool(game_key))
        self.__restore_game(game_key)

    def __t3_team1_ahead_in_pool_behind_in_game(self):
        g = Game()
        g.team1_score = 14 
        g.team2_score = 17 
        g.favored = "team2"
        g.spread = 3.5 
        game_key = self.__edit_existing_game(g)
        self.assertTrue(self.calc.is_team1_winning_pool(game_key))
        self.__restore_game(game_key)

    def __t3_team1_behind_in_pool_ahead_in_game(self):
        g = Game()
        g.team1_score = 21 
        g.team2_score = 17 
        g.favored = "team1"
        g.spread = 4.5 
        game_key = self.__edit_existing_game(g)
        self.assertFalse(self.calc.is_team1_winning_pool(game_key))
        self.__restore_game(game_key)

    def __t3_team1_boundary_case1(self):
        g = Game()
        g.team1_score = 17 
        g.team2_score = 16 
        g.favored = "team1"
        g.spread = 0.5 
        game_key = self.__edit_existing_game(g)
        self.assertTrue(self.calc.is_team1_winning_pool(game_key))
        self.__restore_game(game_key)

    def __t3_team1_boundary_case2(self):
        g = Game()
        g.team1_score = 16 
        g.team2_score = 17 
        g.favored = "team1"
        g.spread = 0.5 
        game_key = self.__edit_existing_game(g)
        self.assertFalse(self.calc.is_team1_winning_pool(game_key))
        self.__restore_game(game_key)

    def __t3_team1_boundary_case3(self):
        g = Game()
        g.team1_score = 17 
        g.team2_score = 16 
        g.favored = "team2"
        g.spread = 0.5 
        game_key = self.__edit_existing_game(g)
        self.assertTrue(self.calc.is_team1_winning_pool(game_key))
        self.__restore_game(game_key)

    def __t3_team1_boundary_case4(self):
        g = Game()
        g.team1_score = 16 
        g.team2_score = 17 
        g.favored = "team2"
        g.spread = 0.5 
        game_key = self.__edit_existing_game(g)
        self.assertFalse(self.calc.is_team1_winning_pool(game_key))
        self.__restore_game(game_key)

    def __t4_bad_game_favored_value(self):
        g = Game()
        g.team1_score = 0
        g.team2_score = 0
        g.favored = "bad value"
        g.spread = 0.5
        game_key = self.__edit_existing_game(g)
        with self.assertRaises(AssertionError):
            self.calc.is_team2_winning_pool(game_key)
        self.__restore_game(game_key)

    def __t4_team2_ahead(self):
        g = Game()
        g.team1_score = 10 
        g.team2_score = 20 
        g.favored = "team2"
        g.spread = 5.5 
        game_key = self.__edit_existing_game(g)
        self.assertTrue(self.calc.is_team2_winning_pool(game_key))
        self.__restore_game(game_key)

    def __t4_team2_behind(self):
        g = Game()
        g.team1_score = 20 
        g.team2_score = 10 
        g.favored = "team2"
        g.spread = 5.5 
        game_key = self.__edit_existing_game(g)
        self.assertFalse(self.calc.is_team2_winning_pool(game_key))
        self.__restore_game(game_key)

    def __t4_team2_ahead_in_pool_behind_in_game(self):
        g = Game()
        g.team1_score = 17 
        g.team2_score = 14 
        g.favored = "team1"
        g.spread = 3.5 
        game_key = self.__edit_existing_game(g)
        self.assertTrue(self.calc.is_team2_winning_pool(game_key))
        self.__restore_game(game_key)

    def __t4_team2_behind_in_pool_ahead_in_game(self):
        g = Game()
        g.team1_score = 17
        g.team2_score = 21
        g.favored = "team2"
        g.spread = 4.5 
        game_key = self.__edit_existing_game(g)
        self.assertFalse(self.calc.is_team2_winning_pool(game_key))
        self.__restore_game(game_key)

    def __t4_team2_boundary_case1(self):
        g = Game()
        g.team1_score = 16 
        g.team2_score = 17 
        g.favored = "team2"
        g.spread = 0.5 
        game_key = self.__edit_existing_game(g)
        self.assertTrue(self.calc.is_team2_winning_pool(game_key))
        self.__restore_game(game_key)

    def __t4_team2_boundary_case2(self):
        g = Game()
        g.team1_score = 17 
        g.team2_score = 16 
        g.favored = "team2"
        g.spread = 0.5 
        game_key = self.__edit_existing_game(g)
        self.assertFalse(self.calc.is_team2_winning_pool(game_key))
        self.__restore_game(game_key)

    def __t4_team2_boundary_case3(self):
        g = Game()
        g.team1_score = 16 
        g.team2_score = 17 
        g.favored = "team1"
        g.spread = 0.5 
        game_key = self.__edit_existing_game(g)
        self.assertTrue(self.calc.is_team2_winning_pool(game_key))
        self.__restore_game(game_key)

    def __t4_team2_boundary_case4(self):
        g = Game()
        g.team1_score = 17 
        g.team2_score = 16 
        g.favored = "team1"
        g.spread = 0.5 
        game_key = self.__edit_existing_game(g)
        self.assertFalse(self.calc.is_team2_winning_pool(game_key))
        self.__restore_game(game_key)

    def __t5_game_none(self):
        with self.assertRaises(Exception):
            self.calc.get_pool_game_winner(None)

    def __t5_game_in_progress(self):
        g = Game()
        g.state = "in_progress"
        game_key = self.__edit_existing_game(g)
        self.assertIsNone(self.calc.get_pool_game_winner(game_key))
        self.__restore_game(game_key)

    def __t5_game_not_started(self):
        g = Game()
        g.state = "not_started"
        game_key = self.__edit_existing_game(g)
        self.assertIsNone(self.calc.get_pool_game_winner(game_key))
        self.__restore_game(game_key)

    def __t5_team1_won(self):
        g = Game()
        g.team1_score = 30 
        g.team2_score = 10 
        g.favored = "team1"
        g.spread = 10.5
        g.state = "final"
        game_key = self.__edit_existing_game(g)
        self.assertEqual(self.calc.get_pool_game_winner(game_key),"team1")
        self.__restore_game(game_key)

    def __t5_team2_won(self):
        g = Game()
        g.team1_score = 30 
        g.team2_score = 25 
        g.favored = "team1"
        g.spread = 10.5
        g.state = "final"
        game_key = self.__edit_existing_game(g)
        self.assertEqual(self.calc.get_pool_game_winner(game_key),"team2")
        self.__restore_game(game_key)

    def __t6_game_none(self):
        with self.assertRaises(Exception):
            self.calc.get_pool_game_winner_team_name(None)

    def __t6_game_in_progress(self):
        g = Game()
        g.state = "in_progress"
        game_key = self.__edit_existing_game(g)
        self.assertIsNone(self.calc.get_pool_game_winner_team_name(game_key))
        self.__restore_game(game_key)

    def __t6_game_not_started(self):
        g = Game()
        g.state = "not_started"
        game_key = self.__edit_existing_game(g)
        self.assertIsNone(self.calc.get_pool_game_winner_team_name(game_key))
        self.__restore_game(game_key)

    def __t6_team1_won(self):
        game_key = self.__find_game_key("LSU","TCU")
        self.assertEqual(self.calc.get_pool_game_winner_team_name(game_key),"LSU")

    def __t6_team2_won(self):
        game_key = self.__find_game_key("Boise State","Washington")
        self.assertEqual(self.calc.get_pool_game_winner_team_name(game_key),"Washington")

    def __t7_game_none(self):
        with self.assertRaises(Exception):
            self.calc.get_game_winner(None)

    def __t7_game_in_progress(self):
        g = Game()
        g.state = "in_progress"
        game_key = self.__edit_existing_game(g)
        self.assertIsNone(self.calc.get_game_winner(game_key))
        self.__restore_game(game_key)

    def __t7_game_not_started(self):
        g = Game()
        g.state = "not_started"
        game_key = self.__edit_existing_game(g)
        self.assertIsNone(self.calc.get_game_winner(game_key))
        self.__restore_game(game_key)

    def __t7_same_score(self):
        g = Game()
        g.team1_score = 21
        g.team2_score = 21
        g.favored = "team1"
        g.spread = 10.5
        g.state = "final"
        game_key = self.__edit_existing_game(g)
        with self.assertRaises(AssertionError):
            self.calc.get_game_winner(game_key)
        self.__restore_game(game_key)

    def __t7_team1_won(self):
        g = Game()
        g.team1_score = 31
        g.team2_score = 21
        g.favored = "team1"
        g.spread = 10.5
        g.state = "final"
        game_key = self.__edit_existing_game(g)
        self.assertEqual(self.calc.get_game_winner(game_key),"team1")
        self.__restore_game(game_key)

    def __t7_team2_won(self):
        g = Game()
        g.team1_score = 10 
        g.team2_score = 24 
        g.favored = "team2"
        g.spread = 14.5
        g.state = "final"
        game_key = self.__edit_existing_game(g)
        self.assertEqual(self.calc.get_game_winner(game_key),"team2")
        self.__restore_game(game_key)

    def __t7_team1_won_but_not_favored(self):
        g = Game()
        g.team1_score = 24
        g.team2_score = 21
        g.favored = "team2"
        g.spread = 5.5
        g.state = "final"
        game_key = self.__edit_existing_game(g)
        self.assertEqual(self.calc.get_game_winner(game_key),"team1")
        self.__restore_game(game_key)

    def __t7_team2_won_but_not_favored(self):
        g = Game()
        g.team1_score = 41
        g.team2_score = 48
        g.favored = "team1"
        g.spread = 7.5
        g.state = "final"
        game_key = self.__edit_existing_game(g)
        self.assertEqual(self.calc.get_game_winner(game_key),"team2")
        self.__restore_game(game_key)

    def __t8_game_none(self):
        with self.assertRaises(Exception):
            self.calc.get_game_winner_team_name(None)

    def __t8_game_in_progress(self):
        g = Game()
        g.state = "in_progress"
        game_key = self.__edit_existing_game(g)
        self.assertIsNone(self.calc.get_game_winner_team_name(game_key))
        self.__restore_game(game_key)

    def __t8_game_not_started(self):
        g = Game()
        g.state = "not_started"
        game_key = self.__edit_existing_game(g)
        self.assertIsNone(self.calc.get_game_winner_team_name(game_key))
        self.__restore_game(game_key)

    def __t8_same_score(self):
        g = Game()
        g.team1_score = 21
        g.team2_score = 21
        g.favored = "team1"
        g.spread = 10.5
        g.state = "final"
        game_key = self.__edit_existing_game(g)
        with self.assertRaises(AssertionError):
            self.calc.get_game_winner_team_name(game_key)
        self.__restore_game(game_key)

    def __t8_team1_won(self):
        game_key = self.__find_game_key("Penn State","Syracuse")
        self.assertEqual(self.calc.get_game_winner_team_name(game_key),"Penn State")

    def __t8_team2_won(self):
        game_key = self.__find_game_key("Georgia","Clemson")
        self.assertEqual(self.calc.get_game_winner_team_name(game_key),"Clemson")

    def __t9_game_none(self):
        with self.assertRaises(Exception):
            self.calc.get_team_winning_pool_game(None)

    def __t9_game_final(self):
        g = Game()
        g.state = "final"
        game_key = self.__edit_existing_game(g)
        self.assertIsNone(self.calc.get_team_winning_pool_game(game_key))
        self.__restore_game(game_key)

    def __t9_game_not_started(self):
        g = Game()
        g.state = "not_started"
        game_key = self.__edit_existing_game(g)
        self.assertIsNone(self.calc.get_team_winning_pool_game(game_key))
        self.__restore_game(game_key)

    def __t9_same_score(self):
        g = Game()
        g.team1_score = 35
        g.team2_score = 35
        g.favored = "team1"
        g.spread = 0.5
        g.state = "in_progress"
        game_key = self.__edit_existing_game(g)
        self.assertEqual(self.calc.get_team_winning_pool_game(game_key),"team2")
        self.__restore_game(game_key)

    def __t9_team1_ahead(self):
        g = Game()
        g.team1_score = 44
        g.team2_score = 48
        g.favored = "team2"
        g.spread = 4.5
        g.state = "in_progress"
        game_key = self.__edit_existing_game(g)
        self.assertEqual(self.calc.get_team_winning_pool_game(game_key),"team1")
        self.__restore_game(game_key)

    def __t9_team2_ahead(self):
        g = Game()
        g.team1_score = 21
        g.team2_score = 18
        g.favored = "team1"
        g.spread = 3.5
        g.state = "in_progress"
        game_key = self.__edit_existing_game(g)
        self.assertEqual(self.calc.get_team_winning_pool_game(game_key),"team2")
        self.__restore_game(game_key)

    def __t10_game_none(self):
        with self.assertRaises(Exception):
            self.calc.get_team_name_winning_pool_game(None)

    def __t10_game_final(self):
        g = Game()
        g.state = "final"
        game_key = self.__edit_existing_game(g)
        self.assertIsNone(self.calc.get_team_name_winning_pool_game(game_key))
        self.__restore_game(game_key)

    def __t10_game_not_started(self):
        g = Game()
        g.state = "not_started"
        game_key = self.__edit_existing_game(g)
        self.assertIsNone(self.calc.get_team_name_winning_pool_game(game_key))
        self.__restore_game(game_key)

    def __t10_same_score(self):
        g = Game()
        g.team1 = self.__find_team("Georgia Tech")
        g.team2 = self.__find_team("Clemson")
        g.team1_score = 35
        g.team2_score = 35
        g.favored = "team1"
        g.spread = 0.5
        g.state = "in_progress"
        game_key = self.__edit_existing_game(g)
        self.assertEqual(self.calc.get_team_name_winning_pool_game(game_key),"Clemson")
        self.__restore_game(game_key)

    def __t10_team1_ahead(self):
        g = Game()
        g.team1 = self.__find_team("Georgia Tech")
        g.team2 = self.__find_team("Clemson")
        g.team1_score = 44
        g.team2_score = 48
        g.favored = "team2"
        g.spread = 4.5
        g.state = "in_progress"
        game_key = self.__edit_existing_game(g)
        self.assertEqual(self.calc.get_team_name_winning_pool_game(game_key),"Georgia Tech")
        self.__restore_game(game_key)

    def __t10_team2_ahead(self):
        g = Game()
        g.team1 = self.__find_team("Georgia Tech")
        g.team2 = self.__find_team("Clemson")
        g.team1_score = 21
        g.team2_score = 18
        g.favored = "team1"
        g.spread = 3.5
        g.state = "in_progress"
        game_key = self.__edit_existing_game(g)
        self.assertEqual(self.calc.get_team_name_winning_pool_game(game_key),"Clemson")
        self.__restore_game(game_key)

    def __t11_game_none(self):
        with self.assertRaises(Exception):
            self.calc.get_team_winning_game(None)

    def __t11_game_final(self):
        g = Game()
        g.state = "final"
        game_key = self.__edit_existing_game(g)
        self.assertIsNone(self.calc.get_team_winning_game(game_key))
        self.__restore_game(game_key)

    def __t11_game_not_started(self):
        g = Game()
        g.state = "not_started"
        game_key = self.__edit_existing_game(g)
        self.assertIsNone(self.calc.get_team_winning_game(game_key))
        self.__restore_game(game_key)

    def __t11_same_score(self):
        g = Game()
        g.team1 = self.__find_team("Georgia Tech")
        g.team2 = self.__find_team("Clemson")
        g.team1_score = 35
        g.team2_score = 35
        g.favored = "team1"
        g.spread = 0.5
        g.state = "in_progress"
        game_key = self.__edit_existing_game(g)
        self.assertEqual(self.calc.get_team_winning_game(game_key),"tied")
        self.__restore_game(game_key)

    def __t11_team1_ahead(self):
        g = Game()
        g.team1 = self.__find_team("Georgia Tech")
        g.team2 = self.__find_team("Clemson")
        g.team1_score = 31
        g.team2_score = 24
        g.favored = "team2"
        g.spread = 4.5
        g.state = "in_progress"
        game_key = self.__edit_existing_game(g)
        self.assertEqual(self.calc.get_team_winning_game(game_key),"team1")
        self.__restore_game(game_key)

    def __t11_team2_ahead(self):
        g = Game()
        g.team1 = self.__find_team("Georgia Tech")
        g.team2 = self.__find_team("Clemson")
        g.team1_score = 17
        g.team2_score = 31
        g.favored = "team1"
        g.spread = 3.5
        g.state = "in_progress"
        game_key = self.__edit_existing_game(g)
        self.assertEqual(self.calc.get_team_winning_game(game_key),"team2")
        self.__restore_game(game_key)

    def __t12_game_none(self):
        with self.assertRaises(Exception):
            self.calc.get_team_name_winning_game(None)

    def __t12_game_final(self):
        g = Game()
        g.state = "final"
        game_key = self.__edit_existing_game(g)
        self.assertIsNone(self.calc.get_team_name_winning_game(game_key))
        self.__restore_game(game_key)

    def __t12_game_not_started(self):
        g = Game()
        g.state = "not_started"
        game_key = self.__edit_existing_game(g)
        self.assertIsNone(self.calc.get_team_name_winning_game(game_key))
        self.__restore_game(game_key)

    def __t12_same_score(self):
        g = Game()
        g.team1 = self.__find_team("Georgia Tech")
        g.team2 = self.__find_team("Clemson")
        g.team1_score = 35
        g.team2_score = 35
        g.favored = "team1"
        g.spread = 0.5
        g.state = "in_progress"
        game_key = self.__edit_existing_game(g)
        self.assertEqual(self.calc.get_team_name_winning_game(game_key),"tied")
        self.__restore_game(game_key)

    def __t12_team1_ahead(self):
        g = Game()
        g.team1 = self.__find_team("Georgia Tech")
        g.team2 = self.__find_team("Clemson")
        g.team1_score = 31
        g.team2_score = 24
        g.favored = "team2"
        g.spread = 4.5
        g.state = "in_progress"
        game_key = self.__edit_existing_game(g)
        self.assertEqual(self.calc.get_team_name_winning_game(game_key),"Georgia Tech")
        self.__restore_game(game_key)

    def __t12_team2_ahead(self):
        g = Game()
        g.team1 = self.__find_team("Georgia Tech")
        g.team2 = self.__find_team("Clemson")
        g.team1_score = 17
        g.team2_score = 31
        g.favored = "team1"
        g.spread = 3.5
        g.state = "in_progress"
        game_key = self.__edit_existing_game(g)
        self.assertEqual(self.calc.get_team_name_winning_game(game_key),"Clemson")
        self.__restore_game(game_key)

    def __t13_game_none(self):
        valid_player_key = self.week1.get_player_key("Brent H.")
        with self.assertRaises(Exception):
            self.calc.player_did_not_pick(valid_player_key,None)

    def __t13_game_invalid(self):
        valid_player_key = self.week1.get_player_key("Brent H.")
        with self.assertRaises(Exception):
            self.calc.player_did_not_pick(valid_player_key,"bad key")

    def __t13_invalid_player(self):
        game_key = self.__get_a_valid_game_key()
        with self.assertRaises(Exception):
            self.calc.player_did_not_pick("bad key",game_key)

    def __t13_player_missing_all_week_picks(self):
        player_key = self.__get_a_valid_player_key()
        game_key = self.__get_a_valid_game_key()
        self.__make_all_picks_missing(player_key)
        self.assertTrue(self.calc.player_did_not_pick(player_key,game_key))
        self.__restore_picks(player_key)

    def __t13_player_missing_pick_for_game(self):
        player_key = self.week1.get_player_key("Brent H.")
        game_key = self.__get_a_valid_game_key()

        self.__remove_game_from_picks(player_key,game_key)
        self.assertTrue(self.calc.player_did_not_pick(player_key,game_key))
        self.__restore_picks(player_key)


    def __t13_player_missing_pick_winner(self):
        player_key = self.week1.get_player_key("Brent H.")
        game_key = self.__get_a_valid_game_key()

        self.__make_winner_missing(player_key,game_key)
        self.assertTrue(self.calc.player_did_not_pick(player_key,game_key))
        self.__restore_picks(player_key)

    def __t13_player_made_pick(self):
        player_key = self.week1.get_player_key("Brent H.")
        game_key = self.__get_a_valid_game_key()
        self.assertFalse(self.calc.player_did_not_pick(player_key,game_key))

    def __t14_game_none(self):
        player_key = self.__get_a_valid_player_key()
        with self.assertRaises(Exception):
            self.calc.did_player_win_game(player_key,None)

    def __t14_invalid_player(self):
        game_key = self.__get_a_valid_game_key()
        with self.assertRaises(Exception):
            self.calc.did_player_win_game("bad key",game_key)

    def __t14_player_missing_pick(self):
        player_key = self.week1.get_player_key("Brent H.")
        game_key = self.__get_a_valid_game_key()

        self.__remove_game_from_picks(player_key,game_key)
        self.assertFalse(self.calc.did_player_win_game(player_key,game_key))
        self.__restore_picks(player_key)

    def __t14_game_in_progress(self):
        player_key = self.week1.get_player_key("Brent H.")
        g = Game()
        g.state = "in_progress"
        game_key = self.__edit_existing_game(g)
        self.assertFalse(self.calc.did_player_win_game(player_key,game_key))
        self.__restore_game(game_key)

    def __t14_game_not_started(self):
        player_key = self.week1.get_player_key("Brent H.")
        g = Game()
        g.state = "not_started"
        game_key = self.__edit_existing_game(g)
        self.assertFalse(self.calc.did_player_win_game(player_key,game_key))
        self.__restore_game(game_key)

    def __t14_player_won_game(self):
        player_key = self.week1.get_player_key("Brent H.")
        game_key = self.__find_game_key("North Carolina","South Carolina")
        self.assertTrue(self.calc.did_player_win_game(player_key,game_key))

    def __t14_player_lost_game(self):
        player_key = self.week1.get_player_key("Brent H.")
        game_key = self.__find_game_key("Penn State","Syracuse")
        self.assertFalse(self.calc.did_player_win_game(player_key,game_key))

    def __t15_game_none(self):
        player_key = self.__get_a_valid_player_key()
        with self.assertRaises(Exception):
            self.calc.did_player_lose_game(player_key,None)

    def __t15_invalid_player(self):
        game_key = self.__get_a_valid_game_key()
        with self.assertRaises(Exception):
            self.calc.did_player_lose_game("bad key",game_key)

    def __t15_player_missing_pick(self):
        player_key = self.week1.get_player_key("Brent H.")
        game_key = self.__get_a_valid_game_key()

        self.__remove_game_from_picks(player_key,game_key)
        self.assertTrue(self.calc.did_player_lose_game(player_key,game_key))
        self.__restore_picks(player_key)

    def __t15_game_in_progress(self):
        player_key = self.week1.get_player_key("Brent H.")
        g = Game()
        g.state = "in_progress"
        game_key = self.__edit_existing_game(g)
        self.assertFalse(self.calc.did_player_lose_game(player_key,game_key))
        self.__restore_game(game_key)

    def __t15_game_not_started(self):
        player_key = self.week1.get_player_key("Brent H.")
        g = Game()
        g.state = "not_started"
        game_key = self.__edit_existing_game(g)
        self.assertFalse(self.calc.did_player_lose_game(player_key,game_key))
        self.__restore_game(game_key)

    def __t15_player_won_game(self):
        player_key = self.week1.get_player_key("Brent H.")
        game_key = self.__find_game_key("North Carolina","South Carolina")
        self.assertFalse(self.calc.did_player_lose_game(player_key,game_key))

    def __t15_player_lost_game(self):
        player_key = self.week1.get_player_key("Brent H.")
        game_key = self.__find_game_key("Penn State","Syracuse")
        self.assertTrue(self.calc.did_player_lose_game(player_key,game_key))

    def __t16_invalid_player(self):
        with self.assertRaises(Exception):
            self.calc.get_number_of_wins("bad key")

    def __t16_no_games_started(self):
        player_key = self.week1.get_player_key("Brent H.")
        self.__modify_game_states(['not_started']*10)
        self.assertEqual(self.calc.get_number_of_wins(player_key),0)
        self.__restore_games()

    def __t16_some_games_in_progress(self):
        player_key = self.week1.get_player_key("Brent H.")
        states = ['not_started']*3 + ['in_progress']*7
        self.__modify_game_states(states)
        self.assertEqual(self.calc.get_number_of_wins(player_key),0)
        self.__restore_games()

    def __t16_mixed_game_states(self):
        player_key = self.week1.get_player_key("Brent H.")
        num_wins_in_first_3_games_2013_week_1 = 2

        states = ['final']*3 + ['not_started']*3 + ['in_progress']*4
        self.__modify_game_states(states)
        self.assertEqual(self.calc.get_number_of_wins(player_key),num_wins_in_first_3_games_2013_week_1)
        self.__restore_games()

    def __t16_all_games_final(self):
        player_key = self.week1.get_player_key("Brent H.")
        num_wins_2013_week_1 = 5
        self.assertEqual(self.calc.get_number_of_wins(player_key),num_wins_2013_week_1)

    def __t16_player_with_no_picks(self):
        player_key = self.week1.get_player_key("Brent H.")
        self.__make_all_player_picks_not_entered(player_key)
        self.assertEqual(self.calc.get_number_of_wins(player_key),0)
        self.__restore_picks(player_key)

    def __t16_player_0_wins(self):
        player_key = self.week1.get_player_key("Dale R.")
        self.__make_dale_0_wins()
        self.assertEqual(self.calc.get_number_of_wins(player_key),0)
        self.__restore_picks(player_key)

    def __t16_player_10_wins(self):
        player_key = self.week1.get_player_key("William M.")
        self.__make_william_10_wins()
        self.assertEqual(self.calc.get_number_of_wins(player_key),10)
        self.__restore_picks(player_key)

    def __t17_invalid_player(self):
        with self.assertRaises(Exception):
            self.calc.get_number_of_losses("bad key")

    def __t17_no_games_started(self):
        player_key = self.week1.get_player_key("Brent H.")
        self.__modify_game_states(['not_started']*10)
        self.assertEqual(self.calc.get_number_of_losses(player_key),0)
        self.__restore_games()

    def __t17_some_games_in_progress(self):
        player_key = self.week1.get_player_key("Brent H.")
        states = ['not_started']*3 + ['in_progress']*7
        self.__modify_game_states(states)
        self.assertEqual(self.calc.get_number_of_losses(player_key),0)
        self.__restore_games()

    def __t17_mixed_game_states(self):
        player_key = self.week1.get_player_key("Brent H.")
        num_losses_in_first_3_games_2013_week_1 = 1

        states = ['final']*3 + ['not_started']*3 + ['in_progress']*4
        self.__modify_game_states(states)
        self.assertEqual(self.calc.get_number_of_losses(player_key),num_losses_in_first_3_games_2013_week_1)
        self.__restore_games()

    def __t17_all_games_final(self):
        player_key = self.week1.get_player_key("Byron R.")
        num_losses_2013_week_1 = 4
        self.assertEqual(self.calc.get_number_of_losses(player_key),num_losses_2013_week_1)

    def __t17_player_with_no_picks(self):
        player_key = self.week1.get_player_key("Brent H.")
        self.__make_all_player_picks_not_entered(player_key)
        self.assertEqual(self.calc.get_number_of_losses(player_key),10)
        self.__restore_picks(player_key)

    def __t17_player_0_losses(self):
        player_key = self.week1.get_player_key("William M.")
        self.__make_william_10_wins()
        self.assertEqual(self.calc.get_number_of_losses(player_key),0)
        self.__restore_picks(player_key)

    def __t17_player_10_losses(self):
        player_key = self.week1.get_player_key("Dale R.")
        self.__make_dale_0_wins()
        self.assertEqual(self.calc.get_number_of_losses(player_key),10)
        self.__restore_picks(player_key)

    def __t18_game_none(self):
        player_key = self.__get_a_valid_player_key()
        with self.assertRaises(Exception):
            self.calc.is_player_winning_game(player_key,None)

    def __t18_invalid_player(self):
        game_key = self.__get_a_valid_game_key()
        with self.assertRaises(Exception):
            self.calc.is_player_winning_game("bad key",game_key)

    def __t18_player_pick_missing_game_not_started(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 25
        game.team2_score = 10
        game.state = "not_started"

        game_key = self.__edit_existing_game(game)
        self.__make_winner_missing(player_key,game_key)

        self.assertFalse(self.calc.is_player_winning_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)

    def __t18_player_pick_missing_game_in_progress(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 25
        game.team2_score = 10
        game.state = "in_progress"

        game_key = self.__edit_existing_game(game)
        self.__make_winner_missing(player_key,game_key)

        self.assertFalse(self.calc.is_player_winning_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)

    def __t18_player_pick_missing_game_final(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 25
        game.team2_score = 10
        game.state = "final"

        game_key = self.__edit_existing_game(game)
        self.__make_winner_missing(player_key,game_key)

        self.assertFalse(self.calc.is_player_winning_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)

    def __t18_player_ahead_in_game_and_pool(self):
        player_key = self.week1.get_player_key("Brent H.")
        self.__save_picks(self.week1.player_picks[player_key])

        game = Game()
        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 25
        game.team2_score = 10
        game.state = "in_progress"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team1")

        self.assertTrue(self.calc.is_player_winning_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)

    def __t18_player_behind_in_game_and_pool(self):
        player_key = self.week1.get_player_key("Brent H.")
        self.__save_picks(self.week1.player_picks[player_key])

        game = Game()
        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 10
        game.team2_score = 30
        game.state = "in_progress"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team1")

        self.assertFalse(self.calc.is_player_winning_game(player_key,game_key))

    def __t18_player_ahead_in_game_and_behind_in_pool(self):
        player_key = self.week1.get_player_key("Brent H.")
        self.__save_picks(self.week1.player_picks[player_key])

        game = Game()
        game.favored = "team2"
        game.spread = 5.5
        game.team1_score = 20 
        game.team2_score = 25
        game.state = "in_progress"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team2")

        self.assertFalse(self.calc.is_player_winning_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)

    def __t18_player_behind_in_game_and_ahead_in_pool(self):
        player_key = self.week1.get_player_key("Brent H.")
        self.__save_picks(self.week1.player_picks[player_key])

        game = Game()
        game.favored = "team2"
        game.spread = 1.5
        game.team1_score = 20 
        game.team2_score = 21
        game.state = "in_progress"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team1")

        self.assertTrue(self.calc.is_player_winning_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)

    def __t18_game_not_started(self):
        player_key = self.week1.get_player_key("Brent H.")
        self.__save_picks(self.week1.player_picks[player_key])

        game = Game()
        game.favored = "team2"
        game.spread = 1.5
        game.team1_score = 20 
        game.team2_score = 21
        game.state = "not_started"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team1")

        self.assertFalse(self.calc.is_player_winning_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)

    def __t18_game_final(self):
        player_key = self.week1.get_player_key("Brent H.")
        self.__save_picks(self.week1.player_picks[player_key])

        game = Game()
        game.favored = "team2"
        game.spread = 1.5
        game.team1_score = 20 
        game.team2_score = 21
        game.state = "final"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team1")

        self.assertFalse(self.calc.is_player_winning_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)

    def __t19_game_none(self):
        player_key = self.__get_a_valid_player_key()
        with self.assertRaises(Exception):
            self.calc.is_player_losing_game(player_key,None)

    def __t19_invalid_player(self):
        game_key = self.__get_a_valid_game_key()
        with self.assertRaises(Exception):
            self.calc.is_player_losing_game("bad key",game_key)

    def __t19_game_not_started(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team2"
        game.spread = 1.5
        game.team1_score = 20 
        game.team2_score = 21
        game.state = "not_started"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team1")

        self.assertFalse(self.calc.is_player_losing_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)

    def __t19_game_final(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team2"
        game.spread = 1.5
        game.team1_score = 20 
        game.team2_score = 21
        game.state = "final"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team1")

        self.assertFalse(self.calc.is_player_losing_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)

    def __t19_player_pick_missing_game_not_started(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 25
        game.team2_score = 10
        game.state = "not_started"

        game_key = self.__edit_existing_game(game)
        self.__make_winner_missing(player_key,game_key)

        self.assertTrue(self.calc.is_player_losing_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)

    def __t19_player_pick_missing_game_in_progress(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 25
        game.team2_score = 10
        game.state = "in_progress"

        game_key = self.__edit_existing_game(game)
        self.__make_winner_missing(player_key,game_key)

        self.assertTrue(self.calc.is_player_losing_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)

    def __t19_player_pick_missing_game_final(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 10
        game.team2_score = 25
        game.state = "final"

        game_key = self.__edit_existing_game(game)
        self.__make_winner_missing(player_key,game_key)

        self.assertFalse(self.calc.is_player_losing_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)

    def __t19_player_ahead_in_game_and_pool(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 25
        game.team2_score = 10
        game.state = "in_progress"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team1")

        self.assertFalse(self.calc.is_player_losing_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)

    def __t19_player_behind_in_game_and_pool(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 10
        game.team2_score = 30
        game.state = "in_progress"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team1")

        self.assertTrue(self.calc.is_player_losing_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)

    def __t19_player_ahead_in_game_and_behind_in_pool(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team2"
        game.spread = 5.5
        game.team1_score = 20 
        game.team2_score = 25
        game.state = "in_progress"
        
        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team2")

        self.assertTrue(self.calc.is_player_losing_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)

    def __t19_player_behind_in_game_and_ahead_in_pool(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team2"
        game.spread = 1.5
        game.team1_score = 20 
        game.team2_score = 21
        game.state = "in_progress"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team1")

        self.assertFalse(self.calc.is_player_losing_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)

    def __t20_game_none(self):
        player_key = self.__get_a_valid_player_key()
        with self.assertRaises(Exception):
            self.calc.is_player_projected_to_win_game(player_key,None)

    def __t20_invalid_player(self):
        game_key = self.__get_a_valid_game_key()
        with self.assertRaises(Exception):
            self.calc.is_player_projected_to_win_game("bad key",game_key)

    def __t20_player_pick_missing(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 10
        game.team2_score = 25
        game.state = "in_progress"

        game_key = self.__edit_existing_game(game)
        self.__make_winner_missing(player_key,game_key)

        self.assertFalse(self.calc.is_player_projected_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)


    def __t20_game_final_player_ahead_in_game_and_pool(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 25
        game.team2_score = 10
        game.state = "final"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team1")

        self.assertTrue(self.calc.is_player_projected_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)


    def __t20_game_final_player_behind_in_game_and_pool(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 10
        game.team2_score = 30
        game.state = "final"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team1")

        self.assertFalse(self.calc.is_player_projected_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)


    def __t20_game_final_player_ahead_in_game_and_behind_in_pool(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team2"
        game.spread = 5.5
        game.team1_score = 20 
        game.team2_score = 25
        game.state = "final"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team2")

        self.assertFalse(self.calc.is_player_projected_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)



    def __t20_game_final_player_behind_in_game_and_ahead_in_pool(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team2"
        game.spread = 1.5
        game.team1_score = 20 
        game.team2_score = 21
        game.state = "final"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team1")

        self.assertTrue(self.calc.is_player_projected_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)

    def __t20_game_in_progress_player_ahead_in_game_and_pool(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 25
        game.team2_score = 10
        game.state = "in_progress"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team1")

        self.assertTrue(self.calc.is_player_projected_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)



    def __t20_game_in_progress_player_behind_in_game_and_pool(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 10
        game.team2_score = 30
        game.state = "in_progress"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team1")

        self.assertFalse(self.calc.is_player_projected_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)

    def __t20_game_in_progress_player_ahead_in_game_and_behind_in_pool(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team2"
        game.spread = 5.5
        game.team1_score = 20 
        game.team2_score = 25
        game.state = "in_progress"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team2")

        self.assertFalse(self.calc.is_player_projected_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)


    def __t20_game_in_progress_player_behind_in_game_and_ahead_in_pool(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team2"
        game.spread = 1.5
        game.team1_score = 20 
        game.team2_score = 21
        game.state = "in_progress"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team1")

        self.assertTrue(self.calc.is_player_projected_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)


    def __t20_game_not_started_player_ahead_in_game_and_pool(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 25
        game.team2_score = 10
        game.state = "not_started"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team1")

        self.assertTrue(self.calc.is_player_projected_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)

    def __t20_game_not_started_player_behind_in_game_and_pool(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 10
        game.team2_score = 30
        game.state = "not_started"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team1")

        self.assertTrue(self.calc.is_player_projected_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)


    def __t20_game_not_started_player_ahead_in_game_and_behind_in_pool(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team2"
        game.spread = 5.5
        game.team1_score = 20 
        game.team2_score = 25
        game.state = "not_started"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team2")

        self.assertTrue(self.calc.is_player_projected_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)


    def __t20_game_not_started_player_behind_in_game_and_ahead_in_pool(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team2"
        game.spread = 1.5
        game.team1_score = 20 
        game.team2_score = 21
        game.state = "not_started"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team1")

        self.assertTrue(self.calc.is_player_projected_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)

    def __t21_game_none(self):
        player_key = self.__get_a_valid_player_key()
        with self.assertRaises(Exception):
            self.calc.is_player_possible_to_win_game(player_key,None)

    def __t21_invalid_player(self):
        game_key = self.__get_a_valid_game_key()
        with self.assertRaises(Exception):
            self.calc.is_player_possible_to_win_game("bad key",game_key)

    def __t21_player_pick_missing(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 10
        game.team2_score = 25
        game.state = "in_progress"

        game_key = self.__edit_existing_game(game)
        self.__make_winner_missing(player_key,game_key)

        self.assertFalse(self.calc.is_player_possible_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)


    def __t21_game_final_player_ahead_in_game_and_pool(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 25
        game.team2_score = 10
        game.state = "final"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team1")

        self.assertTrue(self.calc.is_player_possible_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)


    def __t21_game_final_player_behind_in_game_and_pool(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 10
        game.team2_score = 30
        game.state = "final"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team1")

        self.assertFalse(self.calc.is_player_possible_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)


    def __t21_game_final_player_ahead_in_game_and_behind_in_pool(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team2"
        game.spread = 5.5
        game.team1_score = 20 
        game.team2_score = 25
        game.state = "final"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team2")


        self.assertFalse(self.calc.is_player_possible_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)


    def __t21_game_final_player_behind_in_game_and_ahead_in_pool(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team2"
        game.spread = 1.5
        game.team1_score = 20 
        game.team2_score = 21
        game.state = "final"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team1")

        self.assertTrue(self.calc.is_player_possible_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)


    def __t21_game_in_progress_player_ahead_in_game_and_pool(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 25
        game.team2_score = 10
        game.state = "in_progress"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team1")

        self.assertTrue(self.calc.is_player_possible_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)


    def __t21_game_in_progress_player_behind_in_game_and_pool(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 10
        game.team2_score = 30
        game.state = "in_progress"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team1")

        self.assertTrue(self.calc.is_player_possible_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)


    def __t21_game_in_progress_player_ahead_in_game_and_behind_in_pool(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team2"
        game.spread = 5.5
        game.team1_score = 20 
        game.team2_score = 25
        game.state = "in_progress"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team2")

        self.assertTrue(self.calc.is_player_possible_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)


    def __t21_game_in_progress_player_behind_in_game_and_ahead_in_pool(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team2"
        game.spread = 1.5
        game.team1_score = 20 
        game.team2_score = 21
        game.state = "in_progress"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team1")

        self.assertTrue(self.calc.is_player_possible_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)


    def __t21_game_not_started_player_ahead_in_game_and_pool(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 25
        game.team2_score = 10
        game.state = "not_started"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team1")

        self.assertTrue(self.calc.is_player_possible_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)


    def __t21_game_not_started_player_behind_in_game_and_pool(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 10
        game.team2_score = 30
        game.state = "not_started"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team1")

        self.assertTrue(self.calc.is_player_possible_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)



    def __t21_game_not_started_player_ahead_in_game_and_behind_in_pool(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team2"
        game.spread = 5.5
        game.team1_score = 20 
        game.team2_score = 25
        game.state = "not_started"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team2")

        self.assertTrue(self.calc.is_player_possible_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)


    def __t21_game_not_started_player_behind_in_game_and_ahead_in_pool(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team2"
        game.spread = 1.5
        game.team1_score = 20 
        game.team2_score = 21
        game.state = "not_started"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team1")

        self.assertTrue(self.calc.is_player_possible_to_win_game(player_key,game_key))

        self.__restore_picks(player_key)
        self.__restore_game(game_key)


    def __t22_invalid_player_name(self):
        with self.assertRaises(Exception):
            self.calc.get_number_of_projected_wins("bad key")

    def __t22_no_games_started(self):
        player_key = self.week1.get_player_key("Brent H.")
        self.__modify_game_states(['not_started']*10)
        self.assertEqual(self.calc.get_number_of_projected_wins(player_key),10)
        self.__restore_games()

    def __t22_some_games_in_progress(self):
        player_key = self.week1.get_player_key("Brent H.")
        num_projected_wins_last_7_games_2013_week_1 = 6

        states = ['not_started']*3 + ['in_progress']*7
        self.__modify_game_states(states)
        self.assertEqual(self.calc.get_number_of_projected_wins(player_key),num_projected_wins_last_7_games_2013_week_1)
        self.__restore_games()

    def __t22_mixed_game_states(self):
        num_projected_wins_first_3_games = 2
        num_projected_wins_next_3_games = 3
        num_projected_wins_last_4_games = 2
        num_projected_wins_2013_week_1 = num_projected_wins_first_3_games + num_projected_wins_next_3_games + num_projected_wins_last_4_games

        player_key = self.week1.get_player_key("Brent H.")

        states = ['final']*3 + ['not_started']*3 + ['in_progress']*4
        self.__modify_game_states(states)
        self.assertEqual(self.calc.get_number_of_projected_wins(player_key),num_projected_wins_2013_week_1)
        self.__restore_games()

    def __t22_all_games_final(self):
        player_key = self.week1.get_player_key("Byron R.")
        num_projected_wins_2013_week_1 = 6
        self.assertEqual(self.calc.get_number_of_projected_wins(player_key),num_projected_wins_2013_week_1)

    def __t22_player_with_no_picks(self):
        player_key = self.week1.get_player_key("Brent H.")
        self.__make_all_player_picks_not_entered(player_key)
        self.assertEqual(self.calc.get_number_of_projected_wins(player_key),0)
        self.__restore_picks(player_key)

    def __t22_game_final_player_0_wins(self):
        player_key = self.week1.get_player_key("Dale R.")
        self.__make_dale_0_wins()
        self.__modify_game_states(['final']*10)
        self.assertEqual(self.calc.get_number_of_projected_wins(player_key),0)
        self.__restore_picks(player_key)
        self.__restore_games()

    def __t22_game_final_player_10_wins(self):
        player_key = self.week1.get_player_key("William M.")
        self.__make_william_10_wins()
        self.__modify_game_states(['final']*10)
        self.assertEqual(self.calc.get_number_of_projected_wins(player_key),10)
        self.__restore_picks(player_key)
        self.__restore_games()

    def __t22_game_in_progress_player_0_wins(self):
        player_key = self.week1.get_player_key("Dale R.")
        self.__make_dale_0_wins()
        self.__modify_game_states(['in_progress']*10)
        self.assertEqual(self.calc.get_number_of_projected_wins(player_key),0)
        self.__restore_picks(player_key)
        self.__restore_games()

    def __t22_game_in_progress_player_10_wins(self):
        player_key = self.week1.get_player_key("William M.")
        self.__make_william_10_wins()
        self.__modify_game_states(['in_progress']*10)
        self.assertEqual(self.calc.get_number_of_projected_wins(player_key),10)
        self.__restore_picks(player_key)
        self.__restore_games()

    def __t22_game_not_started_player_0_wins(self):
        player_key = self.week1.get_player_key("Dale R.")
        self.__make_dale_0_wins()
        self.__modify_game_states(['not_started']*10)
        self.assertEqual(self.calc.get_number_of_projected_wins(player_key),10)
        self.__restore_picks(player_key)
        self.__restore_games()

    def __t22_game_not_started_player_10_wins(self):
        player_key = self.week1.get_player_key("William M.")
        self.__make_william_10_wins()
        self.__modify_game_states(['not_started']*10)
        self.assertEqual(self.calc.get_number_of_projected_wins(player_key),10)
        self.__restore_picks(player_key)
        self.__restore_games()

    def __t23_invalid_player(self):
        with self.assertRaises(Exception):
            self.calc.get_number_of_possible_wins("bad key")

    def __t23_no_games_started(self):
        player_key = self.week1.get_player_key("Brent H.")
        self.__modify_game_states(['not_started']*10)
        self.assertEqual(self.calc.get_number_of_possible_wins(player_key),10)
        self.__restore_games()

    def __t23_some_games_in_progress(self):
        player_key = self.week1.get_player_key("Brent H.")
        states = ['not_started']*3 + ['in_progress']*7
        self.__modify_game_states(states)
        self.assertEqual(self.calc.get_number_of_possible_wins(player_key),10)
        self.__restore_games()

    def __t23_mixed_game_states(self):
        num_possible_wins_first_3_games = 2
        num_possible_wins_next_3_games = 3
        num_possible_wins_last_4_games = 4
        num_possible_wins_2013_week_1 = num_possible_wins_first_3_games + num_possible_wins_next_3_games + num_possible_wins_last_4_games

        player_key = self.week1.get_player_key("Brent H.")

        states = ['final']*3 + ['not_started']*3 + ['in_progress']*4
        self.__modify_game_states(states)
        self.assertEqual(self.calc.get_number_of_possible_wins(player_key),num_possible_wins_2013_week_1)
        self.__restore_games()

    def __t23_all_games_final(self):
        num_possible_wins_2013_week_1 = 6
        player_key = self.week1.get_player_key("Byron R.")
        self.assertEqual(self.calc.get_number_of_possible_wins(player_key),num_possible_wins_2013_week_1)

    def __t23_player_with_no_picks(self):
        player_key = self.week1.get_player_key("Brent H.")
        self.__make_all_player_picks_not_entered(player_key)
        self.assertEqual(self.calc.get_number_of_possible_wins(player_key),0)
        self.__restore_picks(player_key)

    def __t23_game_final_player_0_wins(self):
        player_key = self.week1.get_player_key("Dale R.")
        self.__make_dale_0_wins()
        self.__modify_game_states(['final']*10)
        self.assertEqual(self.calc.get_number_of_possible_wins(player_key),0)
        self.__restore_picks(player_key)
        self.__restore_games()

    def __t23_game_final_player_10_wins(self):
        player_key = self.week1.get_player_key("William M.")
        self.__make_william_10_wins()
        self.__modify_game_states(['final']*10)
        self.assertEqual(self.calc.get_number_of_possible_wins(player_key),10)
        self.__restore_picks(player_key)
        self.__restore_games()

    def __t23_game_in_progress_player_0_wins(self):
        player_key = self.week1.get_player_key("Dale R.")
        self.__make_dale_0_wins()
        self.__modify_game_states(['in_progress']*10)
        self.assertEqual(self.calc.get_number_of_possible_wins(player_key),10)
        self.__restore_picks(player_key)
        self.__restore_games()

    def __t23_game_in_progress_player_10_wins(self):
        player_key = self.week1.get_player_key("William M.")
        self.__make_william_10_wins()
        self.__modify_game_states(['in_progress']*10)
        self.assertEqual(self.calc.get_number_of_possible_wins(player_key),10)
        self.__restore_picks(player_key)
        self.__restore_games()

    def __t23_game_not_started_player_0_wins(self):
        player_key = self.week1.get_player_key("Dale R.")
        self.__make_dale_0_wins()
        self.__modify_game_states(['not_started']*10)
        self.assertEqual(self.calc.get_number_of_possible_wins(player_key),10)
        self.__restore_picks(player_key)
        self.__restore_games()

    def __t23_game_not_started_player_10_wins(self):
        player_key = self.week1.get_player_key("William M.")
        self.__make_william_10_wins()
        self.__modify_game_states(['not_started']*10)
        self.assertEqual(self.calc.get_number_of_possible_wins(player_key),10)
        self.__restore_picks(player_key)
        self.__restore_games()

    def __t24_no_games_started(self):
        self.__modify_game_states(['not_started']*10)
        self.assertFalse(self.calc.all_games_final())
        self.__restore_games()

    def __t24_some_games_in_progress(self):
        states = ['not_started']*3 + ['in_progress']*7
        self.__modify_game_states(states)
        self.assertFalse(self.calc.all_games_final())
        self.__restore_games()

    def __t24_mixed_game_states(self):
        states = ['final']*3 + ['not_started']*3 + ['in_progress']*4
        self.__modify_game_states(states)
        self.assertFalse(self.calc.all_games_final())
        self.__restore_games()

    def __t24_all_games_final(self):
        self.assertTrue(self.calc.all_games_final())

    def __t25_no_games_started(self):
        self.__modify_game_states(['not_started']*10)
        self.assertTrue(self.calc.no_games_started())
        self.__restore_games()

    def __t25_some_games_in_progress(self):
        states = ['not_started']*3 + ['in_progress']*7
        self.__modify_game_states(states)
        self.assertFalse(self.calc.no_games_started())
        self.__restore_games()

    def __t25_mixed_game_states(self):
        states = ['final']*3 + ['not_started']*3 + ['in_progress']*4
        self.__modify_game_states(states)
        self.assertFalse(self.calc.no_games_started())
        self.__restore_games()

    def __t25_all_games_final(self):
        self.assertFalse(self.calc.no_games_started())

    def __t26_no_games_started(self):
        self.__modify_game_states(['not_started']*10)
        self.assertFalse(self.calc.at_least_one_game_in_progress())
        self.__restore_games()

    def __t26_one_game_in_progress(self):
        states = ['not_started']*1 + ['in_progress']*9
        self.__modify_game_states(states)
        self.assertTrue(self.calc.at_least_one_game_in_progress())
        self.__restore_games()

    def __t26_some_games_in_progress(self):
        states = ['not_started']*3 + ['in_progress']*7
        self.__modify_game_states(states)
        self.assertTrue(self.calc.at_least_one_game_in_progress())
        self.__restore_games()

    def __t26_mixed_game_states(self):
        states = ['final']*3 + ['not_started']*3 + ['in_progress']*4
        self.__modify_game_states(states)
        self.assertTrue(self.calc.at_least_one_game_in_progress())
        self.__restore_games()

    def __t26_all_games_final(self):
        self.assertFalse(self.calc.at_least_one_game_in_progress())

    def __t27_no_games_started(self):
        self.__modify_game_states(['not_started']*10)
        self.assertEqual(self.calc.get_summary_state_of_all_games(),"not_started")
        self.__restore_games()

    def __t27_one_game_in_progress(self):
        states = ['not_started']*1 + ['in_progress']*9
        self.__modify_game_states(states)
        self.assertEqual(self.calc.get_summary_state_of_all_games(),"in_progress")
        self.__restore_games()

    def __t27_some_games_in_progress(self):
        states = ['not_started']*3 + ['in_progress']*7
        self.__modify_game_states(states)
        self.assertEqual(self.calc.get_summary_state_of_all_games(),"in_progress")
        self.__restore_games()

    def __t27_mixed_game_states(self):
        states = ['final']*3 + ['not_started']*3 + ['in_progress']*4
        self.__modify_game_states(states)
        self.assertEqual(self.calc.get_summary_state_of_all_games(),"in_progress")
        self.__restore_games()

    def __t27_all_games_final(self):
        self.assertEqual(self.calc.get_summary_state_of_all_games(),"final")

    def __t28_game_none(self):
        player_key = self.__get_a_valid_player_key()
        with self.assertRaises(Exception):
            self.calc.get_game_result_string(player_key,None)

    def __t28_invalid_player(self):
        game_key = self.__get_a_valid_game_key()
        with self.assertRaises(Exception):
            self.calc.get_game_result_string("bad key",game_key)

    def __t28_player_pick_missing(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 10
        game.team2_score = 25
        game.state = "in_progress"

        game_key = self.__edit_existing_game(game)
        self.__make_winner_missing(player_key,game_key)

        self.assertEqual(self.calc.get_game_result_string(player_key,game_key),"loss")

        self.__restore_picks(player_key)
        self.__restore_game(game_key)


    def __t28_game_win(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 10
        game.team2_score = 25
        game.state = "final"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team2")

        self.assertEqual(self.calc.get_game_result_string(player_key,game_key),"win")

        self.__restore_picks(player_key)
        self.__restore_game(game_key)


    def __t28_game_loss(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 10
        game.team2_score = 25
        game.state = "final"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team1")

        self.assertEqual(self.calc.get_game_result_string(player_key,game_key),"loss")

        self.__restore_picks(player_key)
        self.__restore_game(game_key)


    def __t28_game_ahead(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 10
        game.team2_score = 25
        game.state = "in_progress"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team2")

        self.assertEqual(self.calc.get_game_result_string(player_key,game_key),"ahead")

        self.__restore_picks(player_key)
        self.__restore_game(game_key)


    def __t28_game_behind(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 10
        game.team2_score = 25
        game.state = "in_progress"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team1")

        self.assertEqual(self.calc.get_game_result_string(player_key,game_key),"behind")

        self.__restore_picks(player_key)
        self.__restore_game(game_key)


    def __t28_game_not_started(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 10
        game.team2_score = 25
        game.state = "not_started"

        game_key = self.__edit_existing_game(game)
        self.__change_player_pick(player_key,game_key,"team1")

        self.assertEqual(self.calc.get_game_result_string(player_key,game_key),"")

        self.__restore_picks(player_key)
        self.__restore_game(game_key)


    def __t29_game_none(self):
        with self.assertRaises(Exception):
            self.calc.get_favored_team_name(None)

    def __t29_invalid_favored(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "invalid"

        game_key = self.__edit_existing_game(game)

        with self.assertRaises(AssertionError):
            self.calc.get_favored_team_name(game_key)

        self.__restore_game(game_key)

    def __t29_team1_favored(self):
        game_key = self.__find_game_key("LSU","TCU")
        self.assertEqual(self.calc.get_favored_team_name(game_key),"LSU")

    def __t29_team2_favored(self):
        game_key = self.__find_game_key("North Carolina","South Carolina")
        self.assertEqual(self.calc.get_favored_team_name(game_key),"South Carolina")

    def __t30_game_none(self):
        with self.assertRaises(Exception):
            self.calc.get_game_score_spread(None)

    def __t30_game_not_started(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 10
        game.team2_score = 25
        game.state = "not_started"

        game_key = self.__edit_existing_game(game)

        with self.assertRaises(Exception):
            self.calc.get_game_score_spread(game_key)

        self.__restore_game(game_key)

    def __t30_game_in_progress(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 10
        game.team2_score = 25
        game.state = "in_progress"

        game_key = self.__edit_existing_game(game)
        self.assertEqual(self.calc.get_game_score_spread(game_key),15)
        self.__restore_game(game_key)


    def __t30_tied_score(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 13 
        game.team2_score = 13
        game.state = "final"

        game_key = self.__edit_existing_game(game)
        self.assertEqual(self.calc.get_game_score_spread(game_key),0)
        self.__restore_game(game_key)

    def __t30_team1_ahead(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()
        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 24
        game.team2_score = 11
        game.state = "final"

        game_key = self.__edit_existing_game(game)
        self.assertEqual(self.calc.get_game_score_spread(game_key),13)
        self.__restore_game(game_key)

    def __t30_team2_ahead(self):
        player_key = self.week1.get_player_key("Brent H.")

        game = Game()

        game.favored = "team1"
        game.spread = 5.5
        game.team1_score = 9
        game.team2_score = 31
        game.state = "final"

        game_key = self.__edit_existing_game(game)
        self.assertEqual(self.calc.get_game_score_spread(game_key),22)
        self.__restore_game(game_key)

    def __t31_pick_none(self):
        with self.assertRaises(Exception):
            self.calc.get_pick_score_spread(None)

    def __t31_pick_team1_score_none(self):
        pick = Pick()
        pick.team1_score = None
        pick.team2_score = 10
        with self.assertRaises(AssertionError):
            self.calc.get_pick_score_spread(pick)

    def __t31_pick_team2_score_none(self):
        pick = Pick()
        pick.team1_score = 10
        pick.team2_score = None
        with self.assertRaises(AssertionError):
            self.calc.get_pick_score_spread(pick)

    def __t31_tied_score(self):
        pick = Pick()
        pick.team1_score = 15 
        pick.team2_score = 15
        self.assertEqual(self.calc.get_pick_score_spread(pick),0)

    def __t31_team1_ahead(self):
        pick = Pick()
        pick.team1_score = 20 
        pick.team2_score = 11
        self.assertEqual(self.calc.get_pick_score_spread(pick),9)

    def __t31_team2_ahead(self):
        pick = Pick()
        pick.team1_score = 3
        pick.team2_score = 11
        self.assertEqual(self.calc.get_pick_score_spread(pick),8)

    def __t32_featured_game(self):
        game = self.calc.get_featured_game()
        self.assertEqual(game.number,10)

    def __t32_featured_game_missing(self):
        featured_game_key = self.__get_game10_key()
        self.week1.games[featured_game_key].number = 11

        with self.assertRaises(AssertionError):
            self.calc.get_featured_game()

        self.week1.games[featured_game_key].number = 10

    def __get_a_valid_game_key(self):
        game_keys = self.week1.games.keys()
        return game_keys[0]

    def __get_a_valid_game2_key(self):
        game_keys = self.week2.games.keys()
        return game_keys[0]

    def __get_a_valid_player_key(self):
        player_keys = self.week1.players.keys()
        return player_keys[0]

    def __make_all_picks_missing(self,player_key):
        self.__save_picks(self.week1.player_picks[player_key])
        self.week1.player_picks[player_key] = []

    def __remove_game_from_picks(self,player_key,game_key):
        self.__save_picks(self.week1.player_picks[player_key])
        new_picks = []
        for pick in self.week1.player_picks[player_key]:
            if pick.game != game_key:
                new_picks.append(pick)
        self.week1.player_picks[player_key] = new_picks

    def __make_winner_missing(self,player_key,game_key):
        self.__save_picks(self.week1.player_picks[player_key])
        for i,pick in enumerate(self.week1.player_picks[player_key]):
            if pick.game == game_key:
                self.week1.player_picks[player_key][i].winner = None
                return
        raise AssertionError,"could not find game in picks"

    def __save_picks(self,picks):
        self.__saved_picks = []
        for pick in picks:
            self.__saved_picks.append(copy.copy(pick))

    def __restore_picks(self,player_key):
        self.week1.player_picks[player_key] = self.__saved_picks

    def __restore_game(self,game_key):
        self.week1.games[game_key].number = self.__saved_game.number
        self.week1.games[game_key].team1_score = self.__saved_game.team1_score
        self.week1.games[game_key].team2_score = self.__saved_game.team2_score
        self.week1.games[game_key].favored = self.__saved_game.favored
        self.week1.games[game_key].spread = self.__saved_game.spread
        self.week1.games[game_key].state = self.__saved_game.state
        self.week1.games[game_key].quarter = self.__saved_game.quarter
        self.week1.games[game_key].time_left = self.__saved_game.time_left
        self.week1.games[game_key].date = self.__saved_game.date

    def __edit_existing_game(self,new_game):
        game_key = self.__get_a_game_to_edit()
        self.__edit_game(game_key,new_game)
        return game_key

    def __get_a_game_to_edit(self):
        return self.week1.games.keys()[0]

    def __edit_game(self,game_key,new_game):
        for key in self.week1.games:
            if key == game_key:
                self.__saved_game = copy.copy(self.week1.games[key])
                self.week1.games[key].number = new_game.number
                self.week1.games[key].team1_score = new_game.team1_score
                self.week1.games[key].team2_score = new_game.team2_score
                self.week1.games[key].favored = new_game.favored
                self.week1.games[key].spread = new_game.spread
                self.week1.games[key].state = new_game.state
                self.week1.games[key].quarter = new_game.quarter
                self.week1.games[key].time_left = new_game.time_left
                self.week1.games[key].date = new_game.date

                if new_game.team1:
                    self.week1.games[key].team1 = new_game.team1
                if new_game.team2:
                    self.week1.games[key].team2 = new_game.team2
                return
        raise AssertionError,"could not find game"

    def __get_game10_key(self):
        for key in self.week1.games:
            game = self.week1.games[key]
            if game.number == 10:
                return key
        raise AssertionError,"could not find game 10"

    def __find_game_key(self,team1,team2):
        for game_key in self.week1.games:
            game = self.week1.games.get(game_key)
            game_team1 = self.week1.teams.get(game.team1)
            game_team2 = self.week1.teams.get(game.team2)

            same_teams = team1 == game_team1.name and team2 == game_team2.name
            if same_teams:
                return game_key
        raise AssertionError, "Could not find game"

    def __find_team(self,name):
        for key in self.week1.teams:
            t = self.week1.get_team(key)
            if t.name == name:
                return key
        raise AssertionError,"Could not find team %s" % (name)

    def __make_william_10_wins(self):
        player_key = self.week1.get_player_key("William M.")
        self.__save_picks(self.week1.player_picks[player_key])
        game1 = self.__find_game_key("Colorado","Colorado State")
        self.__change_player_pick(player_key,game1)

    def __make_dale_0_wins(self):
        player_key = self.week1.get_player_key("Dale R.")
        self.__save_picks(self.week1.player_picks[player_key])
        game1 = self.__find_game_key("North Carolina","South Carolina")
        game2 = self.__find_game_key("Utah State","Utah")
        game3 = self.__find_game_key("Georgia","Clemson")
        self.__change_player_pick(player_key,game1)
        self.__change_player_pick(player_key,game2)
        self.__change_player_pick(player_key,game3)

    def __change_player_pick(self,player_key,game_key,new_value=None):
        player_picks = self.week1.player_picks[player_key]
        for i,pick in enumerate(player_picks):
            if pick.game == game_key:
                if new_value != None:
                    self.week1.player_picks[player_key][i].winner = new_value
                elif pick.winner == "team1":
                    self.week1.player_picks[player_key][i].winner = "team2"
                elif pick.winner == "team2":
                    self.week1.player_picks[player_key][i].winner = "team1"


    def __save_games(self):
        self.__saved_games = dict()
        for key in self.week1.games:
            self.__saved_games[key] = copy.copy(self.week1.games[key])

    def __restore_games(self):
        self.week1.games = self.__saved_games

    def __modify_game_states(self,states):
        assert len(states) == 10
        assert len(self.week1.games) == 10
        self.__save_games()

        for game_key in self.week1.games:
            game = self.week1.get_game(game_key)
            state_index = game.number - 1
            self.week1.games[game_key].state = states[state_index]

    def __make_all_player_picks_not_entered(self,player_key):
        self.__save_picks(self.week1.player_picks[player_key])
        for i in range(len(self.week1.player_picks[player_key])):
            self.week1.player_picks[player_key][i].winner = None

