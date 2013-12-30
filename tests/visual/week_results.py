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
        v.append('Ensure the rank is correct')
        v.append('The page should say "final results"')
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
        v.append('There should be a projected and possible wins columns')
        v.append('Ensure sorting works for each column')
        v.append('The projected and possible wins should be the same since no games are in progress')
        v.append('The rank should be the same for each sort by column')
        v.append('The page should say "in progress"')
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
        v = []
        v.append('There should be a projected and possible wins columns')
        v.append('Ensure sorting works for each column')
        v.append('Verify the rank changes to projected rank when sorting by projected column')
        v.append('The page should say "in progress"')
        return v


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
        v = []
        v.append('There should be a possible wins column')
        v.append('Ensure sorting works for each column')
        v.append('Everyone should be tied for 1st place')
        v.append('The page should say "not started"')
        return v

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
        v = []
        v.append('There should be a possible wins column')
        v.append('Ensure sorting works for each column')
        v.append('The people in last place (defaulters) should be 0-10 and ranked lower')
        return v
