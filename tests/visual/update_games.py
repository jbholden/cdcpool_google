from visual import *
from code.api import *
import datetime
from tests.data.week_in_progress_games_in_progress import *
from tests.data.week_not_started import *

class ScoresLockedTest(VisualTest):

    def __init__(self):
        self.description = "Scores Locked Test"
        self.link = "/2013/week/1/games"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('Verify scores locked message appears')
        v.append('Verify there is no submit button')
        return v

    def setup(self):
        api = API()
        week = api.get_week_in_year(2013,1) 
        week_key = week.key()
        lock_time = datetime.datetime(2010,2,24,19,30)
        data = { 'lock_scores': lock_time }
        api.edit_week_by_key(week_key,data)

        d = Database()
        d.update_week_cache(2013,1)

    def cleanup(self):
        api = API()
        week = api.get_week_in_year(2013,1) 
        week_key = week.key()
        data = { 'lock_scores': None }
        api.edit_week_by_key(week_key,data)

        d = Database()
        d.update_week_cache(2013,1)

class GamesFinalTest(VisualTest):

    def __init__(self):
        self.description = "Week Games Final Test"
        self.link = "/2013/week/1/games"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('All final checkboxes should be checked.')
        return v

class GamesNotStartedTest(VisualTest):

    def __init__(self):
        self.description = "No Games Started Test"
        self.link = "/1978/week/6/games"
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

class GamesInProgressTest(VisualTest):

    def __init__(self):
        self.description = "Games In Progress Test"
        self.link = "/1978/week/7/games"
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

