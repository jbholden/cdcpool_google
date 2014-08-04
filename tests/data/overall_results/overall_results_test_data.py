from google.appengine.ext import db
from google.appengine.api import memcache
from code.database import *
from code.week_results import *
from code.player_results import *
from code.week_data import *
from code.update import *
from models.weeks import *
from models.games import *
from models.players import *
from models.picks import *
from models.saved_keys import *
import logging
from utils.utils import *


class OverallResultsTestData:

    def __init__(self,year,data_name='OverallResultsTestData',leave_objects_in_datastore=False):
        self.year = year
        self.data_name = data_name
        self.leave_objects_in_datastore=leave_objects_in_datastore
        self.__saved_keys = []
        self.weeks = dict()

    def __del__(self):
        if not(self.leave_objects_in_datastore):
            self.cleanup()

    def setup(self):
        self.__saved_keys = []
        self.games = dict()
        self.__load_teams()
        self.setup_database()
        if self.leave_objects_in_datastore:
            self.save_keys_to_database()

    def setup_database(self):
        pass

    def save_keys_to_database(self):
        s = SavedKeys()
        s.name = self.data_name
        s.key_list = [ str(key) for key in self.__saved_keys ]
        s.put()

    def setup_picks_done(self,year,number):
        u = Update()
        u.update_week_results(year,number)

    def delete_keys_from_database(self):
        query = SavedKeys.all()
        if not(query):
            return
        for q in query:
            if q.name == self.data_name:
                for key in q.key_list:
                    db.delete(db.Key(key))
                db.delete(q)

    def cleanup_database(self):
        self.delete_keys_from_database()
        self.cleanup()
        memcache.flush_all()

    def cleanup(self):
        if self.__saved_keys:
            for key in self.__saved_keys:
                db.delete(key)
            self.__saved_keys = []

    def setup_game(self,game):
        game_key = game.put()
        self.__saved_keys.append(game_key)
        self.games[game.number] = game_key

    def setup_week(self,week):
        if len(self.games) > 0:
            week.games = self.games.values()
        week_key = week.put()
        self.__saved_keys.append(week_key)
        self.weeks[week.number] = str(week_key)
        u = Update()
        u.update_years_and_week_numbers()

    def setup_players(self,player_names):
        players = dict()
        for name in player_names:
            player_key = self.__create_player(name)
            players[name] = str(player_key)
        self.players = players
        u = Update()
        u.update_players(self.year)

    def __create_player(self,name):
        p = Player(name=name,years=[self.year])
        player_key = p.put()
        self.__saved_keys.append(player_key)
        return player_key

    def setup_final_game(self,year,week_number,number,team1,team2,favored,spread,team1_score,team2_score):
        team1_key = self.find_team_key(team1)
        team2_key = self.find_team_key(team2)
        game = Game(number=number,team1=team1_key,team2=team2_key,team1_score=team1_score,team2_score=team2_score,favored=favored,spread=spread,state="final",quarter=None,time_left=None,date=None)
        self.setup_game(game)

    def setup_not_started_game(self,year,week_number,number,team1,team2,favored,spread,start_date):
        team1_key = self.find_team_key(team1)
        team2_key = self.find_team_key(team2)
        if start_date:
            start_date_utc = get_datetime_in_utc(start_date,'US/Eastern')
        else:
            start_date_utc = None
        game = Game(number=number,team1=team1_key,team2=team2_key,team1_score=None,team2_score=None,favored=favored,spread=spread,state="not_started",quarter=None,time_left=None,date=start_date_utc)
        self.setup_game(game)

    def setup_in_progress_game(self,year,week_number,number,team1,team2,favored,spread,team1_score,team2_score,quarter,time_left):
        team1_key = self.find_team_key(team1)
        team2_key = self.find_team_key(team2)
        game = Game(number=number,team1=team1_key,team2=team2_key,team1_score=team1_score,team2_score=team2_score,favored=favored,spread=spread,state="in_progress",quarter=quarter,time_left=time_left,date=None)
        self.setup_game(game)

    def setup_pick(self,year,week_number,player_name=None,week_number=None,game_number=None,winner=None,team1_score=None,team2_score=None):
        pick = Pick()

        if player_name:
            pick.player = str(self.players[player_name])

        if game_number:
            pick.game = str(self.games[game_number])

        if week_number:
            pick.week = str(self.weeks[week_number])

        if winner:
            pick.winner = winner

        if team1_score and team2_score:
            pick.team1_score = team1_score
            pick.team2_score = team2_score

        pick_key = pick.put()
        self.__saved_keys.append(pick_key)

    def find_team_key(self,team_name):
        for team_key in self.teams:
            team = self.teams[team_key]
            if team.name == team_name:
                return team_key
        raise AssertionError,"Could not find a team named %s" % (team_name)

    def __load_teams(self):
        database = Database()
        self.teams = database.load_teams('teams')
        self.team_keys = self.teams.keys()



