from google.appengine.ext import db
from code.database import *
from code.week_results import *
from code.week_data import *
from models.weeks import *
from models.games import *
from models.players import *
from models.picks import *

class ResultTestData:

    def __init__(self,year,week_number):
        self.year = year
        self.week_number = week_number

    def __del__(self):
        self.cleanup()

    def setup(self):
        self.__saved_keys = []
        self.results = []
        self.games = dict()
        self.picks = []
        memcache.flush_all()
        self.__load_teams()
        self.setup_database()
        self.__load_week_data()

    def setup_database(self):
        pass

    def cleanup(self):
        for key in self.__saved_keys:
            db.delete(key)
        self.__saved_keys = []

    def get_expected_results(self):
        return self.results

    def setup_players(self,player_names):
        players = dict()
        for name in player_names:
            player_key = self.__create_player(name)
            players[name] = player_key
        self.players = players

    def setup_game(self,game):
        game_key = game.put()
        self.__saved_keys.append(game_key)
        self.games[game.number] = game_key

    def setup_week(self):
        w = Week(year=self.year,number=self.week_number,winner=None,games=self.games.values(),lock_picks=None,lock_scores=None)
        week_key = w.put()
        self.__saved_keys.append(week_key)
        self.week = week_key

    def setup_pick(self,pick,player_name=None,game_number=None):
        if player_name:
            pick.player = str(self.players[player_name])

        if game_number:
            pick.game = str(self.games[game_number])

        pick.week = str(self.week)

        pick_key = pick.put()
        self.__saved_keys.append(pick_key)
        self.picks.append(pick_key)

    def add_result(self,rank=None,projected_rank=None,player_name=None,wins=None,losses=None,win_pct=None,projected_wins=None,possible_wins=None,winner=None):
        result = WeekResults()
        result.rank = rank
        result.projected_rank = projected_rank
        result.player_id = self.__get_player_id(player_name)
        result.player_name = player_name
        result.wins = wins
        result.losses = losses
        result.win_pct = "%0.3f" % (win_pct)
        result.projected_wins = projected_wins
        result.possible_wins = possible_wins

        result.winner = None
        if winner != None:
            result.winner = self.weekdata.get_player_key(winner)
        else:
            result.winner = None
        self.results.append(result)

    def __load_week_data(self):
        database = Database()
        self.weekdata = database.load_week_data(self.year,self.week_number)

    def __load_teams(self):
        database = Database()
        self.teams = database.load_teams()
        self.team_keys = self.teams.keys()

    def __get_player_id(self,player_name):
        player_key = self.weekdata.get_player_key(player_name)
        player = self.weekdata.get_player(player_key)
        return player.key().id()

    def __create_player(self,name):
        p = Player(name=name,years=[self.year])
        player_key = p.put()
        self.__saved_keys.append(player_key)
        return player_key
