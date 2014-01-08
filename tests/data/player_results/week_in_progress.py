from player_result_test_data import *
import datetime
from utils.utils import *


class PlayerResultsWeekInProgress(PlayerResultTestData):

    def __init__(self,leave_objects_in_datastore=False):
        PlayerResultTestData.__init__(self,year=1979,week_number=3,data_name='PlayerWeekInProgress',leave_objects_in_datastore=leave_objects_in_datastore)

    def setup_database(self):
        self.setup_players(["Brent"])
        self.__saved_games = dict()
        self.__saved_games[1] = self.__not_started_game(1,'Tulsa','Clemson','team2',8.5,datetime.datetime(1988,5,12,21,41))
        self.__saved_games[2] = self.__not_started_game(2,'Wisconsin','Hampton','team2',18.5,None)
        self.__saved_games[3] = self.__final_game(3,'Arizona State','Alabama A&M','team1',spread=0.5,team1_score=20,team2_score=15)
        self.__saved_games[4] = self.__final_game(4,'New Mexico','Ohio State','team2',spread=14.5,team1_score=12,team2_score=15)
        self.__saved_games[5] = self.__in_progress_game(5,'Alabama','Brown','team2',spread=22.5,team1_score=30,team2_score=10,quarter=None,time_left=None)
        self.__saved_games[6] = self.__in_progress_game(6,'San Diego State','Houston Baptist','team2',spread=4.5,team1_score=21,team2_score=18,quarter="Halftime",time_left=None)
        self.__saved_games[7] = self.__in_progress_game(7,'Sam Houston State','North Texas','team1',spread=20.5,team1_score=41,team2_score=7,quarter="4th",time_left="4:30") 
        self.__saved_games[8] = self.__in_progress_game(8,'San Diego','Baylor','team2',spread=16.5,team1_score=15,team2_score=21,quarter=None,time_left="7:30") 
        self.__saved_games[9] = self.__in_progress_game(9,'Virginia','Florida State','team1',spread=16.5,team1_score=7,team2_score=41,quarter="3rd",time_left="1:51") 
        self.__saved_games[10] = self.__final_game(10,'Kent State','Texas-El Paso','team1',spread=3.5,team1_score=13,team2_score=21) 

        for game_number in self.__saved_games:
            self.setup_game(self.__saved_games[game_number])

        self.setup_week()
        self.__setup_picks()

    def setup_expected_results(self):
        self.__setup_expected_result(1,'')
        self.__setup_expected_result(2,'')
        self.__setup_expected_result(3,'loss') 
        self.__setup_expected_result(4,'loss') 
        self.__setup_expected_result(5,'ahead') 
        self.__setup_expected_result(6,'ahead') 
        self.__setup_expected_result(7,'behind') 
        self.__setup_expected_result(8,'ahead') 
        self.__setup_expected_result(9,'ahead') 
        self.__setup_expected_result(10,'win') 

    def __setup_picks(self):
        self.__saved_picks = dict()
        self.__saved_picks[1] = self.__create_pick('team1',1)
        self.__saved_picks[2] = self.__create_pick('team1',2)
        self.__saved_picks[3] = self.__create_pick('team2',3)
        self.__saved_picks[4] = self.__create_pick('team2',4)
        self.__saved_picks[5] = self.__create_pick('team1',5)
        self.__saved_picks[6] = self.__create_pick('team1',6)
        self.__saved_picks[7] = self.__create_pick('team2',7)
        self.__saved_picks[8] = self.__create_pick('team1',8)
        self.__saved_picks[9] = self.__create_pick('team2',9)
        self.__saved_picks[10] = self.__create_pick('team2',10,team1_score=10,team2_score=15)


    def __not_started_game(self,number,team1,team2,favored,spread,start_date):
        team1_key = self.find_team_key(team1)
        team2_key = self.find_team_key(team2)
        if start_date:
            start_date_utc = get_datetime_in_utc(start_date,'US/Eastern')
        else:
            start_date_utc = None
        game = Game(number=number,team1=team1_key,team2=team2_key,team1_score=None,team2_score=None,favored=favored,spread=spread,state="not_started",quarter=None,time_left=None,date=start_date_utc)
        return game

    def __final_game(self,number,team1,team2,favored,spread,team1_score,team2_score):
        team1_key = self.find_team_key(team1)
        team2_key = self.find_team_key(team2)
        game = Game(number=number,team1=team1_key,team2=team2_key,team1_score=team1_score,team2_score=team2_score,favored=favored,spread=spread,state="final",quarter=None,time_left=None,date=None)
        return game

    def __in_progress_game(self,number,team1,team2,favored,spread,team1_score,team2_score,quarter,time_left):
        team1_key = self.find_team_key(team1)
        team2_key = self.find_team_key(team2)
        game = Game(number=number,team1=team1_key,team2=team2_key,team1_score=team1_score,team2_score=team2_score,favored=favored,spread=spread,state="in_progress",quarter=quarter,time_left=time_left,date=None)
        return game

    def __create_pick(self,winner,game_number,team1_score=None,team2_score=None):
        p = Pick()
        p.winner = winner
        p.team1_score = team1_score
        p.team2_score = team2_score
        self.setup_pick(p,'Brent',game_number)
        return p

    def __setup_expected_result(self,game_number,expected_result):
        game = self.__saved_games[game_number]
        game_pick = self.__saved_picks[game_number]

        team1_name = self.teams[game.team1].name
        team2_name = self.teams[game.team2].name

        if game_pick.winner == "team1":
            player_pick = team1_name
        elif game_pick.winner == "team2":
            player_pick = team2_name

        if game.favored == "team1":
            favored = team1_name
        elif game.favored == "team2":
            favored = team2_name

        if not(game.team1_score) or not(game.team2_score):
            game_spread = None
            winning_team = None
            team1_score = ''
            team2_score = ''
        else:
            game_spread = abs(game.team2_score-game.team1_score)
            if game.team1_score > game.team2_score:
                winning_team = team1_name
            else:
                winning_team = team2_name
            team1_score = game.team1_score
            team2_score = game.team2_score

        # TODO:  consider changing add_result to take a class with the data instead of so many args
        self.add_result(player_name='Brent',player_pick=player_pick,result=expected_result,team1=team1_name,team2=team2_name,
                        team1_score=team1_score,team2_score=team2_score,game_state=game.state,
                        favored=favored,favored_spread=game.spread,winning_team=winning_team,game_spread=game_spread,
                        game_quarter=game.quarter,game_time_left=game.time_left,game_date=game.date,game_number=game_number,
                        team1_tiebreak=game_pick.team1_score,team2_tiebreak=game_pick.team2_score)
