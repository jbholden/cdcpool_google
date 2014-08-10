from visual import *

# class name encoding scheme:
# class <week state>_<featured game state>_<number of leaders>_<tiebreaker number>_Test
#
# <week state> values: 
#   WFO = week final official, WFU = week final unofficial
#   WIP = week in progress, WNS = week not started
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
        self.description = "Week Final, Official, Only 1 Leader"

class WFO_L5_Test(VisualTest):
        self.description = "Week Final, Official, 5 Leaders Tied for First"

class WFU_L1_Test(VisualTest):
        self.description = "Week Final, Unofficial, Only 1 Leader"

class WFU_L5_TB0_Test(VisualTest):
        self.description = "Week Final, Official, 5 Leaders Tied for First, Tiebreak 0 decides"

class WFU_L5_TB1_Test(VisualTest):
        self.description = "Week Final, Official, 5 Leaders Tied for First, Tiebreak 1 decides"

class WFU_L5_TB2_Test(VisualTest):
        self.description = "Week Final, Official, 5 Leaders Tied for First, Tiebreak 2 decides"

class WFU_L5_TB3_Test(VisualTest):
        self.description = "Week Final, Official, 5 Leaders Tied for First, Tiebreak 3 decides"
