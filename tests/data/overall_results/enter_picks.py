from overall_results_test_data import *
from models.weeks import *
from models.games import *
import datetime

class EnterPicks(OverallResultsTestData):

    def __init__(self,leave_objects_in_datastore=False):
        OverallResultsTestData.__init__(self,year=1982,data_name='EnterPicks',leave_objects_in_datastore=leave_objects_in_datastore)

    def setup_database(self):
        self.setup_players(['Player1','Player2','Player3','Player4','Player5'])
        self.__setup_week1()
        self.__setup_week1_picks()
        self.__setup_week2()

    def __setup_week1(self):
        self.setup_final_game(self.year,1,1,"Fresno State","Lehigh","team1",0.5,20,15)
        self.setup_final_game(self.year,1,2,"Maine","Oklahoma","team2",1.5,31,15)
        self.setup_final_game(self.year,1,3,"Alcorn State","Illinois State","team1",2.5,32,15)
        self.setup_final_game(self.year,1,4,"North Texas","Southern Cal","team2",3.5,33,15)
        self.setup_final_game(self.year,1,5,"Elon","Dartmouth","team1",4.5,34,15)
        self.setup_final_game(self.year,1,6,"Northern Arizona","Illinois","team2",5.5,35,15)
        self.setup_final_game(self.year,1,7,"Syracuse","Mercer","team1",6.5,26,15)
        self.setup_final_game(self.year,1,8,"Wagner","Memphis","team2",7.5,37,15)
        self.setup_final_game(self.year,1,9,"Ball State","Troy","team1",8.5,18,15)
        self.setup_final_game(self.year,1,10,"California","Army","team2",9.5,10,15)
        w = Week(year=self.year,number=1,games=[])
        self.setup_week(w)

    def __setup_week2(self):
        self.games = dict()
        self.setup_not_started_game(self,year,2,1,"Boston College", "Duke","team1",0.5,datetime.datetime(1982,8,1,12,0))
        self.setup_not_started_game(self,year,2,2,"Georgia Tech", "Maryland","team2",0.5,datetime.datetime(1982,8,1,12,0))
        self.setup_not_started_game(self,year,2,3,"Miami-Florida", "NC State","team1",0.5,datetime.datetime(1982,8,1,12,0))
        self.setup_not_started_game(self,year,2,4,"Virginia", "Virginia Tech","team2",0.5,datetime.datetime(1982,8,1,12,0))
        self.setup_not_started_game(self,year,2,5,"Wake Forest", "Oklahoma State","team1",0.5,datetime.datetime(1982,8,1,12,0))
        self.setup_not_started_game(self,year,2,6,"TCU", "Baylor","team2",0.5,datetime.datetime(1982,8,1,12,0))
        self.setup_not_started_game(self,year,2,7,"Iowa State", "Kansas","team1",0.5,datetime.datetime(1982,8,1,12,0))
        self.setup_not_started_game(self,year,2,8,"Kansas State", "Oklahoma","team2",0.5,datetime.datetime(1982,8,1,12,0))
        self.setup_not_started_game(self,year,2,9,"Texas", "Texas Tech","team1",0.5,datetime.datetime(1982,8,1,12,0))
        self.setup_not_started_game(self,year,2,10,"West Virginia", "Cincinnati","team2",0.5,datetime.datetime(1982,8,1,12,0))
        w = Week(year=self.year,number=2,games=[])
        w.lock_picks = self.__get_time_now_plus_1_day()
        self.setup_week(w)

    def __setup_week1_picks(self):
        self.setup_pick(self.year,1,"Player1",1,1,"team1")
        self.setup_pick(self.year,1,"Player1",1,2,"team2")
        self.setup_pick(self.year,1,"Player1",1,3,"team1")
        self.setup_pick(self.year,1,"Player1",1,4,"team2")
        self.setup_pick(self.year,1,"Player1",1,5,"team1")
        self.setup_pick(self.year,1,"Player1",1,6,"team2")
        self.setup_pick(self.year,1,"Player1",1,7,"team1")
        self.setup_pick(self,year,1,"Player1",1,8,"team2")
        self.setup_pick(self,year,1,"Player1",1,9,"team1")
        self.setup_pick(self,year,1,"Player1",1,10,"team2",20,10)
        self.setup_pick(self,year,1,"Player2",1,1,"team1")
        self.setup_pick(self,year,1,"Player2",1,2,"team1")
        self.setup_pick(self,year,1,"Player2",1,3,"team2")
        self.setup_pick(self,year,1,"Player2",1,4,"team1")
        self.setup_pick(self,year,1,"Player2",1,5,"team1")
        self.setup_pick(self,year,1,"Player2",1,6,"team2")
        self.setup_pick(self,year,1,"Player2",1,7,"team1")
        self.setup_pick(self,year,1,"Player2",1,8,"team1")
        self.setup_pick(self,year,1,"Player2",1,9,"team2")
        self.setup_pick(self,year,1,"Player2",1,10,"team1",20,10)
        self.setup_pick(self,year,1,"Player3",1,1,"team1")
        self.setup_pick(self,year,1,"Player3",1,2,"team2")
        self.setup_pick(self,year,1,"Player3",1,3,"team1")
        self.setup_pick(self,year,1,"Player3",1,4,"team1")
        self.setup_pick(self,year,1,"Player3",1,5,"team1")
        self.setup_pick(self,year,1,"Player3",1,6,"team2")
        self.setup_pick(self,year,1,"Player3",1,7,"team1")
        self.setup_pick(self,year,1,"Player3",1,8,"team1")
        self.setup_pick(self,year,1,"Player3",1,9,"team1")
        self.setup_pick(self,year,1,"Player3",1,10,"team2",20,10)
        self.setup_pick(self,year,1,"Player4",1,1,"team1")
        self.setup_pick(self,year,1,"Player4",1,2,"team1")
        self.setup_pick(self,year,1,"Player4",1,3,"team1")
        self.setup_pick(self,year,1,"Player4",1,4,"team2")
        self.setup_pick(self,year,1,"Player4",1,5,"team1")
        self.setup_pick(self,year,1,"Player4",1,6,"team1")
        self.setup_pick(self,year,1,"Player4",1,7,"team1")
        self.setup_pick(self,year,1,"Player4",1,8,"team2")
        self.setup_pick(self,year,1,"Player4",1,9,"team1")
        self.setup_pick(self,year,1,"Player4",1,10,"team1",20,10)
        self.setup_pick(self,year,1,"Player5",1,1,"team2")
        self.setup_pick(self,year,1,"Player5",1,2,"team1")
        self.setup_pick(self,year,1,"Player5",1,3,"team2")
        self.setup_pick(self,year,1,"Player5",1,4,"team1")
        self.setup_pick(self,year,1,"Player5",1,5,"team1")
        self.setup_pick(self,year,1,"Player5",1,6,"team2")
        self.setup_pick(self,year,1,"Player5",1,7,"team1")
        self.setup_pick(self,year,1,"Player5",1,8,"team2")
        self.setup_pick(self,year,1,"Player5",1,9,"team1")
        self.setup_pick(self,year,1,"Player5",1,10,"team2",20,10)
        self.setup_picks_done(self.year,1)

    def __get_time_now_plus_1_day(self):
        return datetime.datetime.now() + datetime.timedelta(days=1)
