from google.appengine.ext import db
from google.appengine.api import memcache
import logging
import time
import datetime
from utils.utils import *
from week_data import *
from calculator import *
from models.games import *
from models.weeks import *

# TODO:  test load teams, load players

class Database:

    # Use when creating new pick sheet, writes DB (Game and Week tables) and updates memcache
    def put_games_week_in_database(self,games,week):
        gamekeys = list()
        for index in games:
            g = Game()
            g.number = games[index]['number']
            g.team1 = games[index]['team1']
            g.team2 = games[index]['team2']
            g.favored = games[index]['favored']
            g.spread = games[index]['spread']
            g.state = games[index]['state']
            g.date = games[index]['date']
            gamekeys.append(g.put())

        w = Week(year=week['year'],number=week['number'])
        w.winner = None
        w.games = gamekeys
        weekkey = w.put()

        #update memcache
        week_entry = self.__get_week_in_database(week['year'],week['number'],update=True)
        self.__get_week_games_in_database(week_entry,update=True)
        self.load_weeks_and_years(update=True)

    def is_year_valid(self,year,update=False):
        weeks_and_years = self.load_weeks_and_years(update)
        return year in weeks_and_years

    def is_week_valid(self,week,year,update=False):
        weeks_and_years = self.load_weeks_and_years(update)
        return (year in weeks_and_years) and (week in weeks_and_years[year])

    def before_pick_deadline(self,year,week_number,update=False):
        # TODO: tests
        # visual tests:  user logged in, user logged out, before pick deadline
        # bad year, bad week number
        # cache test?
        week = self.__get_week_in_database(year,week_number,update=update)
        return self.__before_pick_deadline(week)

    def get_pick_deadline(self,year,week_number,update=False):
        # TODO:  tests
        week = self.__get_week_in_database(year,week_number,update=update)
        return week.lock_picks

    def get_next_year_week_for_create_week(self,update=False):
        # returns tuple that is (year, week)
        weeks_and_years = self.load_weeks_and_years(update)
        sorted_years = sorted(weeks_and_years.keys())
        if len(sorted_years) == 0:
          return ('2014','1')
        latest_year = int(sorted_years[-1])
        sorted_weeks = sorted(weeks_and_years[latest_year])
        latest_week = int(sorted_weeks[-1])
        if latest_week == 13:
          return (str(latest_year + 1), '1')
        else:
          return (str(latest_year), str(latest_week + 1))

    def load_week_data(self,year,week_number,update=False):
        data = WeekData()
        data.week = self.__get_week_in_database(year,week_number,update)
        data.games = self.__get_week_games_in_database(data.week,update)
        data.player_picks = self.__get_player_week_picks_in_database(data.week,update)
        data.picks = self.__get_week_picks_in_database(data.week,update)
        data.players = self.load_players(data.week.year,update)
        data.teams = self.load_teams("teams",update)
        return data

    def get_week_numbers(self,year,update=False):
        weeks_and_years = self.load_weeks_and_years(update)
        return sorted(weeks_and_years[year])

    def get_years(self,update=False):
        weeks_and_years = self.load_weeks_and_years(update)
        return sorted(weeks_and_years.keys())

    # see:  https://github.com/jbholden/cdcpool_google/issues/20
    def get_pool_state(self,year,update=False):
        # TODO tests
        if not(self.is_year_valid(year,update)):
            return "invalid"

        week_numbers = self.get_week_numbers(year)
        last_week_number = week_numbers[-1]

        week = self.__get_week_in_database(year,week_number=last_week_number,update=update)
        week_has_no_games = week.games == None or len(week.games) == 0

        only_week_one_exists = last_week_number == 1 and len(week_numbers) == 1

        if only_week_one_exists and week_has_no_games:
            return "not_started"

        assert not(week_has_no_games),"Every week should have games except for a week 1 exception"

        if self.__before_pick_deadline(week):
            return "enter_picks"

        week_state = self.__get_week_state(week,update)

        if last_week_number == 13 and week_state == "final":
            return "end_of_year"

        if week_state == "not_started":
            return "week_not_started"
        elif week_state == "in_progress":
            return "week_in_progress"
        elif week_state == "final":
            return "week_final"


    def __get_week_state(self,week,update=False):
        week_games = self.__get_week_games_in_database(week,update)

        week_data = WeekData()
        week_data.games = week_games
        calc = CalculateResults(week_data)
        return calc.get_summary_state_of_all_games()


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

    def delete_players_from_memcache(self,year):
        key = "players_%d" % (year)
        memcache.delete(key)

    # BLR - Added key argument...should be either "teams" or "teamkeys". The former returns
    #       a dict indexed on datastore key with values team name. The latter returns a dict
    #       indexed on team name with values datastore key.
    def load_teams(self,key,update=False):
        #key = "teams"
        teams = memcache.get(key)
        if update or not(teams):
            teams_query = db.GqlQuery('select * from Team')
            assert teams_query != None
            results = list(teams_query)
            if key == "teams":
              teams = { str(team.key()):team for team in results }
            elif key == "teamkeys":
              teams = { team.name:str(team.key()) for team in results }
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
            #assert len(games) == 10
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

    def __before_pick_deadline(self,week):
        if week.lock_picks == None:
            return False
        return get_current_time_in_utc() <= week.lock_picks
