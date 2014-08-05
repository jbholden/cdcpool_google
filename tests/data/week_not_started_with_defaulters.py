from result_test_data import *
from models.root import *

class WeekNotStartedWithDefaulters(ResultTestData):

    def __init__(self,leave_objects_in_datastore=False):
        ResultTestData.__init__(self,year=1978,week_number=5,data_name='WeekNotStartedWithDefaulters',leave_objects_in_datastore=leave_objects_in_datastore)

    def setup_database(self):
        players_with_picks = [ "Brent", "Byron", "Alice", "Joan", "Bill", "David", "Amy", "Annie" ]
        players_missing_picks = [ "Kevin","John" ]
        player_names = players_with_picks + players_missing_picks

        self.setup_players(player_names)
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

        for name in players_with_picks:
            self.__setup_player_picks(name)

        for name in players_missing_picks:
            self.__setup_player_missing_picks(name)

    def get_expected_results(self):
        self.add_result(rank=1,projected_rank=1,player_name='Brent',wins=0,losses=0,win_pct=0.000,projected_wins=10,possible_wins=10)
        self.add_result(rank=1,projected_rank=1,player_name='Byron',wins=0,losses=0,win_pct=0.000,projected_wins=10,possible_wins=10)
        self.add_result(rank=1,projected_rank=1,player_name='Alice',wins=0,losses=0,win_pct=0.000,projected_wins=10,possible_wins=10)
        self.add_result(rank=1,projected_rank=1,player_name='Joan',wins=0,losses=0,win_pct=0.000,projected_wins=10,possible_wins=10)
        self.add_result(rank=1,projected_rank=1,player_name='Bill',wins=0,losses=0,win_pct=0.000,projected_wins=10,possible_wins=10)
        self.add_result(rank=1,projected_rank=1,player_name='David',wins=0,losses=0,win_pct=0.000,projected_wins=10,possible_wins=10)
        self.add_result(rank=1,projected_rank=1,player_name='Amy',wins=0,losses=0,win_pct=0.000,projected_wins=10,possible_wins=10)
        self.add_result(rank=1,projected_rank=1,player_name='Annie',wins=0,losses=0,win_pct=0.000,projected_wins=10,possible_wins=10)
        self.add_result(rank=9,projected_rank=9,player_name='Kevin',wins=0,losses=10,win_pct=0.000,projected_wins=0,possible_wins=0)
        self.add_result(rank=9,projected_rank=9,player_name='John',wins=0,losses=10,win_pct=0.000,projected_wins=0,possible_wins=0)
        return self.results


    def __not_started_game(self,number):
        team1_key = self.team_keys[0]
        team2_key = self.team_keys[1]
        parent = root_games(self.year,self.week_number)
        game = Game(number=number,team1=team1_key,team2=team2_key,team1_score=None,team2_score=None,favored="team2",spread=0.5,state="not_started",quarter=None,time_left=None,date=None,parent=parent)
        return game

    def __setup_player_picks(self,player_name):
        for game_number in range(1,11):
            self.setup_pick(self.__create_pick(),player_name,game_number)

    def __setup_player_missing_picks(self,player_name):
        for game_number in range(1,11):
            self.setup_pick(self.__create_missing_pick(),player_name,game_number)

    def __create_pick(self):
        p = Pick(parent=root_picks(self.year,self.week_number))
        p.winner = "team1"
        p.team1_score = None
        p.team2_score = None
        return p

    def __create_missing_pick(self):
        p = Pick(parent=root_picks(self.year,self.week_number))
        p.winner = None
        p.team1_score = None
        p.team2_score = None
        return p
