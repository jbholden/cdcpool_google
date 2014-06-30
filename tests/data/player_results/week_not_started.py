from player_result_test_data import *
import datetime
from utils.utils import *

class PlayerResultsWeekNotStarted(PlayerResultTestData):

    def __init__(self,leave_objects_in_datastore=False,lock_picks_time=None):
        PlayerResultTestData.__init__(self,year=1979,week_number=1,data_name='PlayerWeekNotStarted',leave_objects_in_datastore=leave_objects_in_datastore)
        self.__lock_picks_time = lock_picks_time

    def setup_database(self):
        self.setup_players(["Brent"])
        self.__saved_games = dict()
        self.__saved_games[1] = self.__not_started_game(1,'Tulsa','Clemson','team2',8.5,datetime.datetime(1988,5,12,21,41))
        self.__saved_games[2] = self.__not_started_game(2,'Wisconsin','Ball State','team2',18.5,datetime.datetime(1998,7,3,9,36))
        self.__saved_games[3] = self.__not_started_game(3,'Arizona State','Texas A&M','team1',0.5,datetime.datetime(1988,5,19,2,21))
        self.__saved_games[4] = self.__not_started_game(4,'New Mexico','Ohio State','team2',14.5,datetime.datetime(2001,12,10,0,6))
        self.__saved_games[5] = self.__not_started_game(5,'Alabama','UCF','team2',22.5,datetime.datetime(1978,11,13,19,19))
        self.__saved_games[6] = self.__not_started_game(6,'San Diego State','South Carolina','team2',4.5,datetime.datetime(2011,5,16,22,45))
        self.__saved_games[7] = self.__not_started_game(7,'Temple','North Texas','team2',20.5,datetime.datetime(1999,10,18,6,54))
        self.__saved_games[8] = self.__not_started_game(8,'Syracuse','Baylor','team2',16.5,datetime.datetime(2012,7,24,15,24))
        self.__saved_games[9] = self.__not_started_game(9,'Virginia','Florida State','team1',16.5,None)
        self.__saved_games[10] = self.__not_started_game(10,'Kent State','Texas-El Paso','team1',3.5,None)

        for game_number in self.__saved_games:
            self.setup_game(self.__saved_games[game_number])

        self.setup_week(lock_picks=self.__lock_picks_time)
        self.__setup_picks()

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

    def setup_expected_results(self):
        for game_number in range(1,11):
            self.__setup_expected_result(game_number)

    def __setup_expected_result(self,game_number):
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
        else:
            game_spread = abs(game.team2_score-game.team1_score)
            if game.team1_score > game.team2_score:
                winning_team = team1_name
            else:
                winning_team = team2_name

        # TODO:  consider changing add_result to take a class with the data instead of so many args
        self.add_result(player_name='Brent',player_pick=player_pick,result='',team1=team1_name,team2=team2_name,
                        team1_score='',team2_score='',game_state='not_started',
                        favored=favored,favored_spread=game.spread,winning_team=winning_team,game_spread=game_spread,
                        game_quarter=None,game_time_left=None,game_date=game.date,game_number=game_number,
                        team1_tiebreak=game_pick.team1_score,team2_tiebreak=game_pick.team2_score)

    def __not_started_game(self,number,team1,team2,favored,spread,start_date):
        team1_key = self.find_team_key(team1)
        team2_key = self.find_team_key(team2)
        if start_date:
            start_date_utc = get_datetime_in_utc(start_date,'US/Eastern')
        else:
            start_date_utc = None
        game = Game(number=number,team1=team1_key,team2=team2_key,team1_score=None,team2_score=None,favored=favored,spread=spread,state="not_started",quarter=None,time_left=None,date=start_date_utc)
        return game

    def __create_pick(self,winner,game_number,team1_score=None,team2_score=None):
        p = Pick()
        p.winner = winner
        p.team1_score = team1_score
        p.team2_score = team2_score
        self.setup_pick(p,'Brent',game_number)
        return p
