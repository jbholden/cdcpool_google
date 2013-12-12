from code.update import *
from code.week_results import *
from code.database import *
import time
import logging
import unittest
import copy
import random
from test_data import *

class TestUpdate(unittest.TestCase):

    def test_get_week_results(self):
        self.__test_get_week_results(2013,1,TestData.week_results_2013_week1())
        self.__test_get_week_results(2013,2,TestData.week_results_2013_week2())
        self.__test_get_week_results(2013,3,TestData.week_results_2013_week3())
        self.__test_get_week_results(2013,4,TestData.week_results_2013_week4())
        self.__test_get_week_results(2013,5,TestData.week_results_2013_week5())
        self.__test_get_week_results(2013,6,TestData.week_results_2013_week6())
        self.__test_get_week_results(2013,7,TestData.week_results_2013_week7())
        self.__test_get_week_results(2013,8,TestData.week_results_2013_week8())
        self.__test_get_week_results(2013,9,TestData.week_results_2013_week9())
        self.__test_get_week_results(2013,10,TestData.week_results_2013_week10())
        self.__test_get_week_results(2013,11,TestData.week_results_2013_week11())
        self.__test_get_week_results(2013,12,TestData.week_results_2013_week12())
        self.__test_get_week_results(2013,13,TestData.week_results_2013_week13())

    def test_t2_assign_rank(self):
        self.__t2_win_loss_all_different()
        self.__t2_week_not_started()
        self.__t2_week_not_started_with_defaulters()
        self.__t2_week_not_started_with_some_missing_picks()
        self.__t2_win_loss_with_ties()
        self.__t2_win_loss_with_ties_less_than_10_games_complete()
        self.__t2_win_loss_with_first_place_ties()
        self.__t2_win_loss_with_first_place_ties_and_winner_specified()
        self.__t2_winner_missing()
        self.__t2_winner_insane()


    def test_t3_assign_projected_rank(self):
        self.__t3_wins_all_different()
        self.__t3_week_not_started()
        self.__t3_week_not_started_with_defaulters()
        self.__t3_week_not_started_with_some_missing_picks()
        self.__t3_wins_with_ties()
        self.__t3_less_than_10_wins()
        self.__t3_all_wins_0()
        self.__t3_first_place_ties()
        self.__t3_winner_specified()
        self.__t3_first_place_tie_with_winner_specified()
        self.__t3_winner_missing()
        self.__t3_winner_insane()

    def __t2_win_loss_all_different(self):
        self.__week_results = []
        self.__add_result(rank=None,expected_rank=11,wins=0,losses=10)
        self.__add_result(rank=None,expected_rank=10,wins=1,losses=9)
        self.__add_result(rank=None,expected_rank=9,wins=2,losses=8)
        self.__add_result(rank=None,expected_rank=8,wins=3,losses=7)
        self.__add_result(rank=None,expected_rank=7,wins=4,losses=6)
        self.__add_result(rank=None,expected_rank=6,wins=5,losses=5)
        self.__add_result(rank=None,expected_rank=5,wins=6,losses=4)
        self.__add_result(rank=None,expected_rank=4,wins=7,losses=3)
        self.__add_result(rank=None,expected_rank=3,wins=8,losses=2)
        self.__add_result(rank=None,expected_rank=2,wins=9,losses=1)
        self.__add_result(rank=None,expected_rank=1,wins=10,losses=0)

        self.__run_assign_rank_test()

    def __t2_week_not_started(self): 
        # in the week not started case, all records are 0-0
        # all should be tied for first place
        self.__week_results = []
        self.__add_result(rank=None,expected_rank=1,wins=0,losses=0)
        self.__add_result(rank=None,expected_rank=1,wins=0,losses=0)
        self.__add_result(rank=None,expected_rank=1,wins=0,losses=0)
        self.__add_result(rank=None,expected_rank=1,wins=0,losses=0)
        self.__add_result(rank=None,expected_rank=1,wins=0,losses=0)
        self.__add_result(rank=None,expected_rank=1,wins=0,losses=0)
        self.__add_result(rank=None,expected_rank=1,wins=0,losses=0)
        self.__add_result(rank=None,expected_rank=1,wins=0,losses=0)
        self.__add_result(rank=None,expected_rank=1,wins=0,losses=0)
        self.__add_result(rank=None,expected_rank=1,wins=0,losses=0)
        self.__add_result(rank=None,expected_rank=1,wins=0,losses=0)

        self.__run_assign_rank_test()

    def __t2_week_not_started_with_defaulters(self): 
        # in the week not started case, players with picks have record 0-0
        # defaulters have a record of 0-10
        # defaulters tied for last place, all others tied for first place
        self.__week_results = []
        self.__add_result(rank=None,expected_rank=1,wins=0,losses=0)
        self.__add_result(rank=None,expected_rank=1,wins=0,losses=0)
        self.__add_result(rank=None,expected_rank=1,wins=0,losses=0)
        self.__add_result(rank=None,expected_rank=1,wins=0,losses=0)
        self.__add_result(rank=None,expected_rank=1,wins=0,losses=0)
        self.__add_result(rank=None,expected_rank=9,wins=0,losses=10)
        self.__add_result(rank=None,expected_rank=9,wins=0,losses=10)
        self.__add_result(rank=None,expected_rank=9,wins=0,losses=10)
        self.__add_result(rank=None,expected_rank=1,wins=0,losses=0)
        self.__add_result(rank=None,expected_rank=1,wins=0,losses=0)
        self.__add_result(rank=None,expected_rank=1,wins=0,losses=0)

        self.__run_assign_rank_test()

    def __t2_week_not_started_with_some_missing_picks(self): 
        # not started player with picks have record 0-0
        # not started player with missing picks have losses 0-#losses
        self.__week_results = []
        self.__add_result(rank=None,expected_rank=1,wins=0,losses=0)
        self.__add_result(rank=None,expected_rank=1,wins=0,losses=0)
        self.__add_result(rank=None,expected_rank=1,wins=0,losses=0)
        self.__add_result(rank=None,expected_rank=1,wins=0,losses=0)
        self.__add_result(rank=None,expected_rank=1,wins=0,losses=0)
        self.__add_result(rank=None,expected_rank=1,wins=0,losses=0)
        self.__add_result(rank=None,expected_rank=7,wins=0,losses=1)
        self.__add_result(rank=None,expected_rank=7,wins=0,losses=1)
        self.__add_result(rank=None,expected_rank=9,wins=0,losses=2)
        self.__add_result(rank=None,expected_rank=10,wins=0,losses=10)
        self.__add_result(rank=None,expected_rank=10,wins=0,losses=10)

        self.__run_assign_rank_test()

    def __t2_win_loss_with_ties(self):
        self.__week_results = []
        self.__add_result(rank=None,expected_rank=1,wins=10,losses=0)
        self.__add_result(rank=None,expected_rank=2,wins=9,losses=1)
        self.__add_result(rank=None,expected_rank=2,wins=9,losses=1)
        self.__add_result(rank=None,expected_rank=4,wins=8,losses=2)
        self.__add_result(rank=None,expected_rank=4,wins=8,losses=2)
        self.__add_result(rank=None,expected_rank=6,wins=7,losses=3)
        self.__add_result(rank=None,expected_rank=6,wins=7,losses=3)
        self.__add_result(rank=None,expected_rank=8,wins=6,losses=4)
        self.__add_result(rank=None,expected_rank=8,wins=6,losses=4)
        self.__add_result(rank=None,expected_rank=10,wins=5,losses=5)
        self.__add_result(rank=None,expected_rank=10,wins=5,losses=5)
        self.__add_result(rank=None,expected_rank=12,wins=4,losses=6)
        self.__add_result(rank=None,expected_rank=12,wins=4,losses=6)
        self.__add_result(rank=None,expected_rank=14,wins=3,losses=7)
        self.__add_result(rank=None,expected_rank=14,wins=3,losses=7)
        self.__add_result(rank=None,expected_rank=16,wins=2,losses=8)
        self.__add_result(rank=None,expected_rank=16,wins=2,losses=8)
        self.__add_result(rank=None,expected_rank=18,wins=1,losses=9)
        self.__add_result(rank=None,expected_rank=18,wins=1,losses=9)
        self.__add_result(rank=None,expected_rank=20,wins=0,losses=10)
        self.__add_result(rank=None,expected_rank=20,wins=0,losses=10)

        self.__run_assign_rank_test()

    def __t2_win_loss_with_ties_less_than_10_games_complete(self):
        self.__week_results = []
        self.__add_result(rank=None,expected_rank=1,wins=5,losses=1)
        self.__add_result(rank=None,expected_rank=1,wins=5,losses=1)
        self.__add_result(rank=None,expected_rank=3,wins=4,losses=2)
        self.__add_result(rank=None,expected_rank=3,wins=4,losses=2)
        self.__add_result(rank=None,expected_rank=3,wins=4,losses=2)
        self.__add_result(rank=None,expected_rank=6,wins=3,losses=3)
        self.__add_result(rank=None,expected_rank=6,wins=3,losses=3)
        self.__add_result(rank=None,expected_rank=6,wins=3,losses=3)
        self.__add_result(rank=None,expected_rank=9,wins=2,losses=4)
        self.__add_result(rank=None,expected_rank=9,wins=2,losses=4)
        self.__add_result(rank=None,expected_rank=11,wins=1,losses=5)

        self.__run_assign_rank_test()

    def __t2_win_loss_with_first_place_ties(self):
        self.__week_results = []
        self.__add_result(rank=None,expected_rank=1,wins=8,losses=2)
        self.__add_result(rank=None,expected_rank=1,wins=8,losses=2)
        self.__add_result(rank=None,expected_rank=1,wins=8,losses=2)
        self.__add_result(rank=None,expected_rank=1,wins=8,losses=2)
        self.__add_result(rank=None,expected_rank=1,wins=8,losses=2)
        self.__add_result(rank=None,expected_rank=6,wins=7,losses=3)
        self.__add_result(rank=None,expected_rank=7,wins=6,losses=4)
        self.__add_result(rank=None,expected_rank=7,wins=6,losses=4)
        self.__add_result(rank=None,expected_rank=9,wins=5,losses=5)
        self.__add_result(rank=None,expected_rank=10,wins=4,losses=6)
        self.__add_result(rank=None,expected_rank=11,wins=3,losses=7)
        self.__add_result(rank=None,expected_rank=12,wins=2,losses=8)
        self.__add_result(rank=None,expected_rank=13,wins=1,losses=9)
        self.__add_result(rank=None,expected_rank=14,wins=0,losses=10)
        self.__add_result(rank=None,expected_rank=14,wins=0,losses=10)

        self.__run_assign_rank_test()

    def __t2_win_loss_with_first_place_ties_and_winner_specified(self): 
        self.__week_results = []
        self.__add_result(rank=None,expected_rank=1,wins=8,losses=2,player_key="player15")
        self.__add_result(rank=None,expected_rank=2,wins=8,losses=2,player_key="player14")
        self.__add_result(rank=None,expected_rank=2,wins=8,losses=2,player_key="player13")
        self.__add_result(rank=None,expected_rank=2,wins=8,losses=2,player_key="player12")
        self.__add_result(rank=None,expected_rank=2,wins=8,losses=2,player_key="player11")
        self.__add_result(rank=None,expected_rank=6,wins=7,losses=3,player_key="player10")
        self.__add_result(rank=None,expected_rank=7,wins=6,losses=4,player_key="player9")
        self.__add_result(rank=None,expected_rank=7,wins=6,losses=4,player_key="player8")
        self.__add_result(rank=None,expected_rank=9,wins=5,losses=5,player_key="player7")
        self.__add_result(rank=None,expected_rank=10,wins=4,losses=6,player_key="player6")
        self.__add_result(rank=None,expected_rank=11,wins=3,losses=7,player_key="player5")
        self.__add_result(rank=None,expected_rank=12,wins=2,losses=8,player_key="player4")
        self.__add_result(rank=None,expected_rank=13,wins=1,losses=9,player_key="player3")
        self.__add_result(rank=None,expected_rank=14,wins=0,losses=10,player_key="player2")
        self.__add_result(rank=None,expected_rank=14,wins=0,losses=10,player_key="player1")

        self.__run_assign_rank_test(winner="player15")

    def __t2_winner_missing(self):
        self.__week_results = []
        self.__add_result(rank=None,expected_rank=1,wins=8,losses=2,player_key="player15")
        self.__add_result(rank=None,expected_rank=2,wins=8,losses=2,player_key="player14")
        self.__add_result(rank=None,expected_rank=2,wins=8,losses=2,player_key="player13")
        self.__add_result(rank=None,expected_rank=4,wins=8,losses=2,player_key="player12")
        self.__add_result(rank=None,expected_rank=4,wins=8,losses=2,player_key="player11")
        self.__add_result(rank=None,expected_rank=6,wins=7,losses=3,player_key="player10")
        self.__add_result(rank=None,expected_rank=8,wins=6,losses=4,player_key="player9")
        self.__add_result(rank=None,expected_rank=8,wins=6,losses=4,player_key="player8")
        self.__add_result(rank=None,expected_rank=10,wins=5,losses=5,player_key="player7")
        self.__add_result(rank=None,expected_rank=12,wins=4,losses=6,player_key="player6")
        self.__add_result(rank=None,expected_rank=14,wins=3,losses=7,player_key="player5")
        self.__add_result(rank=None,expected_rank=16,wins=2,losses=8,player_key="player4")
        self.__add_result(rank=None,expected_rank=18,wins=1,losses=9,player_key="player3")
        self.__add_result(rank=None,expected_rank=20,wins=0,losses=10,player_key="player2")
        self.__add_result(rank=None,expected_rank=20,wins=0,losses=10,player_key="player1")

        with self.assertRaises(Exception):
            self.__run_assign_rank_test(winner="playerxxx",num_tests=1)

    def __t2_winner_insane(self):
        self.__week_results = []
        self.__add_result(rank=None,expected_rank=1,wins=8,losses=2,player_key="player15")
        self.__add_result(rank=None,expected_rank=2,wins=8,losses=2,player_key="player14")
        self.__add_result(rank=None,expected_rank=2,wins=8,losses=2,player_key="player13")
        self.__add_result(rank=None,expected_rank=4,wins=8,losses=2,player_key="player12")
        self.__add_result(rank=None,expected_rank=4,wins=8,losses=2,player_key="player11")
        self.__add_result(rank=None,expected_rank=6,wins=7,losses=3,player_key="player10")
        self.__add_result(rank=None,expected_rank=8,wins=6,losses=4,player_key="player9")
        self.__add_result(rank=None,expected_rank=8,wins=6,losses=4,player_key="player8")
        self.__add_result(rank=None,expected_rank=10,wins=5,losses=5,player_key="player7")
        self.__add_result(rank=None,expected_rank=12,wins=4,losses=6,player_key="player6")
        self.__add_result(rank=None,expected_rank=14,wins=3,losses=7,player_key="player5")
        self.__add_result(rank=None,expected_rank=16,wins=2,losses=8,player_key="player4")
        self.__add_result(rank=None,expected_rank=18,wins=1,losses=9,player_key="player3")
        self.__add_result(rank=None,expected_rank=20,wins=0,losses=10,player_key="player2")
        self.__add_result(rank=None,expected_rank=20,wins=0,losses=10,player_key="player1")

        with self.assertRaises(Exception):
            self.__run_assign_rank_test(winner="player8",num_tests=1)

    def __t3_wins_all_different(self):
        self.__week_results = []
        self.__add_result(projected_rank=None,expected_rank=11,projected_wins=0)
        self.__add_result(projected_rank=None,expected_rank=10,projected_wins=1)
        self.__add_result(projected_rank=None,expected_rank=9,projected_wins=2)
        self.__add_result(projected_rank=None,expected_rank=8,projected_wins=3)
        self.__add_result(projected_rank=None,expected_rank=7,projected_wins=4)
        self.__add_result(projected_rank=None,expected_rank=6,projected_wins=5)
        self.__add_result(projected_rank=None,expected_rank=5,projected_wins=6)
        self.__add_result(projected_rank=None,expected_rank=4,projected_wins=7)
        self.__add_result(projected_rank=None,expected_rank=3,projected_wins=8)
        self.__add_result(projected_rank=None,expected_rank=2,projected_wins=9)
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=10)

        self.__run_assign_projected_rank_test()

    def __t3_week_not_started(self): 
        # in the week not started case, player projected to win all games
        # all should be tied for first place
        self.__week_results = []
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=10)
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=10)
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=10)
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=10)
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=10)
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=10)
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=10)
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=10)
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=10)
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=10)
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=10)

        self.__run_assign_projected_rank_test()

    def __t3_week_not_started_with_defaulters(self): 
        # in the week not started case, players with picks projected to win all games
        # defaulters should be projected to win 0 games
        # players with picks tied for 1st, defaulters tied for last place
        self.__week_results = []
        self.__add_result(projected_rank=None,expected_rank=8,projected_wins=0)
        self.__add_result(projected_rank=None,expected_rank=8,projected_wins=0)
        self.__add_result(projected_rank=None,expected_rank=8,projected_wins=0)
        self.__add_result(projected_rank=None,expected_rank=8,projected_wins=0)
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=10)
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=10)
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=10)
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=10)
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=10)
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=10)
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=10)

        self.__run_assign_projected_rank_test()

    def __t3_week_not_started_with_some_missing_picks(self): 
        # players with all picks expect to win all games
        # players missing picks expect to lost those games
        self.__week_results = []
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=10)
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=10)
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=10)
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=10)
        self.__add_result(projected_rank=None,expected_rank=5,projected_wins=9)
        self.__add_result(projected_rank=None,expected_rank=5,projected_wins=9)
        self.__add_result(projected_rank=None,expected_rank=7,projected_wins=5)
        self.__add_result(projected_rank=None,expected_rank=8,projected_wins=4)
        self.__add_result(projected_rank=None,expected_rank=9,projected_wins=0)
        self.__add_result(projected_rank=None,expected_rank=9,projected_wins=0)

        self.__run_assign_projected_rank_test()

    def __t3_wins_with_ties(self): 
        self.__week_results = []
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=10)
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=10)
        self.__add_result(projected_rank=None,expected_rank=3,projected_wins=9)
        self.__add_result(projected_rank=None,expected_rank=3,projected_wins=9)
        self.__add_result(projected_rank=None,expected_rank=5,projected_wins=8)
        self.__add_result(projected_rank=None,expected_rank=5,projected_wins=8)
        self.__add_result(projected_rank=None,expected_rank=7,projected_wins=7)
        self.__add_result(projected_rank=None,expected_rank=7,projected_wins=7)
        self.__add_result(projected_rank=None,expected_rank=9,projected_wins=6)
        self.__add_result(projected_rank=None,expected_rank=9,projected_wins=6)
        self.__add_result(projected_rank=None,expected_rank=11,projected_wins=5)
        self.__add_result(projected_rank=None,expected_rank=11,projected_wins=5)
        self.__add_result(projected_rank=None,expected_rank=13,projected_wins=4)
        self.__add_result(projected_rank=None,expected_rank=13,projected_wins=4)
        self.__add_result(projected_rank=None,expected_rank=15,projected_wins=3)
        self.__add_result(projected_rank=None,expected_rank=15,projected_wins=3)
        self.__add_result(projected_rank=None,expected_rank=17,projected_wins=2)
        self.__add_result(projected_rank=None,expected_rank=17,projected_wins=2)
        self.__add_result(projected_rank=None,expected_rank=19,projected_wins=1)
        self.__add_result(projected_rank=None,expected_rank=19,projected_wins=1)
        self.__add_result(projected_rank=None,expected_rank=21,projected_wins=0)
        self.__add_result(projected_rank=None,expected_rank=21,projected_wins=0)

        self.__run_assign_projected_rank_test()

    def __t3_less_than_10_wins(self): 
        self.__week_results = []
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=7)
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=7)
        self.__add_result(projected_rank=None,expected_rank=3,projected_wins=6)
        self.__add_result(projected_rank=None,expected_rank=4,projected_wins=5)
        self.__add_result(projected_rank=None,expected_rank=5,projected_wins=4)
        self.__add_result(projected_rank=None,expected_rank=6,projected_wins=3)
        self.__add_result(projected_rank=None,expected_rank=6,projected_wins=3)
        self.__add_result(projected_rank=None,expected_rank=8,projected_wins=0)

        self.__run_assign_projected_rank_test()

    def __t3_all_wins_0(self): 
        self.__week_results = []
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=0)
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=0)
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=0)
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=0)
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=0)
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=0)
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=0)
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=0)

        self.__run_assign_projected_rank_test()

    def __t3_first_place_ties(self): 
        self.__week_results = []
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=8)
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=8)
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=8)
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=8)
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=8)
        self.__add_result(projected_rank=None,expected_rank=6,projected_wins=5)
        self.__add_result(projected_rank=None,expected_rank=7,projected_wins=4)
        self.__add_result(projected_rank=None,expected_rank=8,projected_wins=3)
        self.__add_result(projected_rank=None,expected_rank=9,projected_wins=2)
        self.__add_result(projected_rank=None,expected_rank=10,projected_wins=1)

        self.__run_assign_projected_rank_test()

    def __t3_winner_specified(self): 
        self.__week_results = []
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=8,player_key="player8")
        self.__add_result(projected_rank=None,expected_rank=2,projected_wins=7,player_key="player7")
        self.__add_result(projected_rank=None,expected_rank=3,projected_wins=6,player_key="player6")
        self.__add_result(projected_rank=None,expected_rank=4,projected_wins=5,player_key="player5")
        self.__add_result(projected_rank=None,expected_rank=5,projected_wins=4,player_key="player4")
        self.__add_result(projected_rank=None,expected_rank=6,projected_wins=3,player_key="player3")
        self.__add_result(projected_rank=None,expected_rank=7,projected_wins=2,player_key="player2")
        self.__add_result(projected_rank=None,expected_rank=8,projected_wins=1,player_key="player1")

        self.__run_assign_projected_rank_test(projected_winner="player8")

    def __t3_first_place_tie_with_winner_specified(self): 
        self.__week_results = []
        self.__add_result(projected_rank=None,expected_rank=2,projected_wins=7,player_key="player1")
        self.__add_result(projected_rank=None,expected_rank=2,projected_wins=7,player_key="player2")
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=7,player_key="player3")
        self.__add_result(projected_rank=None,expected_rank=2,projected_wins=7,player_key="player4")
        self.__add_result(projected_rank=None,expected_rank=2,projected_wins=7,player_key="player5")
        self.__add_result(projected_rank=None,expected_rank=6,projected_wins=6,player_key="player6")
        self.__add_result(projected_rank=None,expected_rank=7,projected_wins=5,player_key="player7")
        self.__add_result(projected_rank=None,expected_rank=8,projected_wins=4,player_key="player8")
        self.__add_result(projected_rank=None,expected_rank=9,projected_wins=3,player_key="player9")
        self.__add_result(projected_rank=None,expected_rank=10,projected_wins=2,player_key="player10")
        self.__add_result(projected_rank=None,expected_rank=11,projected_wins=1,player_key="player11")

        self.__run_assign_projected_rank_test(projected_winner="player3")

    def __t3_winner_missing(self): 
        self.__week_results = []
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=7,player_key="player1")
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=7,player_key="player2")
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=7,player_key="player3")
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=7,player_key="player4")
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=7,player_key="player5")
        self.__add_result(projected_rank=None,expected_rank=6,projected_wins=6,player_key="player6")

        with self.assertRaises(Exception):
            self.__run_assign_projected_rank_test(projected_winner="playerxxx",num_tests=1)

    def __t3_winner_insane(self): 
        self.__week_results = []
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=7,player_key="player1")
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=7,player_key="player2")
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=7,player_key="player3")
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=7,player_key="player4")
        self.__add_result(projected_rank=None,expected_rank=1,projected_wins=7,player_key="player5")
        self.__add_result(projected_rank=None,expected_rank=6,projected_wins=6,player_key="player6")

        with self.assertRaises(Exception):
            self.__run_assign_projected_rank_test(projected_winner="player6",num_tests=1)





    def __randomize_results_order(self):
        indexes = range(len(self.__week_results))
        random.shuffle(indexes)

        random_results = []
        for i in indexes:
            random_results.append(self.__week_results[i])

        self.__week_results = random_results

    def __add_result(self,rank=None,projected_rank=None,expected_rank=None,player_key=None,wins=None,losses=None,projected_wins=None,possible_wins=None):
        result = WeekResults()
        result.rank = rank
        result.player_key = player_key
        result.player_name = str(expected_rank)
        result.wins = wins
        result.losses = losses
        result.win_pct = None
        result.projected_wins = projected_wins
        result.possible_wins = possible_wins
        result.winner = None
        self.__week_results.append(result)

    def __verify_ranks(self,results):
        for result in results:
            expected_rank = int(result.player_name)
            self.assertEqual(result.rank,expected_rank)

    def __verify_projected_ranks(self,results):
        for result in results:
            expected_rank = int(result.player_name)
            self.assertEqual(result.projected_rank,expected_rank)

    def __verify_all_ranks_tied_for_first(self,results):
        for result in results:
            self.assertEqual(result.rank,1)

    def __run_assign_rank_test(self,num_tests=10,winner=None):
        u = Update()
        random.seed(777)
        for i in range(num_tests):
            self.__randomize_results_order()
            if not(winner):
                assigned_results = u.assign_rank(self.__week_results)
            else:
                assigned_results = u.assign_rank(self.__week_results,winner=winner)
            self.__verify_ranks(assigned_results)

    def __run_assign_projected_rank_test(self,num_tests=10,projected_winner=None):
        u = Update()
        random.seed(888)
        for i in range(num_tests):
            self.__randomize_results_order()
            if not(projected_winner):
                assigned_results = u.assign_projected_rank(self.__week_results)
            else:
                assigned_results = u.assign_projected_rank(self.__week_results,projected_winner=projected_winner)
            self.__verify_projected_ranks(assigned_results)

    def __test_get_week_results(self,year,week_number,expected_results):
        u = Update()
        results = u.get_week_results(year,week_number)
        #self.__debug_print_results(results,title="Results")
        #self.__debug_print_results(expected_results,title="Expected Results")
        #self.__verify_results(results,expected_results)
        self.__verify_results_ignore_tied_order(results,expected_results)

    def __verify_results(self,results,expected_results):
        self.assertEqual(len(results),len(expected_results))
        for i in range(len(results)):
            self.assertEqual(results[i].rank,expected_results[i].rank)
            self.assertEqual(results[i].projected_rank,expected_results[i].projected_rank)
            self.assertEqual(results[i].player_id,expected_results[i].player_id)
            self.assertEqual(results[i].player_name,expected_results[i].player_name)
            self.assertEqual(results[i].wins,expected_results[i].wins)
            self.assertEqual(results[i].losses,expected_results[i].losses)
            self.assertEqual(results[i].win_pct,expected_results[i].win_pct)
            self.assertEqual(results[i].projected_wins,expected_results[i].projected_wins)
            self.assertEqual(results[i].possible_wins,expected_results[i].possible_wins)
            # TODO self.assertEqual(results[i].winner,expected_results.winner)

    def __verify_results_ignore_tied_order(self,results,expected_results):
        self.assertEqual(len(results),len(expected_results))

        first_place_wins = results[0].wins
        first_place_losses = results[0].losses

        for i in range(len(results)):
            result = results[i]
            expected = self.__find_expected_result(result,expected_results)

            # TODO:  temporary code, fix this after winner implemented
            # code does not currently figure out the winner so the rank
            # for the players tied for first will be wrong
            # current code:  first place ties all have a rank of 1
            # future correct code:  winner is in 1st place, others tied for 1st in 2nd place
            if result.wins == first_place_wins and result.losses == first_place_losses:
                self.assertEqual(result.rank,1)
                self.assertEqual(result.projected_rank,1)
            else:
                self.assertEqual(result.rank,expected.rank)
                self.assertEqual(result.projected_rank,expected.projected_rank)

            self.assertEqual(result.player_id,expected.player_id)
            self.assertEqual(result.player_name,expected.player_name)
            self.assertEqual(result.wins,expected.wins)
            self.assertEqual(result.losses,expected.losses)
            self.assertEqual(result.win_pct,expected.win_pct)
            self.assertEqual(result.projected_wins,expected.projected_wins)
            self.assertEqual(result.possible_wins,expected.possible_wins)
            # TODO self.assertEqual(resultswinner,expected.winner)

    def __find_expected_result(self,result,expected_results):
        for expected in expected_results:
            if expected.player_name == result.player_name:
                return expected
        raise AssertionError,"could not find expected result"

    def __debug_print_ranks(self,results):
        print ""
        print "Rank  Expected  Wins  Losses  Player Key"
        print "----  --------  ----  ------  ----------"
        for result in results:
            print "%4s  %8s  %4s  %6s  %10s" % (result.rank,result.player_name,result.wins,result.losses,result.player_key)
        print ""

    def __debug_print_results(self,results,title=None):
        print ""
        if title:
            print "-----------------------------------------------------------------------------------"
            print "%s" % (title)
            print "-----------------------------------------------------------------------------------"
        print "Rank  Id                 Name             Wins  Losses  Projected  Possible"
        print "----  -----------------  ---------------  ----  ------  ---------  --------"
        for result in results:
            print "%4s  %17s  %15s  %4s  %6s  %9s  %8s" % (result.rank,result.player_id,result.player_name,result.wins,result.losses,result.projected_wins,result.possible_wins)
        print ""


