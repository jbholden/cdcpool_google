from visual import *
from tests.data.player_results.week_not_started import *
from tests.data.player_results.week_not_started_defaulter import *
from tests.data.player_results.week_in_progress import *
from utils.utils import *
from code.database import *
import random

class FinalPlayerResultsTest(VisualTest):

    def __init__(self):
        self.description = "Week Final Test"
        self.link = "/2013/week/1/results"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('**IMPORTANT**')
        v.append('you need to navigate to the player results page by clicking the player name')
        return v

class NotStartedPlayerResultsTest(VisualTest):

    def __init__(self):
        self.description = "Week Not Started Test"
        self.link = "/1979/week/1/results"
        self.verify =  self.__verify_instructions()

    def setup(self):
        testdata = PlayerResultsWeekNotStarted(leave_objects_in_datastore=True)
        testdata.setup()

    def cleanup(self):
        testdata = PlayerResultsWeekNotStarted()
        testdata.cleanup_database()

    def __verify_instructions(self):
        v = []
        v.append('**IMPORTANT**')
        v.append('you need to navigate to the player results page by clicking the player name')
        v.append('Game 1 (Tulsa vs. Clemson):  5/12/1988 9:41 PM EDT')
        v.append('Game 2 (Wisconsin vs. Hampton):  7/3/1998 9:36 AM EDT')
        v.append('Game 3 (Arizona State vs. Alabama A&M):  5/19/1988 2:21 AM EDT')
        v.append('Game 4 (New Mexico vs. Ohio State):  12/10/2001 12:06 AM EST')
        v.append('Game 5 (Alabama vs. Brown):  11/13/1978 7:19 PM EST')
        v.append('Game 6 (San Diego State vs. Houston Baptist):  5/16/2011 10:45 PM EDT')
        v.append('Game 8 (Sam Houston State vs. North Texas):  10/18/1999 6:54 AM EDT')
        v.append('Game 9 (San Diego vs. Baylor):  7/24/2012 3:24 PM EDT')
        v.append('Game 9 (Virginia vs. Florida State):  No game start time')
        v.append('Game 10 (Kent State vs. Texas-El Paso):  No game start time')
        return v

class NotStartedPlayerResultsDefaulterTest(VisualTest):

    def __init__(self):
        self.description = "Week Not Started Defaulter Test"
        self.link = "/1979/week/2/results"
        self.verify =  self.__verify_instructions()

    def setup(self):
        testdata = PlayerResultsWeekNotStartedDefaulter(leave_objects_in_datastore=True)
        testdata.setup()

    def cleanup(self):
        testdata = PlayerResultsWeekNotStartedDefaulter()
        testdata.cleanup_database()

    def __verify_instructions(self):
        v = []
        v.append('**IMPORTANT**')
        v.append('you need to navigate to the player results page by clicking the player name')
        v.append('all games should be counted as a loss')
        return v

class InProgressPlayerResultsTest(VisualTest):

    def __init__(self):
        self.description = "Week In Progress Test"
        self.link = "/1979/week/3/results"
        self.verify =  self.__verify_instructions()

    def setup(self):
        testdata = PlayerResultsWeekInProgress(leave_objects_in_datastore=True)
        testdata.setup()

    def cleanup(self):
        testdata = PlayerResultsWeekInProgress()
        testdata.cleanup_database()

    def __verify_instructions(self):
        v = []
        v.append('**IMPORTANT**')
        v.append('you need to navigate to the player results page by clicking the player name')
        return v

class BeforePickDeadlinePlayerResultsTest(VisualTest):

    def __init__(self):
        self.description = "Before the Pick Deadline Test"
        self.link = "/1979/week/1/results"
        self.verify =  self.__verify_instructions()

    def setup(self):
        current_time = get_current_time_in_utc()
        deadline = current_time + datetime.timedelta(days=1) 
        testdata = PlayerResultsWeekNotStarted(leave_objects_in_datastore=True,lock_picks_time=deadline)
        testdata.setup()

    def cleanup(self):
        testdata = PlayerResultsWeekNotStarted()
        testdata.cleanup_database()

    def __verify_instructions(self):
        v = []
        v.append('**IMPORTANT**')
        v.append('you need to navigate to the player results page by clicking the player name')
        v.append('you should see an error message about being before the pick deadline')
        v.append('the pick deadline has been set for 1 day in the future')
        return v

class AfterPickDeadlinePlayerResultsTest(VisualTest):

    def __init__(self):
        self.description = "After the Pick Deadline Test"
        self.link = "/1979/week/1/results"
        self.verify =  self.__verify_instructions()

    def setup(self):
        deadline = get_current_time_in_utc()
        testdata = PlayerResultsWeekNotStarted(leave_objects_in_datastore=True,lock_picks_time=deadline)
        testdata.setup()

    def cleanup(self):
        testdata = PlayerResultsWeekNotStarted()
        testdata.cleanup_database()

    def __verify_instructions(self):
        v = []
        v.append('**IMPORTANT**')
        v.append('you need to navigate to the player results page by clicking the player name')
        v.append('you should see the player results, not an error message')
        return v


class BadYearPlayerResultsTest(VisualTest):

    def __init__(self):
        self.description = "Bad Year Test"
        self.link = "/1900/week/1/player/100/results"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('you should get an error page')
        return v

class BadWeekNumberPlayerResultsTest(VisualTest):

    def __init__(self):
        player_id = self.__get_a_valid_player_id(2013)
        self.description = "Bad Week Number Test"
        self.link = "/2013/week/14/player/%d/results" % (player_id)
        self.verify =  self.__verify_instructions()

    def __get_a_valid_player_id(self,year):
        d = Database()
        players = d.load_players(year)
        player = players.values()[0]
        return player.key().id()

    def __verify_instructions(self):
        v = []
        v.append('you should get an error page')
        return v

class BadPlayerPlayerResultsTest(VisualTest):

    def __init__(self):
        self.description = "Bad Player Number Test"
        self.link = "/2013/week/1/player/%d/results" % (self.__get_invalid_player_id(2013))
        self.verify =  self.__verify_instructions()

    def __get_invalid_player_id(self,year):
        d = Database()
        players = d.load_players(year)
        player_ids = [ player.key().id() for player in players.values() ]
        while True:
            player_id = random.randint(0,len(player_ids)+1)
            if player_id not in player_ids:
                return player_id

    def __verify_instructions(self):
        v = []
        v.append('you should get an error page')
        return v
