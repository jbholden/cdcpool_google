from google.appengine.ext import db
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


class OverallResultsTestData:

    def __init__(self,year,data_name='OverallResultsTestData',leave_objects_in_datastore=False):
        self.year = year
        self.data_name = data_name
        self.leave_objects_in_datastore=leave_objects_in_datastore
        self.__saved_keys = []

    def __del__(self):
        if not(self.leave_objects_in_datastore):
            self.cleanup()

    def setup(self):
        self.__saved_keys = []
        self.games = []
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
        self.week = week_key
        u = Update()
        u.update_week_results(week.year,week.number)

    def setup_players(self,player_names):
        players = dict()
        for name in player_names:
            player_key = self.__create_player(name)
            players[name] = player_key
        self.players = players
        u = Update()
        u.update_players(self.year)

    def __create_player(self,name):
        p = Player(name=name,years=[self.year])
        player_key = p.put()
        self.__saved_keys.append(player_key)
        return player_key



