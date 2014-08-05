from result_test_data import *
from google.appengine.api import memcache
from models.root import *

class WeekInProgressGamesInProgress(ResultTestData):

    def __init__(self,leave_objects_in_datastore=False):
        ResultTestData.__init__(self,year=1978,week_number=7,data_name="WeekInProgressGamesInProgress",leave_objects_in_datastore=leave_objects_in_datastore)

    def setup_database(self):
        player_names = [ "Brent", "Byron", "Alice", "Joan", "Bill", "David", "Amy", "Annie", "Kevin", "John" ]
        winners = ["team1","team1","team1","team2","team2","team2"]
        ahead = ["team1","team2","team1"]
        self.setup_players(player_names)
        self.setup_game(self.__final_game(1,winner=winners[0]))
        self.setup_game(self.__final_game(2,winner=winners[1]))
        self.setup_game(self.__final_game(3,winner=winners[2]))
        self.setup_game(self.__final_game(4,winner=winners[3]))
        self.setup_game(self.__final_game(5,winner=winners[4]))
        self.setup_game(self.__final_game(6,winner=winners[5]))
        self.setup_game(self.__game_in_progress(7,ahead=ahead[0]))
        self.setup_game(self.__game_in_progress(8,ahead=ahead[1]))
        self.setup_game(self.__game_in_progress(9,ahead=ahead[2]))
        self.setup_game(self.__not_started_game(10))
        self.setup_week()
        self.__setup_6_wins_9_projected("Brent",winners,ahead)
        self.__setup_6_wins_8_projected("Byron",winners,ahead)
        self.__setup_5_wins_8_projected("Alice",winners,ahead)
        self.__setup_5_wins_6_projected("Joan",winners,ahead)
        self.__setup_4_wins_7_projected("Bill",winners,ahead)
        self.__setup_4_wins_5_projected("David",winners,ahead)
        self.__setup_3_wins_5_projected("Amy",winners,ahead)
        self.__setup_3_wins_4_projected("Annie",winners,ahead)
        self.__setup_1_win_2_projected("Kevin",winners,ahead)
        self.__setup_missing_picks("John")


    def get_expected_results(self):
        self.add_result(rank=1,projected_rank=1,player_name='Brent',wins=6,losses=0,win_pct=1.000,projected_wins=9,possible_wins=10)
        self.add_result(rank=1,projected_rank=2,player_name='Byron',wins=6,losses=0,win_pct=1.000,projected_wins=8,possible_wins=10)
        self.add_result(rank=3,projected_rank=2,player_name='Alice',wins=5,losses=1,win_pct=0.833,projected_wins=8,possible_wins=9)
        self.add_result(rank=3,projected_rank=5,player_name='Joan',wins=5,losses=1,win_pct=0.833,projected_wins=6,possible_wins=9)
        self.add_result(rank=5,projected_rank=4,player_name='Bill',wins=4,losses=2,win_pct=0.667,projected_wins=7,possible_wins=8)
        self.add_result(rank=5,projected_rank=6,player_name='David',wins=4,losses=2,win_pct=0.667,projected_wins=5,possible_wins=8)
        self.add_result(rank=7,projected_rank=6,player_name='Amy',wins=3,losses=3,win_pct=0.500,projected_wins=5,possible_wins=7)
        self.add_result(rank=7,projected_rank=8,player_name='Annie',wins=3,losses=3,win_pct=0.500,projected_wins=4,possible_wins=7)
        self.add_result(rank=9,projected_rank=9,player_name='Kevin',wins=1,losses=5,win_pct=0.167,projected_wins=2,possible_wins=5)
        self.add_result(rank=10,projected_rank=10,player_name='John',wins=0,losses=10,win_pct=0.000,projected_wins=0,possible_wins=0)
        return self.results

    def __not_started_game(self,number):
        team1_key = self.team_keys[0]
        team2_key = self.team_keys[1]
        parent = root_games(self.year,self.week_number)
        game = Game(number=number,team1=team1_key,team2=team2_key,team1_score=None,team2_score=None,favored="team2",spread=0.5,state="not_started",quarter=None,time_left=None,date=None,parent=parent)
        return game

    def __final_game(self,number,winner):
        team1_key = self.team_keys[0]
        team2_key = self.team_keys[1]
        favored,spread,team1_score,team2_score = self.__compute_game_winner(winner)
        parent = root_games(self.year,self.week_number)
        game = Game(number=number,team1=team1_key,team2=team2_key,team1_score=team1_score,team2_score=team2_score,favored=favored,spread=spread,state="final",quarter=None,time_left=None,date=None,parent=parent)
        return game

    def __game_in_progress(self,number,ahead):
        team1_key = self.team_keys[0]
        team2_key = self.team_keys[1]
        favored,spread,team1_score,team2_score = self.__compute_game_winner(ahead)
        parent = root_games(self.year,self.week_number)
        game = Game(number=number,team1=team1_key,team2=team2_key,team1_score=team1_score,team2_score=team2_score,favored=favored,spread=spread,state="in_progress",quarter="2nd",time_left="7:30",date=None,parent=parent)
        return game


    def __compute_game_winner(self,winner):
        favored = winner
        spread = 0.5
        if winner == 'team1':
            team1_score = 25
            team2_score = 20
        else:
            team1_score = 15
            team2_score = 30
        return favored,spread,team1_score,team2_score

    def __setup_6_wins_9_projected(self,player_name,winners,ahead):
        self.setup_pick(self.__create_winning_pick(winners[0]),player_name,1)
        self.setup_pick(self.__create_winning_pick(winners[1]),player_name,2)
        self.setup_pick(self.__create_winning_pick(winners[2]),player_name,3)
        self.setup_pick(self.__create_winning_pick(winners[3]),player_name,4)
        self.setup_pick(self.__create_winning_pick(winners[4]),player_name,5)
        self.setup_pick(self.__create_winning_pick(winners[5]),player_name,6)
        self.setup_pick(self.__create_winning_pick(ahead[0]),player_name,7)
        self.setup_pick(self.__create_winning_pick(ahead[1]),player_name,8)
        self.setup_pick(self.__create_losing_pick(ahead[2]),player_name,9)
        self.setup_pick(self.__create_pick(),player_name,10)

    def __setup_6_wins_8_projected(self,player_name,winners,ahead):
        self.setup_pick(self.__create_winning_pick(winners[0]),player_name,1)
        self.setup_pick(self.__create_winning_pick(winners[1]),player_name,2)
        self.setup_pick(self.__create_winning_pick(winners[2]),player_name,3)
        self.setup_pick(self.__create_winning_pick(winners[3]),player_name,4)
        self.setup_pick(self.__create_winning_pick(winners[4]),player_name,5)
        self.setup_pick(self.__create_winning_pick(winners[5]),player_name,6)
        self.setup_pick(self.__create_winning_pick(ahead[0]),player_name,7)
        self.setup_pick(self.__create_losing_pick(ahead[1]),player_name,8)
        self.setup_pick(self.__create_losing_pick(ahead[2]),player_name,9)
        self.setup_pick(self.__create_pick(),player_name,10)

    def __setup_5_wins_8_projected(self,player_name,winners,ahead):
        self.setup_pick(self.__create_winning_pick(winners[0]),player_name,1)
        self.setup_pick(self.__create_winning_pick(winners[1]),player_name,2)
        self.setup_pick(self.__create_winning_pick(winners[2]),player_name,3)
        self.setup_pick(self.__create_winning_pick(winners[3]),player_name,4)
        self.setup_pick(self.__create_winning_pick(winners[4]),player_name,5)
        self.setup_pick(self.__create_losing_pick(winners[5]),player_name,6)
        self.setup_pick(self.__create_winning_pick(ahead[0]),player_name,7)
        self.setup_pick(self.__create_winning_pick(ahead[1]),player_name,8)
        self.setup_pick(self.__create_losing_pick(ahead[2]),player_name,9)
        self.setup_pick(self.__create_pick(),player_name,10)

    def __setup_5_wins_6_projected(self,player_name,winners,ahead):
        self.setup_pick(self.__create_winning_pick(winners[0]),player_name,1)
        self.setup_pick(self.__create_winning_pick(winners[1]),player_name,2)
        self.setup_pick(self.__create_winning_pick(winners[2]),player_name,3)
        self.setup_pick(self.__create_winning_pick(winners[3]),player_name,4)
        self.setup_pick(self.__create_winning_pick(winners[4]),player_name,5)
        self.setup_pick(self.__create_losing_pick(winners[5]),player_name,6)
        self.setup_pick(self.__create_losing_pick(ahead[0]),player_name,7)
        self.setup_pick(self.__create_losing_pick(ahead[1]),player_name,8)
        self.setup_pick(self.__create_losing_pick(ahead[2]),player_name,9)
        self.setup_pick(self.__create_pick(),player_name,10)

    def __setup_4_wins_7_projected(self,player_name,winners,ahead):
        self.setup_pick(self.__create_winning_pick(winners[0]),player_name,1)
        self.setup_pick(self.__create_winning_pick(winners[1]),player_name,2)
        self.setup_pick(self.__create_winning_pick(winners[2]),player_name,3)
        self.setup_pick(self.__create_winning_pick(winners[3]),player_name,4)
        self.setup_pick(self.__create_losing_pick(winners[4]),player_name,5)
        self.setup_pick(self.__create_losing_pick(winners[5]),player_name,6)
        self.setup_pick(self.__create_winning_pick(ahead[0]),player_name,7)
        self.setup_pick(self.__create_winning_pick(ahead[1]),player_name,8)
        self.setup_pick(self.__create_losing_pick(ahead[2]),player_name,9)
        self.setup_pick(self.__create_pick(),player_name,10)

    def __setup_4_wins_5_projected(self,player_name,winners,ahead):
        self.setup_pick(self.__create_winning_pick(winners[0]),player_name,1)
        self.setup_pick(self.__create_winning_pick(winners[1]),player_name,2)
        self.setup_pick(self.__create_winning_pick(winners[2]),player_name,3)
        self.setup_pick(self.__create_winning_pick(winners[3]),player_name,4)
        self.setup_pick(self.__create_losing_pick(winners[4]),player_name,5)
        self.setup_pick(self.__create_losing_pick(winners[5]),player_name,6)
        self.setup_pick(self.__create_losing_pick(ahead[0]),player_name,7)
        self.setup_pick(self.__create_losing_pick(ahead[1]),player_name,8)
        self.setup_pick(self.__create_losing_pick(ahead[2]),player_name,9)
        self.setup_pick(self.__create_pick(),player_name,10)

    def __setup_3_wins_5_projected(self,player_name,winners,ahead):
        self.setup_pick(self.__create_winning_pick(winners[0]),player_name,1)
        self.setup_pick(self.__create_winning_pick(winners[1]),player_name,2)
        self.setup_pick(self.__create_winning_pick(winners[2]),player_name,3)
        self.setup_pick(self.__create_losing_pick(winners[3]),player_name,4)
        self.setup_pick(self.__create_losing_pick(winners[4]),player_name,5)
        self.setup_pick(self.__create_losing_pick(winners[5]),player_name,6)
        self.setup_pick(self.__create_winning_pick(ahead[0]),player_name,7)
        self.setup_pick(self.__create_losing_pick(ahead[1]),player_name,8)
        self.setup_pick(self.__create_losing_pick(ahead[2]),player_name,9)
        self.setup_pick(self.__create_pick(),player_name,10)

    def __setup_3_wins_4_projected(self,player_name,winners,ahead):
        self.setup_pick(self.__create_winning_pick(winners[0]),player_name,1)
        self.setup_pick(self.__create_winning_pick(winners[1]),player_name,2)
        self.setup_pick(self.__create_winning_pick(winners[2]),player_name,3)
        self.setup_pick(self.__create_losing_pick(winners[3]),player_name,4)
        self.setup_pick(self.__create_losing_pick(winners[4]),player_name,5)
        self.setup_pick(self.__create_losing_pick(winners[5]),player_name,6)
        self.setup_pick(self.__create_losing_pick(ahead[0]),player_name,7)
        self.setup_pick(self.__create_losing_pick(ahead[1]),player_name,8)
        self.setup_pick(self.__create_losing_pick(ahead[2]),player_name,9)
        self.setup_pick(self.__create_pick(),player_name,10)

    def __setup_1_win_2_projected(self,player_name,winners,ahead):
        self.setup_pick(self.__create_winning_pick(winners[0]),player_name,1)
        self.setup_pick(self.__create_losing_pick(winners[1]),player_name,2)
        self.setup_pick(self.__create_losing_pick(winners[2]),player_name,3)
        self.setup_pick(self.__create_losing_pick(winners[3]),player_name,4)
        self.setup_pick(self.__create_losing_pick(winners[4]),player_name,5)
        self.setup_pick(self.__create_losing_pick(winners[5]),player_name,6)
        self.setup_pick(self.__create_losing_pick(ahead[0]),player_name,7)
        self.setup_pick(self.__create_losing_pick(ahead[1]),player_name,8)
        self.setup_pick(self.__create_losing_pick(ahead[2]),player_name,9)
        self.setup_pick(self.__create_pick(),player_name,10)

    def __create_pick(self):
        p = Pick(parent=root_picks(self.year,self.week_number))
        p.winner = "team1"
        p.team1_score = None
        p.team2_score = None
        return p

    def __create_winning_pick(self,winner):
        p = Pick(parent=root_picks(self.year,self.week_number))
        p.winner = winner
        p.team1_score = None
        p.team2_score = None
        return p

    def __create_losing_pick(self,winner):
        winner_value = "team2" if winner == "team1" else "team1"
        p = Pick(parent=root_picks(self.year,self.week_number))
        p.winner = winner_value
        p.team1_score = None
        p.team2_score = None
        return p

    def __create_missing_pick(self):
        p = Pick(parent=root_picks(self.year,self.week_number))
        p.winner = None
        p.team1_score = None
        p.team2_score = None
        return p

    def __setup_missing_picks(self,player_name):
        for game_number in range(1,11):
            self.setup_pick(self.__create_missing_pick(),player_name,game_number)


