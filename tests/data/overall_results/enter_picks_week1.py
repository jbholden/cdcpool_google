from overall_results_test_data import *
from models.weeks import *
from models.games import *
from models.root import *
import datetime

class EnterPicksWeek1(OverallResultsTestData):

    def __init__(self,leave_objects_in_datastore=False):
        OverallResultsTestData.__init__(self,year=1982,data_name='EnterPicks',leave_objects_in_datastore=leave_objects_in_datastore)

    def setup_database(self):
        self.setup_players(['Player1','Player2','Player3','Player4','Player5'])
        self.__setup_week1()

    def __setup_week1(self):
        self.games = dict()
        self.setup_not_started_game(self.year,1,1,"Boston College", "Duke","team1",0.5,datetime.datetime(1982,8,1,12,0))
        self.setup_not_started_game(self.year,1,2,"Georgia Tech", "Maryland","team2",0.5,datetime.datetime(1982,8,1,12,0))
        self.setup_not_started_game(self.year,1,3,"Miami-Florida", "NC State","team1",0.5,datetime.datetime(1982,8,1,12,0))
        self.setup_not_started_game(self.year,1,4,"Virginia", "Virginia Tech","team2",0.5,datetime.datetime(1982,8,1,12,0))
        self.setup_not_started_game(self.year,1,5,"Wake Forest", "Oklahoma State","team1",0.5,datetime.datetime(1982,8,1,12,0))
        self.setup_not_started_game(self.year,1,6,"TCU", "Baylor","team2",0.5,datetime.datetime(1982,8,1,12,0))
        self.setup_not_started_game(self.year,1,7,"Iowa State", "Kansas","team1",0.5,datetime.datetime(1982,8,1,12,0))
        self.setup_not_started_game(self.year,1,8,"Kansas State", "Oklahoma","team2",0.5,datetime.datetime(1982,8,1,12,0))
        self.setup_not_started_game(self.year,1,9,"Texas", "Texas Tech","team1",0.5,datetime.datetime(1982,8,1,12,0))
        self.setup_not_started_game(self.year,1,10,"West Virginia", "Cincinnati","team2",0.5,datetime.datetime(1982,8,1,12,0))
        w = Week(year=self.year,number=1,games=[],parent=root_weeks(self,year,1))
        w.lock_picks = self.__get_time_now_plus_1_day()
        self.setup_week(w)

    def __get_time_now_plus_1_day(self):
        return datetime.datetime.now() + datetime.timedelta(days=1)
