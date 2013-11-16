import unittest
from google.appengine.ext import db
from code.database import *
import time
import logging
import datetime

# TODO check data types?

class TestDatabase(unittest.TestCase):

    def test_check_for_weeks_in_database(self):
        weeks_2012 = range(1,14)
        weeks_2013 = range(1,12)    # year 2013 is not finished yet
        for week in weeks_2012:
            self.__test_week_query(2012,week)
        for week in weeks_2013:
            self.__test_week_query(2013,week)
        # TODO check week state?

    def test_check_for_invalid_weeks_in_database(self):
        self.__test_invalid_week_query(year=2012,week_number=14)
        self.__test_invalid_week_query(year=2012,week_number=0)
        self.__test_invalid_week_query(year=1900,week_number=1)

    def test_week_games_query_and_game_states(self):
        weeks_2012 = range(1,14)
        weeks_2013 = range(1,12)    # year 2013 is not finished yet
        for week in weeks_2012:
            self.__test_week_games_query_and_game_state(2012,week)
        for week in weeks_2013:
            self.__test_week_games_query_and_game_state(2013,week)

    def __disable_test_week_picks_query_and_pick_states(self):
        weeks_2012 = range(1,14)
        weeks_2013 = range(1,12)    # year 2013 is not finished yet
        for week in weeks_2012:
            logging.info("Picks test %d week %d" % (2012,week))
            self.__test_week_picks_query_and_pick_states(2012,week)
        for week in weeks_2013:
            logging.info("Picks test %d week %d" % (2013,week))
            self.__test_week_picks_query_and_pick_states(2013,week)

    def test_load_week_data(self):
        weeks_2012 = range(1,14)
        weeks_2013 = range(1,12)    # year 2013 is not finished yet
        for week in weeks_2012:
            logging.info("Load week test %d week %d" % (2012,week))
            self.__test_load_week_data(2012,week)
        for week in weeks_2013:
            logging.info("Load week test %d week %d" % (2013,week))
            self.__test_load_week_data(2013,week)


    def __load_2013_week_1(self):
        week_query = db.GqlQuery('SELECT * FROM Week WHERE year=2013 and number=1')
        if week_query:
            return list(week_query)[0]

    def __load_week(self,year,week_number):
        week_query = db.GqlQuery('SELECT * FROM Week WHERE year=:year and number=:number',year=year,number=week_number)
        if week_query:
            return list(week_query)[0]

    def __test_load_week_data(self,year,week_number):
        d = Database()
        week,games,picks = d.load_week_data(year,week_number)
        self.assertIsNotNone(week)
        self.assertEqual(week.number,week_number)
        self.assertEqual(week.year,year)
        self.assertEqual(len(games),10)
        self.assertGreater(len(picks),0)

    def _tmp_test_load_week_data_time(self):
        start = time.time()
        d = Database()
        week,games,picks = d.load_week_data(2013,3)
        elapsed_time = time.time()-start
        logging.debug("Elapsed load time = %f" % (elapsed_time))
        self.assertLess(elapsed_time,2.00)
        self.assertTrue(False)


    def __test_week_query(self,year,week_number):
        week_query = db.GqlQuery('SELECT * FROM Week WHERE year=:year and number=:number',year=year,number=week_number)
        self.assertIsNotNone(week_query)
        weeks = list(week_query)
        self.assertEqual(len(weeks),1)
        week = weeks[0]
        self.assertEqual(week.year,year)
        self.assertEqual(week.number,week_number)
        self.assertEqual(len(week.games),10)
        if week.winner != None:
            self.__check_key_exists(week.winner)

    def __test_invalid_week_query(self,year,week_number):
        week_query = db.GqlQuery('SELECT * FROM Week WHERE year=:year and number=:number',year=year,number=week_number)
        self.assertIsNotNone(week_query)
        weeks = list(week_query)
        self.assertEqual(len(weeks),0)

    def __test_week_games_query_and_game_state(self,year,week_number):
        week = self.__load_week(year,week_number)
        self.assertIsNotNone(week)
        games = []
        for game_key in week.games:
            games.append(db.get(game_key))
        self.assertTrue(len(games) == 10)
        self.__check_week_game_numbers(games)
        self.__check_game_state(games)

    def __check_week_game_numbers(self,games):
        game_number_counts = self.__initialize_game_number_counts_to_0()
        for game in games:
            self.__check_game_number_is_valid(game.number)
            self.__track_game_number_count(game_number_counts,game.number)
        self.__verify_one_game_exists_for_each_game_number(game_number_counts)

    def __check_game_number_is_valid(self,number):
        self.assertIn(number,range(1,11))

    def __track_game_number_count(self,game_number_counts,game_number):
        game_number_counts[game_number] += 1

    def __initialize_game_number_counts_to_0(self):
        return { week_number:0 for week_number in range(1,11) }

    def __verify_one_game_exists_for_each_game_number(self,game_numbers):
        for number in range(1,11):
            self.assertEqual(game_numbers[number],1)

    def __check_game_state(self,games):
        for game in games:
            self.assertIn(game.state,['not_started','in_progress','final'])
            self.assertIsNotNone(game.team1)
            self.assertIsNotNone(game.team2)
            self.assertIsNotNone(game.favored)
            self.assertIsNotNone(game.spread)
            self.__check_key_exists(game.team1)
            self.__check_key_exists(game.team2)
            if game.state == "not_started":
                self.assertIsNone(game.team1_score)
                self.assertIsNone(game.team2_score)
            elif game.state == "in_progress":
                self.assertIsNotNone(game.team1_score)
                self.assertIsNotNone(game.team2_score)
            elif game.state == "final":
                self.assertIsNotNone(game.team1_score)
                self.assertIsNotNone(game.team2_score)

    def __test_week_picks_query_and_pick_states(self,year,week_number):
        week = self.__load_week(year,week_number)
        self.assertIsNotNone(week)
        picks_query = db.GqlQuery('SELECT * FROM Pick WHERE week=:week_key',week_key=str(week.key()))
        self.assertIsNotNone(picks_query)
        picks = list(picks_query)
        self.assertGreater(len(picks),0)
        for pick in picks:
            self.__check_pick_state(pick)

    def __check_pick_state(self,pick):
        self.assertIsNotNone(pick.week)
        self.assertIsNotNone(pick.player)
        self.assertIsNotNone(pick.game)
        self.__check_pick_winner_value(pick.winner)
        current_time = datetime.datetime.now()
        self.assertLess(pick.created,current_time)
        self.assertLess(pick.modified,current_time)
        self.__check_key_exists(pick.week)
        self.__check_key_exists(pick.player)
        self.__check_key_exists(pick.game)

        game = db.get(db.Key(pick.game))
        if game.number != 10:
            self.assertIsNone(pick.team1_score)
            self.assertIsNone(pick.team2_score)
        # game 10: score could be None or an int
        # if score is None then the player did not enter a score for the tiebreaker

        # TODO check instance object type (dbkey.kind() == "Game")
        # TODO check invalid key value

    def __log_pick_info(self,pick):
        week = db.get(db.Key(pick.week))
        player = db.get(db.Key(pick.player))
        game = db.get(db.Key(pick.game))
        team1 = db.get(db.Key(game.team1))
        team2 = db.get(db.Key(game.team2))
        logging.info("%d Week %d Player %s Game %s vs. %s" % (week.year,week.number,player.name,team1.name,team2.name))

    def __check_key_exists(self,key_value):
        value = db.get(db.Key(key_value))
        self.assertIsNotNone(value)

    def __check_pick_winner_value(self,winner):
        pick_not_entered = winner == None
        if pick_not_entered:
            return
        self.assertIn(winner,["team1","team2"])

    def _tmp_test_weeks_database(self):
        pass
        """
        years = [ 2012 ]
        weeks = range(1,14)
        for year in years:
            for week in weeks:
                q = db.GqlQuery('SELECT * FROM Week WHERE year=:year and number=:week',year=year,number=week)
                self.assertIsNotNone(q)
                self.assertTrue(len(list(q))==1)
        bad_years = [ 1000 ]
        for year in bad_years:
            for week in weeks:
                q = db.GqlQuery('SELECT * FROM Week WHERE year=:year and number=:week',year=year,number=week)
                self.assertIsNotNone(q)
                self.assertTrue(len(list(q))==0)
        bad_weeks = [ -1, 14, 20 ]
        for year in year:
            for week in bad_weeks:
                q = db.GqlQuery('SELECT * FROM Week WHERE year=:year and number=:week',year=year,number=week)
                self.assertIsNotNone(q)
                self.assertTrue(len(list(q))==0)
        """

#if __name__ == "__main__":
    #unittest.main()
