from visual import *
from tests.data.player_results.week_not_started import *

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
