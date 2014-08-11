from tests.data.result_test_data import *
import random  # see tests.test_update
from google.appengine.api import memcache
from models.root import *

class WinnerData(ResultTestData):

    def __init__(self,year,week_number,data_name,leave_objects_in_datastore=False):
        self.year = year
        self.week_number = week_number
        self.set_week_state('not_started')
        self.featured_game_state('not_started')
        self.number_of_leaders(0)
        self.number_of_players(0)
        self.tiebreaker_winner(0)
        ResultTestData.__init__(self,year=year,week_number=week_number,data_name=data_name,leave_objects_in_datastore=leave_objects_in_datastore)

    def set_week_state(self,state):
        self.__week_state = state

    def featured_game_state(self,state):
        self.__featured_state = state

    def number_of_leaders(self,num_leaders):
        self.__num_leaders = num_leaders

    def number_of_players(self,num_players):
        self.__num_players = num_players

    def tiebreaker_winner(self,tiebreak_number):
        self.__tiebreak = tiebreak_number

    def setup_database(self):
        self.__setup_players()
        self.__setup_game_teams()

        if self.__week_state == "not_started":
            self.__setup_week_not_started()

    # defined in result_test_data
    #def cleanup(self):
        #pass

    def __setup_players(self):
        assert self.__num_players >= self.__num_leaders
        player_names = [ "Player %d" % (player_num) for player_num in range(self.__num_players) ]
        self.setup_players(player_names)

    def __setup_week_not_started(self):
        self.setup_game(self.__not_started_game(1))
        self.setup_game(self.__not_started_game(2))
        self.setup_game(self.__not_started_game(3))
        self.setup_game(self.__not_started_game(4))
        self.setup_game(self.__not_started_game(5))
        self.setup_game(self.__not_started_game(6))
        self.setup_game(self.__not_started_game(7))
        self.setup_game(self.__not_started_game(8))
        self.setup_game(self.__not_started_game(9))
        self.setup_game(self.__not_started_game(10))
        self.setup_week()

        # don't care about player picks, just set up some picks for each player with dummy data
        for name in self.players:
            for game_number in range(1,11):
                self.setup_pick(self.__create_pick(),name,game_number)

    def __setup_game_teams(self):
        game_team_names = dict()
        game_team_names[1] = ("Arizona", "Colorado")
        game_team_names[2] = ("Virginia","Virginia Tech")
        game_team_names[3] = ("Iowa","Kansas")                 
        game_team_names[4] = ("Louisiana Monroe","Maryland")               
        game_team_names[5] = ("Michigan", "Mississippi")            
        game_team_names[6] = ("Nevada", "Northwestern")           
        game_team_names[7] = ("Oklahoma State", "Pittsburgh")             
        game_team_names[8] = ("South Alabama", "Southern Miss")          
        game_team_names[9] = ("Temple","Stanford")               
        game_team_names[10] = ("Georgia", "Georgia Tech")

        game_teams = dict()
        for game_number in game_team_names:
            team1,team2 = game_team_names[game_number]
            team1_key = self.team_lookup[team1]
            team2_key = self.team_lookup[team2]
            game_teams[game_number] = (team1_key,team2_key)

        self.game_team_keys = game_teams

    def __not_started_game(self,number):
        team1_key,team2_key = self.game_team_keys[number]
        parent = root_games(self.year,self.week_number)
        game = Game(number=number,team1=team1_key,team2=team2_key,team1_score=None,team2_score=None,favored="team2",spread=0.5,state="not_started",quarter=None,time_left=None,date=None,parent=parent)
        return game

    def __in_progress_game(self,number,favored="team1",spread=0.5,team1_score=19,team2_score=20,quarter="3rd",time_left="7:00"):
        team1_key,team2_key = self.game_team_keys[number]
        parent = root_games(self.year,self.week_number)
        game = Game(number=number,team1=team1_key,team2=team2_key,team1_score=team1_score,team2_score=team2_score,favored=favored,spread=spread,state="in_progress",quarter=quarter,time_left=time_left,date=None,parent=parent)
        return game

    def __final_game(self,number,favored="team1",spread=0.5,team1_score=30,team2_score=29):
        team1_key,team2_key = self.game_team_keys[number]
        parent = root_games(self.year,self.week_number)
        game = Game(number=number,team1=team1_key,team2=team2_key,team1_score=team1_score,team2_score=team2_score,favored=favored,spread=spread,state="final",quarter=None,time_left=None,date=None,parent=parent)
        return game

    def __final_game(self,number,winner,team1,team2):
        team1_key = self.team_lookup(team1)
        team2_key = self.team_lookup(team2)
        favored,spread,team1_score,team2_score = self.__compute_game_winner(winner)
        parent = root_games(self.year,self.week_number)
        game = Game(number=number,team1=team1_key,team2=team2_key,team1_score=team1_score,team2_score=team2_score,favored=favored,spread=spread,state="final",quarter=None,time_left=None,date=None,parent=parent)
        return game

    def __create_pick(self,winner="team1",team1_score=None,team2_score=None):
        p = Pick(parent=root_picks(self.year,self.week_number))
        p.winner = winner
        p.team1_score = team1_score
        p.team2_score = team2_score
        return p
