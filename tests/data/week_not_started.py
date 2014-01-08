from result_test_data import *
from google.appengine.api import memcache

class WeekNotStarted(ResultTestData):

    def __init__(self,leave_objects_in_datastore=False):
        ResultTestData.__init__(self,year=1978,week_number=6,data_name='WeekNotStarted',leave_objects_in_datastore=leave_objects_in_datastore)

    def setup_database(self):
        player_names = [ "Brent", "Byron", "Alice", "Joan", "Bill", "David", "Amy", "Annie", "Kevin", "John" ]
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

        for name in player_names:
            self.__setup_player_picks(name)

    def get_expected_results(self):
        self.add_result(rank=1,projected_rank=1,player_name='Brent',wins=0,losses=0,win_pct=0.000,projected_wins=10,possible_wins=10)
        self.add_result(rank=1,projected_rank=1,player_name='Byron',wins=0,losses=0,win_pct=0.000,projected_wins=10,possible_wins=10)
        self.add_result(rank=1,projected_rank=1,player_name='Alice',wins=0,losses=0,win_pct=0.000,projected_wins=10,possible_wins=10)
        self.add_result(rank=1,projected_rank=1,player_name='Joan',wins=0,losses=0,win_pct=0.000,projected_wins=10,possible_wins=10)
        self.add_result(rank=1,projected_rank=1,player_name='Bill',wins=0,losses=0,win_pct=0.000,projected_wins=10,possible_wins=10)
        self.add_result(rank=1,projected_rank=1,player_name='David',wins=0,losses=0,win_pct=0.000,projected_wins=10,possible_wins=10)
        self.add_result(rank=1,projected_rank=1,player_name='Amy',wins=0,losses=0,win_pct=0.000,projected_wins=10,possible_wins=10)
        self.add_result(rank=1,projected_rank=1,player_name='Annie',wins=0,losses=0,win_pct=0.000,projected_wins=10,possible_wins=10)
        self.add_result(rank=1,projected_rank=1,player_name='Kevin',wins=0,losses=0,win_pct=0.000,projected_wins=10,possible_wins=10)
        self.add_result(rank=1,projected_rank=1,player_name='John',wins=0,losses=0,win_pct=0.000,projected_wins=10,possible_wins=10)
        return self.results

    def get_expected_player_results(self,player_name):
        player_names = [ "Brent", "Byron", "Alice", "Joan", "Bill", "David", "Amy", "Annie", "Kevin", "John" ]
        self.add_player_result()
        pass


    def __not_started_game(self,number):
        team1_key = self.team_keys[0]
        team2_key = self.team_keys[1]
        game = Game(number=number,team1=team1_key,team2=team2_key,team1_score=None,team2_score=None,favored="team2",spread=0.5,state="not_started",quarter=None,time_left=None,date=None)
        return game

    def __setup_player_picks(self,player_name):
        for game_number in range(1,11):
            self.setup_pick(self.__create_pick(),player_name,game_number)

    def __create_pick(self):
        p = Pick()
        p.winner = "team1"
        p.team1_score = None
        p.team2_score = None
        return p
