ROOT_PATH = '../../.'
import sys
sys.path.append(ROOT_PATH)

import unittest
import socket
import logging
from scripts.api.fbpool_api import *
from scripts.api.fbpool_api_exception import *


class TestPlayer(unittest.TestCase):

    def setUp(self):
        url = "http://localhost:10090"
        self.fbpool = FBPoolAPI(url=url)

    def test_cache_flush(self):
        try:
            self.fbpool.deleteCache()
        except FBAPIException as e:
            print str(e)
            self.assertTrue(False)
            return

    def test_update_cache(self):
        try:
            self.fbpool.updateCache()
        except FBAPIException as e:
            print str(e)
            self.assertTrue(False)
            return

    def test_update_cache_year(self):
        try:
            self.fbpool.updateCacheForYear(2013)
        except FBAPIException as e:
            print str(e)
            self.assertTrue(False)
            return

    def test_update_cache_week(self):
        try:
            self.fbpool.updateCacheForWeek(year=2013,week=1)
        except FBAPIException as e:
            print str(e)
            self.assertTrue(False)
            return

if __name__ == "__main__":
    unittest.main()
