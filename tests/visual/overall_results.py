from visual import *
from tests.data.overall_results.pool_not_started import *
from tests.data.overall_results.pool_not_started_with_players import *
from tests.data.overall_results.enter_picks import *
from tests.data.overall_results.enter_picks_week1 import *
from tests.data.overall_results.week_not_started import *
from tests.data.overall_results.week_in_progress import *
from tests.data.overall_results.week_final import *

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

class BadYearResultsTest(VisualTest):

    def __init__(self):
        self.description = "Year Does Not Exist Test"
        self.link = "/1932/results"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('Should see an error message')
        return v

class NotStartedResultsTest(VisualTest):
    def __init__(self):
        self.description = "Pool Not Started Test 1"
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
        v.append('Verify not started message')
        return v

class NotStartedWithPlayersResultsTest(VisualTest):
    def __init__(self):
        self.description = "Pool Not Started Test 2"
        self.link = "/1981/results"
        self.verify =  self.__verify_instructions()

    def setup(self):
        testdata = PoolNotStartedWithPlayers(leave_objects_in_datastore=True)
        testdata.setup()

    def cleanup(self):
        testdata = PoolNotStartedWithPlayers()
        testdata.cleanup_database()

    def __verify_instructions(self):
        v = []
        v.append('Verify not started message')
        v.append('Verify number of players = 5')
        return v

class EnterPicksResultsTest(VisualTest):
    def __init__(self):
        self.description = "Enter Picks Test 1"
        self.link = "/1982/results"
        self.verify =  self.__verify_instructions()

    def setup(self):
        testdata = EnterPicks(leave_objects_in_datastore=True)
        testdata.setup()

    def cleanup(self):
        testdata = EnterPicks()
        testdata.cleanup_database()

    def __verify_instructions(self):
        v = []
        v.append('Verify enter picks message')
        v.append('Verify week 1 has results')
        v.append('Verify week 2 results all 0')
        return v

class EnterPicksWeek1ResultsTest(VisualTest):
    def __init__(self):
        self.description = "Enter Picks Test 2"
        self.link = "/1982/results"
        self.verify =  self.__verify_instructions()

    def setup(self):
        testdata = EnterPicksWeek1(leave_objects_in_datastore=True)
        testdata.setup()

    def cleanup(self):
        testdata = EnterPicksWeek1()
        testdata.cleanup_database()

    def __verify_instructions(self):
        v = []
        v.append('Tests enter picks state for week 1')
        v.append('Verify enter picks message')
        v.append('Verify week 1 results all 0')
        return v

class WeekNotStartedResultsTest(VisualTest):
    def __init__(self):
        self.description = "Week Not Started Test"
        self.link = "/1983/results"
        self.verify =  self.__verify_instructions()

    def setup(self):
        testdata = WeekNotStarted(leave_objects_in_datastore=True)
        testdata.setup()

    def cleanup(self):
        testdata = WeekNotStarted()
        testdata.cleanup_database()

    def __verify_instructions(self):
        v = []
        v.append('Verify week not started message')
        v.append('Verify week 2 results all 0')
        return v

class WeekInProgressResultsTest(VisualTest):
    def __init__(self):
        self.description = "Week In Progress Test"
        self.link = "/1984/results"
        self.verify =  self.__verify_instructions()

    def setup(self):
        testdata = WeekInProgress(leave_objects_in_datastore=True)
        testdata.setup()

    def cleanup(self):
        testdata = WeekInProgress()
        testdata.cleanup_database()

    def __verify_instructions(self):
        v = []
        v.append('Verify week in progress message')
        v.append('Verify overall projected column is present')
        v.append('Verify overall possible column is present')
        v.append('Verify week 2 projected column is present')
        v.append('Verify week 2 possible column is present')
        return v

class WeekFinalResultsTest(VisualTest):
    def __init__(self):
        self.description = "Week Final Test"
        self.link = "/1984/results"
        self.verify =  self.__verify_instructions()

    def setup(self):
        testdata = WeekFinal(leave_objects_in_datastore=True)
        testdata.setup()

    def cleanup(self):
        testdata = WeekFinal()
        testdata.cleanup_database()

    def __verify_instructions(self):
        v = []
        v.append('Verify week final message')
        v.append('Verify week 1 results present')
        v.append('Verify overall possible results present')
        return v
