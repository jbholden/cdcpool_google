from overall_results_test_data import *
from models.root import *

class PoolNotStarted(OverallResultsTestData):

    def __init__(self,leave_objects_in_datastore=False):
        OverallResultsTestData.__init__(self,year=1980,data_name='PoolNotStarted',leave_objects_in_datastore=leave_objects_in_datastore)

    def setup_database(self):
        w = Week(year=self.year,number=1,games=[],parent=root_weeks(self.year,1))
        self.setup_week(w)
