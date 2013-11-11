import unittest
from google.appengine.ext import db
from code.database import *
import time
import logging

class TestDatabase(unittest.TestCase):

    def __load_2013_week_1(self):
        week_query = db.GqlQuery('SELECT * FROM Week WHERE year=2013 and number=1')
        if week_query:
            return list(week_query)[0]

    def test_load_week_data(self):
        d = Database()
        week,games,picks = d.load_week_data(2013,2)
        self.assertIsNotNone(week)
        self.assertEqual(week.number,2)
        self.assertEqual(week.year,2013)
        self.assertEqual(len(games),10)
        self.assertGreater(len(picks),0)

    def test_load_week_data_time(self):
        start = time.time()
        d = Database()
        week,games,picks = d.load_week_data(2013,3)
        elapsed_time = time.time()-start
        logging.debug("Elapsed load time = %f" % (elapsed_time))
        self.assertLess(elapsed_time,2.00)
        self.assertTrue(False)

    def test_week_query(self):
        week_query = db.GqlQuery('SELECT * FROM Week WHERE year=2013 and number=1')
        self.assertTrue(week_query != None)
        weeks = list(week_query)
        self.assertTrue(len(weeks) == 1)
        week = weeks[0]
        self.assertTrue(week.year == 2013)
        self.assertTrue(week.number == 1)
        self.assertTrue(len(week.games) == 10)

    def test_week_games_query(self):
        week = self.__load_2013_week_1()
        games = []
        for game_key in week.games:
            games.append(db.get(game_key))
        self.assertTrue(len(games) == 10)

    def test_week_picks_query(self):
        week = self.__load_2013_week_1()
        picks_query = db.GqlQuery('SELECT * FROM Pick WHERE week=:week',week=week)
        self.assertTrue(picks_query != None)
        picks = list(picks_query)
        self.assertTrue(len(picks) > 0)

    def test_weeks_database(self):
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
