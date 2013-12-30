from google.appengine.ext import db
from google.appengine.api import memcache
import logging
import time
from week_data import *

# TODO:  test load teams, load players

class Database:

    def is_week_valid(self,week,year,update=False):
        weeks_and_years = self.load_weeks_and_years(update)
        return (year in weeks_and_years) and (week in weeks_and_years[year])

    def load_week_data(self,year,week_number,update=False):
        data = WeekData()
        data.week = self.__get_week_in_database(year,week_number,update)
        data.games = self.__get_week_games_in_database(data.week,update)
        data.player_picks = self.__get_player_week_picks_in_database(data.week,update)
        data.picks = self.__get_week_picks_in_database(data.week,update)
        data.players = self.load_players(data.week.year,update)
        data.teams = self.load_teams(update)
        return data

    def get_week_numbers(self,year,update=False):
        weeks_and_years = self.load_weeks_and_years(update)
        return sorted(weeks_and_years[year])

    def get_years(self,update=False):
        weeks_and_years = self.load_weeks_and_years(update)
        return sorted(weeks_and_years.keys())

    def load_weeks_and_years(self,update=False):
        key = "weeks_and_years"
        weeks_and_years = memcache.get(key)
        if update or not(weeks_and_years):
            weeks_and_years = self.__load_week_numbers_and_years()
            memcache.set(key,weeks_and_years)
        return weeks_and_years

    def load_players(self,year,update=False):
        key = "players_%d" % (year)
        players = memcache.get(key)
        if update or not(players):
            players_query = db.GqlQuery('select * from Player where years IN :year',year=[year])
            assert players_query != None
            results = list(players_query)
            players = { str(player.key()):player for player in results }
            memcache.set(key,players)
        return players


    def load_teams(self,update=False):
        key = "teams"
        teams = memcache.get(key)
        if update or not(teams):
            teams_query = db.GqlQuery('select * from Team')
            assert teams_query != None
            results = list(teams_query)
            teams = { str(team.key()):team for team in results }
            memcache.set(key,teams)
        return teams


    def load_week_data_timed(self,year,week_number,update=False):
        start = time.time()
        week = self.__get_week_in_database(year,week_number,update)
        week_elapsed_time = time.time()-start
        start = time.time()
        games = self.__get_week_games_in_database(week,update)
        games_elapsed_time = time.time()-start
        start = time.time()
        picks = self.__get_player_week_picks_in_database(week,update)
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
            assert len(weeks) == 1,"Found %d weeks for %d week %d" % (len(weeks),year,week_number)
            week = weeks[0]
            memcache.set(key,week)
        return week

    def __get_week_games_in_database(self,week,update):
        key = "games_%d_%d" % (week.year,week.number)
        games = memcache.get(key)
        if update or not(games):
            games = { str(game_key):db.get(game_key) for game_key in week.games }
            assert len(games) == 10
            memcache.set(key,games)
        return games

    def __get_player_week_picks_in_database(self,week,update):
        key = "player_picks_%d_%d" % (week.year,week.number)
        player_picks = memcache.get(key)
        week_key = str(week.key())
        if update or not(player_picks):
            picks_query = db.GqlQuery('select * from Pick where week=:week',week=week_key)
            assert picks_query != None
            picks = list(picks_query) 

            players = self.load_players(week.year,update)
            player_picks = { player_key:[] for player_key in players }

            for pick in picks:
                player_picks[pick.player].append(pick)

            memcache.set(key,player_picks)

        return player_picks

    def __get_week_picks_in_database(self,week,update):
        key = "week_picks_%d_%d" % (week.year,week.number)
        week_picks = memcache.get(key)
        week_key = str(week.key())
        if update or not(week_picks):
            picks_query = db.GqlQuery('select * from Pick where week=:week',week=week_key)
            assert picks_query != None
            picks = list(picks_query) 

            week_picks = { str(pick.key()):pick for pick in picks }
            memcache.set(key,week_picks)

        return week_picks

    def __load_week_numbers_and_years(self):
        weeks_query = db.GqlQuery('select * from Week')
        assert weeks_query != None
        weeks = list(weeks_query)

        week_numbers_and_years = dict()

        for week in weeks:
            year = int(week.year)
            week_number = int(week.number)
            if year not in week_numbers_and_years:
                week_numbers_and_years[year] = [ week_number ]
            else:
                week_numbers_and_years[year].append(week_number)

        return week_numbers_and_years
