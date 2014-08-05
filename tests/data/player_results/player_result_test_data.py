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
from models.root import *


class PlayerResultTestData:

    def __init__(self,year,week_number,data_name='PlayerResultTestData',leave_objects_in_datastore=False):
        self.year = year
        self.week_number = week_number
        self.data_name = data_name
        self.leave_objects_in_datastore=leave_objects_in_datastore
        self.__saved_keys = []

    def __del__(self):
        if not(self.leave_objects_in_datastore):
            self.cleanup()

    def setup(self):
        self.__saved_keys = []
        self.player_results = dict()
        self.games = dict()
        self.picks = []
        self.__load_teams()
        self.setup_database()
        self.__load_week_data()
        self.setup_expected_results()
        if self.leave_objects_in_datastore:
            self.save_keys_to_database()

    def setup_database(self):
        pass

    def save_keys_to_database(self):
        s = SavedKeys(parent=root_savedkeys())
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
        database = Database()
        players = database.load_players(self.year)
        player_ids = [ player.key().id() for player in players.values()]

        if self.__saved_keys:
            for key in self.__saved_keys:
                db.delete(key)
            self.__saved_keys = []

        weeks_and_years = database.load_weeks_and_years(update=True)

        u = Update()
        for player_id in player_ids:
            u.delete_player_results_from_memcache(player_id,self.year,self.week_number)

        u.delete_week_results_from_memcache(self.year,self.week_number)
        database.delete_players_from_memcache(self.year)


    def setup_expected_results(self):
        pass

    def get_expected_results(self):
        return self.player_results

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

    def setup_week(self,lock_picks=None):
        parent = root_weeks()
        w = Week(year=self.year,number=self.week_number,winner=None,games=self.games.values(),lock_picks=lock_picks,lock_scores=None,parent=parent)
        week_key = w.put()
        self.__saved_keys.append(week_key)
        self.week = week_key

    def setup_pick(self,pick,player_name=None,game_number=None):
        # use self.year, self.week_number
        if player_name:
            pick.player = str(self.players[player_name])

        if game_number:
            pick.game = str(self.games[game_number])

        pick.week = str(self.week)

        pick_key = pick.put()
        self.__saved_keys.append(pick_key)
        self.picks.append(pick_key)

    def find_team_key(self,team_name):
        for team_key in self.teams:
            team = self.teams[team_key]
            if team.name == team_name:
                return team_key
        raise AssertionError,"Could not find a team named %s" % (team_name)


    def add_result(self,player_name=None,player_pick=None,result=None,team1=None,team2=None,team1_score=None,team2_score=None,game_state=None,favored=None,favored_spread=None,winning_team=None,game_spread=None,game_quarter=None,game_time_left=None,game_date=None,game_number=None,team1_tiebreak=None,team2_tiebreak=None):
        player_result = PlayerResult()
        player_result.player_pick = player_pick
        player_result.result = result
        player_result.team1 = team1
        player_result.team2 = team2
        player_result.team1_score = team1_score
        player_result.team2_score = team2_score
        player_result.game_state = game_state
        player_result.favored = favored
        player_result.favored_spread = favored_spread
        player_result.winning_team = winning_team
        player_result.game_spread = game_spread
        player_result.game_quarter = game_quarter
        player_result.game_time_left = game_time_left
        player_result.game_date = game_date

        if player_name not in self.player_results:
            self.player_results[player_name] = [ player_result ]
        else:
            self.player_results[player_name].append(player_result)

        # unsued currently:  game_number,team1_tiebreak,team2_tiebreak

    def __load_week_data(self):
        database = Database()
        weeks_and_years = database.load_weeks_and_years(update=True)
        self.weekdata = database.load_week_data(self.year,self.week_number,update=True)  

    def __load_teams(self):
        database = Database()
        self.teams = database.load_teams('teams')
        self.team_keys = self.teams.keys()

    def __get_player_id(self,player_name):
        player_key = self.weekdata.get_player_key(player_name)
        player = self.weekdata.get_player(player_key)
        return player.key().id()

    def __create_player(self,name):
        p = Player(name=name,years=[self.year],parent=root_players())
        player_key = p.put()
        self.__saved_keys.append(player_key)
        return player_key
