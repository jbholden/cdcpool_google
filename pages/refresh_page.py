import webapp2
import logging
from handler import *
import string
import re
from google.appengine.api import memcache
from code.database import *

class RefreshPage(Handler):

    def get(self):
        memcache_keys = self.__get_memcache_keys()
        for memcache_key in memcache_keys:
            dummy = memcache.get(memcache_key)
        self.write("success")

    def __get_memcache_keys(self):
        static_keys = [ "weeks_and_years", "teams", "teamkeys"]
        api_keys = [ "players", "weeks_id", "weeks_key", "picks_id", "picks_key", "games_id", "games_key" ]
        #"players_<year>"
        #"week_<year>_<week>"
        #"games_<year>_<week>"
        #"player_picks_<year>_<week>"
        #"week_picks_<year>_<week>"
        #"week_results_<year>_<week>"
        #"player_results_<player_id>_<year>_<week>"
        #"week_games_<year>_<week>"
        #"overall_results_<year>"

        memcache_keys = static_keys + api_keys

        database = Database()
        weeks_and_years = database.load_weeks_and_years()
        for year in weeks_and_years:
            players = database.load_players(year)
            player_ids = [ player.key().id() for player in players.values()]

            memcache_keys.append("players_%d" % (year))
            memcache_keys.append("overall_results_%d" % (year))

            for week_number in weeks_and_years[year]:
                memcache_keys.append("week_%d_%d" % (year,week_number))
                memcache_keys.append("games_%d_%d" % (year,week_number))
                memcache_keys.append("player_picks_%d_%d" % (year,week_number))
                memcache_keys.append("week_picks_%d_%d" % (year,week_number))
                memcache_keys.append("week_results_%d_%d" % (year,week_number))
                memcache_keys.append("week_games_%d_%d" % (year,week_number))

                for player_id in player_ids:
                    key = "player_results_%d_%d_%d" % (player_id,year,week_number)
                    memcache_keys.append(key)

            return memcache_keys
