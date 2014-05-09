from visual import *
from tests.data.overall_results.pool_not_started import *

class FinalResultsTest(VisualTest):

    def __init__(self):
        self.description = "Final Results Test"
        self.link = "/2013/results"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('Ensure sorting works for each column')
        v.append('Ensure the rank is correct')
        v.append('The page should say "final results"')
        return v

class NotStartedResultsTest(VisualTest):
    def __init__(self):
        self.description = "Pool Not Started Test"
        self.link = "/1980/results"
        self.verify =  self.__verify_instructions()

    def setup(self):
        testdata = PoolNotStarted(leave_objects_in_datastore=True)
        testdata.setup()

    def cleanup(self):
        testdata = PoolNotStarted()
        testdata.cleanup_database()

    def __verify_instructions(self):
        v = []
        v.append('TBD')
        return v
