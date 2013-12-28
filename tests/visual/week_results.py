from visual import *
from tests.data.week_in_progress import *

class FinalWeekResultsTest(VisualTest):

    def __init__(self):
        self.description = "Week Results Final Test"
        self.link = "/2013/week/6/results"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('Ensure sorting works for each column')
        v.append('When sorting by projected wins ensure the rank changes to the projected rank')
        v.append('When sorting by possible wins ensure the rank changes to the possible rank')
        v.append('All other sorts should have rank by wins')
        return v


class WeekInProgressResultsTest(VisualTest):

    def __init__(self):
        self.description = "Week Results In Progress Test"
        self.link = "/1978/week/8/results"
        self.verify =  self.__verify_instructions()

    def setup(self):
        testdata = WeekInProgress(leave_objects_in_datastore=True)
        testdata.setup()

    def cleanup(self):
        testdata = WeekInProgress()
        testdata.cleanup_database()

    def __verify_instructions(self):
        v = []
        v.append('Ensure sorting works for each column')
        v.append('When sorting by projected wins ensure the rank changes to the projected rank')
        v.append('When sorting by possible wins ensure the rank changes to the possible rank')
        v.append('All other sorts should have rank by wins')
        return v

