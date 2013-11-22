from google.appengine.ext import db
from google.appengine.api import memcache
import logging
import time

# TODO:  test load teams
# TODO:  implement and test load players


class Database:

    def load_players(self,year):
        pass

    def load_week_data(self,year,week_number,update=False):
        week = self.__get_week_in_database(year,week_number,update)
        games = self.__get_week_games_in_database(week,update)
        picks = self.__get_player_week_picks_in_database(week,update)
        return week,games,picks

    def load_teams(self,update=False):
        key = "teams"
        teams = memcache.get(key)
        if update or not(teams):
            teams_query = db.GqlQuery('select * from Team')
            assert teams_query != None
            teams = list(teams_query)
            memcache.set(key,teams)
        return teams


    def load_week_data_timed(self,year,week_number):
        start = time.time()
        week = self.__get_week_in_database(year,week_number)
        week_elapsed_time = time.time()-start
        start = time.time()
        games = self.__get_week_games_in_database(week)
        games_elapsed_time = time.time()-start
        start = time.time()
        picks = self.__get_player_week_picks_in_database(week)
        picks_elapsed_time = time.time()-start
        logging.info("Load weeks = %f" % (week_elapsed_time))
        logging.info("Load games = %f" % (games_elapsed_time))
        logging.info("Load picks = %f" % (picks_elapsed_time))
        return week,games,picks

    def __get_week_in_database(self,year,week_number,update):
        key = "week_%d_%d" % (year,week_number)
        week = memcache.get(key)
        if update or not(week):
            weeks_query = db.GqlQuery('SELECT * FROM Week WHERE year=:year and number=:week',year=year,week=week_number)
            assert weeks_query != None
            weeks = list(weeks_query)
            assert len(weeks) == 1
            week = weeks[0]
            memcache.set(key,week)
        return week

    def __get_week_games_in_database(self,week,update):
        key = "games_%d_%d" % (week.year,week.number)
        games = memcache.get(key)
        if update or not(games):
            games = []
            for game_key in week.games:
                games.append(db.get(game_key))
            assert len(games) == 10
            memcache.set(key,games)
        return games

    def __get_players_in_database(self,year,update):
        key = "players_%d" % (year)
        players = memcache.get(key)
        if update or not(players):
            players_query = db.GqlQuery('select * from Player where years IN :year',year=[year])
            assert players_query != None
            players = list(players_query)
            memcache.set(key,players)
        return players

    def __get_player_week_picks_in_database_v2(self,week):
        players = self.__get_players_in_database(week.year)

        player_picks = dict()
        for player in players:
            picks_query = db.GqlQuery('select * from Pick where week=:week and player=:player',week=week,player=player)
            assert picks_query != None
            picks = list(picks_query) 

            player_picks[player.name] = picks
        return player_picks

    def __get_player_week_picks_in_database(self,week,update):
        key = "player_picks_%d_%d" % (week.year,week.number)
        player_picks = memcache.get(key)
        if update or not(player_picks):
            picks_query = db.GqlQuery('select * from Pick where week=:week',week=week)
            assert picks_query != None
            picks = list(picks_query) 

            players = self.__get_players_in_database(week.year,update)
            player_picks = { player.name:[] for player in players }

            for pick in picks:
                # idea:  create key,value dict with player_key,player_name
                # idea:  create key,value dict with player_key,picks array
                player_picks[pick.player.name].append(pick)

            memcache.set(key,player_picks)

        return player_picks
