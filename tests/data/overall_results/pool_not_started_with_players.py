from overall_results_test_data import *

class PoolNotStartedWithPlayers(OverallResultsTestData):

    def __init__(self,leave_objects_in_datastore=False):
        OverallResultsTestData.__init__(self,year=1981,data_name='PoolNotStartedWithPlayers',leave_objects_in_datastore=leave_objects_in_datastore)

    def setup_database(self):
        w = Week(year=self.year,number=1,games=[])
        self.setup_week(w)
        self.setup_players(['Player1','Player2','Player3','Player4','Player5'])
