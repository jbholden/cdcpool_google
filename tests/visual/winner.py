from visual import *
from tests.data.winner.winner_data import *

# class name encoding scheme:
# class <week state>_<featured game state>_<number of leaders>_<tiebreaker number>_Test
#
# <week state> values: 
#   WFO = week final official
#   WFU = week final unofficial
#   WIP = week in progress
#   WNS = week not started
#
# <featured game state> values:
#   <blank> = does not matter for this test
#   FGF = featured game final
#   FGIP = featured game in progress
#   FGNS = featured game not started
#
# <number of leaders> values:
#   L1 = 1 leader in first
#   L2 = 2 leaders tied for first
#   L3 = 3 leaders tied for first
#   etc.
#
# <tiebreaker number> values:
#   <blank> = does not matter for this test
#   TB0 = tiebreaker 0 determines the winner
#   TB1 = tiebreaker 1 determines the winner
#   TB2 = tiebreaker 2 determines the winner
#   TB3 = tiebreaker 3 determines the winner

class WFO_L1_Test(VisualTest):
    def __init__(self):
        self.description = "Week Final, Official, Only 1 Leader"
        self.link = "TBD"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('TBD')
        return v

class WFO_L5_Test(VisualTest):
    def __init__(self):
        self.description = "Week Final, Official, 5 Leaders Tied for First"
        self.link = "TBD"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('TBD')
        return v

class WFU_L1_Test(VisualTest):
    def __init__(self):
        self.description = "Week Final, Unofficial, Only 1 Leader"
        self.link = "TBD"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('TBD')
        return v

class WFU_L5_TB0_Test(VisualTest):
    def __init__(self):
        self.description = "Week Final, Unofficial, 5 Leaders Tied for First, Tiebreak 0 decides"
        self.link = "TBD"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('TBD')
        return v

class WFU_L5_TB1_Test(VisualTest):
    def __init__(self):
        self.description = "Week Final, Unofficial, 5 Leaders Tied for First, Tiebreak 1 decides"
        self.link = "TBD"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('TBD')
        return v

class WFU_L5_TB2_Test(VisualTest):
    def __init__(self):
        self.description = "Week Final, Unofficial, 5 Leaders Tied for First, Tiebreak 2 decides"
        self.link = "TBD"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('TBD')
        return v

class WFU_L5_TB3_Test(VisualTest):
    def __init__(self):
        self.description = "Week Final, Unofficial, 5 Leaders Tied for First, Tiebreak 3 decides"
        self.link = "TBD"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('TBD')
        return v

class WIP_FGF_L1_Test(VisualTest):
    def __init__(self):
        self.description = "Week In Progress, Featured Game Final, Only 1 Leader"
        self.link = "TBD"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('TBD')
        return v

class WIP_FGF_L5_TB0_Test(VisualTest):
    def __init__(self):
        self.description = "Week In Progress, Featured Game Final, 5 Leaders Tied for First, Tiebreak 0 decides"
        self.link = "TBD"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('TBD')
        return v

class WIP_FGF_L5_TB1_Test(VisualTest):
    def __init__(self):
        self.description = "Week In Progress, Featured Game Final, 5 Leaders Tied for First, Tiebreak 1 decides"
        self.link = "TBD"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('TBD')
        return v

class WIP_FGF_L5_TB2_Test(VisualTest):
    def __init__(self):
        self.description = "Week In Progress, Featured Game Final, 5 Leaders Tied for First, Tiebreak 2 decides"
        self.link = "TBD"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('TBD')
        return v

class WIP_FGF_L5_TB3_Test(VisualTest):
    def __init__(self):
        self.description = "Week In Progress, Featured Game Final, 5 Leaders Tied for First, Tiebreak 3 decides"
        self.link = "TBD"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('TBD')
        return v

class WIP_FGIP_L1_Test(VisualTest):
    def __init__(self):
        self.description = "Week In Progress, Featured Game In Progress, Only 1 Leader"
        self.link = "TBD"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('TBD')
        return v

class WIP_FGIP_L5_TB0_Test(VisualTest):
    def __init__(self):
        self.description = "Week In Progress, Featured Game In Progress, 5 Leaders Tied for First, Tiebreak 0 decides"
        self.link = "TBD"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('TBD')
        return v

class WIP_FGIP_L5_TB1_Test(VisualTest):
    def __init__(self):
        self.description = "Week In Progress, Featured Game In Progress, 5 Leaders Tied for First, Tiebreak 1 decides"
        self.link = "TBD"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('TBD')
        return v

class WIP_FGIP_L5_TB2_Test(VisualTest):
    def __init__(self):
        self.description = "Week In Progress, Featured Game In Progress, 5 Leaders Tied for First, Tiebreak 2 decides"
        self.link = "TBD"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('TBD')
        return v

class WIP_FGIP_L5_TB3_Test(VisualTest):
    def __init__(self):
        self.description = "Week In Progress, Featured Game In Progress, 5 Leaders Tied for First, Tiebreak 3 decides"
        self.link = "TBD"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('TBD')
        return v

class WIP_FGNS_L1_Test(VisualTest):
    def __init__(self):
        self.description = "Week In Progress, Featured Game Not Started, Only 1 Leader"
        self.link = "TBD"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('TBD')
        return v

class WIP_FGNS_L5_Test(VisualTest):
    def __init__(self):
        self.description = "Week In Progress, Featured Game Not Started, 5 Leaders Tied for First"
        self.link = "TBD"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('TBD')
        return v

class WNS_Test(VisualTest):
    def __init__(self):
        self.description = "Week Not Started"
        self.link = "/1984/week/1/results"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('Note:  teams from 2013 must be loaded.')
        v.append('No one should be marked as a winner.')
        return v

    def setup(self):
        testdata = WinnerData(1984,1,"wns",leave_objects_in_datastore=True)
        testdata.set_week_state("not_started")
        testdata.number_of_players(10)
        testdata.setup()

    def cleanup(self):
        testdata = WinnerData(1984,1,"wns",leave_objects_in_datastore=True)
        testdata.cleanup_database()
