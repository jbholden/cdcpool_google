from visual import *
from tests.data.week_in_progress import *
from tests.data.week_in_progress_games_in_progress import *
from tests.data.week_not_started import *
from tests.data.week_not_started_with_defaulters import *

class FinalWeekResultsTest(VisualTest):

    def __init__(self):
        self.description = "Week Final Test"
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
        self.description = "Week In Progress Test"
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

class WeekInProgressGamesInProgressResultsTest(VisualTest):

    def __init__(self):
        self.description = "Week In Progress and Games In Progress Test"
        self.link = "/1978/week/7/results"
        self.verify =  self.__verify_instructions()

    def setup(self):
        testdata = WeekInProgressGamesInProgress(leave_objects_in_datastore=True)
        testdata.setup()

    def cleanup(self):
        testdata = WeekInProgressGamesInProgress()
        testdata.cleanup_database()

    def __verify_instructions(self):
        return []


class NotStartedWeekResultsTest(VisualTest):

    def __init__(self):
        self.description = "Week Not Started Test"
        self.link = "/1978/week/6/results"
        self.verify =  self.__verify_instructions()

    def setup(self):
        testdata = WeekNotStarted(leave_objects_in_datastore=True)
        testdata.setup()

    def cleanup(self):
        testdata = WeekNotStarted()
        testdata.cleanup_database()

    def __verify_instructions(self):
        return []

class NotStartedDefaultersWeekResultsTest(VisualTest):

    def __init__(self):
        self.description = "Week Not Started With Defaulters Test"
        self.link = "/1978/week/5/results"
        self.verify =  self.__verify_instructions()

    def setup(self):
        testdata = WeekNotStartedWithDefaulters(leave_objects_in_datastore=True)
        testdata.setup()

    def cleanup(self):
        testdata = WeekNotStartedWithDefaulters()
        testdata.cleanup_database()

    def __verify_instructions(self):
        return []
