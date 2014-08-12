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
#   TB3I = tiebreaker 3 determines the winner but not enough data to determine winner (indeterminate)

class WFO_L1_Test(VisualTest):
    def __init__(self):
        self.description = "Week Final, Official, Only 1 Leader"
        self.link = "/1984/week/2/results"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('Note:  teams from 2013 needs to be loaded')
        v.append('There should be only 1 leader')
        return v

    def setup(self):
        testdata = WinnerData(1984,2,"wfo_l1",leave_objects_in_datastore=True)
        testdata.set_week_state("final")
        testdata.number_of_players(10)
        testdata.number_of_leaders(1)
        testdata.week_official()
        testdata.featured_game_state("final")
        testdata.setup()

    def cleanup(self):
        testdata = WinnerData(1984,2,"wfo_l1",leave_objects_in_datastore=True)
        testdata.cleanup_database()

class WFO_L5_Test(VisualTest):
    def __init__(self):
        self.description = "Week Final, Official, 5 Leaders Tied for First"
        self.link = "/1984/week/3/results"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('Note:  teams from 2013 needs to be loaded')
        v.append('There should be only 5 people tied for the lead')
        v.append('One winner should be identified from the tied leaders')
        v.append('WINNER should be a hyperlink to the tiebreak page')
        v.append('The WINNER should have a rank of 1, while others tied for lead have a rank of 2')
        return v

    def setup(self):
        testdata = WinnerData(1984,3,"wfo_l5",leave_objects_in_datastore=True)
        testdata.set_week_state("final")
        testdata.number_of_players(10)
        testdata.number_of_leaders(5)
        testdata.week_official()
        testdata.featured_game_state("final")
        testdata.setup()

    def cleanup(self):
        testdata = WinnerData(1984,3,"wfo_l5",leave_objects_in_datastore=True)
        testdata.cleanup_database()

class WFU_L1_Test(VisualTest):
    def __init__(self):
        self.description = "Week Final, Unofficial, Only 1 Leader"
        self.link = "/1984/week/4/results"
        self.verify = self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('Note:  teams from 2013 needs to be loaded')
        v.append('There should be only 1 leader')
        return v

    def setup(self):
        testdata = WinnerData(1984,4,"wfu_l1",leave_objects_in_datastore=True)
        testdata.set_week_state("final")
        testdata.number_of_players(10)
        testdata.number_of_leaders(1)
        testdata.week_unofficial()
        testdata.featured_game_state("final")
        testdata.setup()

    def cleanup(self):
        testdata = WinnerData(1984,4,"wfu_l1",leave_objects_in_datastore=True)
        testdata.cleanup_database()

class WFU_L5_TB0_Test(VisualTest):
    def __init__(self):
        self.description = "Week Final, Unofficial, 5 Leaders Tied for First, Tiebreak 0 decides"
        self.link = "/1984/week/5/results"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('Note:  teams from 2013 needs to be loaded')
        v.append('There should be only 5 leaders tied for first.')
        v.append('One leader should be the unofficial winner.')
        v.append('The winner should win because of tiebreak 0')
        v.append('The unofficial winner should be listed first')
        return v

    def setup(self):
        testdata = WinnerData(1984,5,"wfu_l5_tb0",leave_objects_in_datastore=True)
        testdata.set_week_state("final")
        testdata.number_of_players(10)
        testdata.number_of_leaders(5)
        testdata.week_unofficial()
        testdata.tiebreaker_winner(0)
        testdata.featured_game_state("final")
        testdata.setup()

    def cleanup(self):
        testdata = WinnerData(1984,5,"wfu_l5_tb0",leave_objects_in_datastore=True)
        testdata.cleanup_database()

class WFU_L5_TB1_Test(VisualTest):
    def __init__(self):
        self.description = "Week Final, Unofficial, 5 Leaders Tied for First, Tiebreak 1 decides"
        self.link = "/1984/week/6/results"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('Note:  teams from 2013 needs to be loaded')
        v.append('There should be only 5 leaders tied for first.')
        v.append('One leader should be the unofficial winner.')
        v.append('The winner should win because of tiebreak 1')
        v.append('The unofficial winner should be listed first')
        return v

    def setup(self):
        testdata = WinnerData(1984,6,"wfu_l5_tb1",leave_objects_in_datastore=True)
        testdata.set_week_state("final")
        testdata.number_of_players(10)
        testdata.number_of_leaders(5)
        testdata.week_unofficial()
        testdata.tiebreaker_winner(1)
        testdata.featured_game_state("final")
        testdata.setup()

    def cleanup(self):
        testdata = WinnerData(1984,6,"wfu_l5_tb1",leave_objects_in_datastore=True)
        testdata.cleanup_database()

class WFU_L5_TB2_Test(VisualTest):
    def __init__(self):
        self.description = "Week Final, Unofficial, 5 Leaders Tied for First, Tiebreak 2 decides"
        self.link = "/1984/week/7/results"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('Note:  teams from 2013 needs to be loaded')
        v.append('There should be only 5 leaders tied for first.')
        v.append('One leader should be the unofficial winner.')
        v.append('The winner should win because of tiebreak 2')
        v.append('The unofficial winner should be listed first')
        return v

    def setup(self):
        testdata = WinnerData(1984,7,"wfu_l5_tb2",leave_objects_in_datastore=True)
        testdata.set_week_state("final")
        testdata.number_of_players(10)
        testdata.number_of_leaders(5)
        testdata.week_unofficial()
        testdata.tiebreaker_winner(2)
        testdata.featured_game_state("final")
        testdata.setup()

    def cleanup(self):
        testdata = WinnerData(1984,7,"wfu_l5_tb2",leave_objects_in_datastore=True)
        testdata.cleanup_database()

class WFU_L5_TB3_Test(VisualTest):
    def __init__(self):
        self.description = "Week Final, Unofficial, 5 Leaders Tied for First, Tiebreak 3 decides"
        self.link = "/1984/week/8/results"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('Note:  teams from 2013 needs to be loaded')
        v.append('There should be only 5 leaders tied for first.')
        v.append('One leader should be the unofficial winner.')
        v.append('The winner should win because of tiebreak 3')
        v.append('The unofficial winner should be listed first')
        return v

    def setup(self):
        testdata = WinnerData(1984,8,"wfu_l5_tb3",leave_objects_in_datastore=True)
        testdata.set_week_state("final")
        testdata.number_of_players(10)
        testdata.number_of_leaders(5)
        testdata.week_unofficial()
        testdata.tiebreaker_winner(3)
        testdata.make_tiebreak3_valid()
        testdata.featured_game_state("final")
        testdata.setup()

    def cleanup(self):
        testdata = WinnerData(1984,8,"wfu_l5_tb3",leave_objects_in_datastore=True)
        testdata.cleanup_database()

class WFU_L5_TB3I_Test(VisualTest):
    def __init__(self):
        self.description = "Week Final, Unofficial, 5 Leaders Tied for First, Tiebreak 3 decides but indeterminate"
        self.link = "/1984/week/9/results"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('Note:  teams from 2013 needs to be loaded')
        v.append('There should be only 5 leaders tied for first.')
        v.append('Multiple winners are possible')
        v.append('Should be unable to determine winner using tiebreak 3')
        return v

    def setup(self):
        testdata = WinnerData(1984,9,"wfu_l5_tb3i",leave_objects_in_datastore=True)
        testdata.set_week_state("final")
        testdata.number_of_players(10)
        testdata.number_of_leaders(5)
        testdata.week_unofficial()
        testdata.tiebreaker_winner(3)
        testdata.make_tiebreak3_indeterminate()
        testdata.featured_game_state("final")
        testdata.setup()

    def cleanup(self):
        testdata = WinnerData(1984,8,"wfu_l5_tb3i",leave_objects_in_datastore=True)
        testdata.cleanup_database()


class WIP_FGF_L1_Test(VisualTest):
    def __init__(self):
        self.description = "Week In Progress, Featured Game Final, Only 1 Leader"
        self.link = "/1985/week/1/results"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('Note:  teams from 2013 needs to be loaded')
        v.append('There should be 1 leader in first place')
        v.append('The leader should be labeled as the PROJECTED WINNER')
        return v

    def setup(self):
        testdata = WinnerData(1985,1,"wip_fgf_l1",leave_objects_in_datastore=True)
        testdata.set_week_state("in_progress")
        testdata.number_of_players(10)
        testdata.number_of_leaders(1)
        testdata.week_unofficial()
        testdata.featured_game_state("final")
        testdata.setup()

    def cleanup(self):
        testdata = WinnerData(1985,1,"wip_fgf_l1",leave_objects_in_datastore=True)
        testdata.cleanup_database()

class WIP_FGF_L5_TB0_Test(VisualTest):
    def __init__(self):
        self.description = "Week In Progress, Featured Game Final, 5 Leaders Tied for First, Tiebreak 0 decides"
        self.link = "/1985/week/2/results"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('Note:  teams from 2013 needs to be loaded')
        v.append('There should be 5 leaders tied for first place')
        v.append('The leader should be labeled as the PROJECTED WINNER')
        return v

    def setup(self):
        testdata = WinnerData(1985,2,"wip_fgf_l5_tb0",leave_objects_in_datastore=True)
        testdata.set_week_state("in_progress")
        testdata.number_of_players(10)
        testdata.number_of_leaders(5)
        testdata.week_unofficial()
        testdata.tiebreaker_winner(0)
        testdata.featured_game_state("final")
        testdata.setup()

    def cleanup(self):
        testdata = WinnerData(1985,2,"wip_fgf_l5_tb0",leave_objects_in_datastore=True)
        testdata.cleanup_database()

class WIP_FGF_L5_TB1_Test(VisualTest):
    def __init__(self):
        self.description = "Week In Progress, Featured Game Final, 5 Leaders Tied for First, Tiebreak 1 decides"
        self.link = "/1985/week/3/results"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('Note:  teams from 2013 needs to be loaded')
        v.append('There should be 5 leaders tied for first place')
        v.append('The leader should be labeled as the PROJECTED WINNER')
        return v

    def setup(self):
        testdata = WinnerData(1985,3,"wip_fgf_l5_tb1",leave_objects_in_datastore=True)
        testdata.set_week_state("in_progress")
        testdata.number_of_players(10)
        testdata.number_of_leaders(5)
        testdata.week_unofficial()
        testdata.tiebreaker_winner(1)
        testdata.featured_game_state("final")
        testdata.setup()

    def cleanup(self):
        testdata = WinnerData(1985,3,"wip_fgf_l5_tb1",leave_objects_in_datastore=True)
        testdata.cleanup_database()

class WIP_FGF_L5_TB2_Test(VisualTest):
    def __init__(self):
        self.description = "Week In Progress, Featured Game Final, 5 Leaders Tied for First, Tiebreak 2 decides"
        self.link = "/1985/week/4/results"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('Note:  teams from 2013 needs to be loaded')
        v.append('There should be 5 leaders tied for first place')
        v.append('The leader should be labeled as the PROJECTED WINNER')
        return v

    def setup(self):
        testdata = WinnerData(1985,4,"wip_fgf_l5_tb2",leave_objects_in_datastore=True)
        testdata.set_week_state("in_progress")
        testdata.number_of_players(10)
        testdata.number_of_leaders(5)
        testdata.week_unofficial()
        testdata.tiebreaker_winner(2)
        testdata.featured_game_state("final")
        testdata.setup()

    def cleanup(self):
        testdata = WinnerData(1985,4,"wip_fgf_l5_tb2",leave_objects_in_datastore=True)
        testdata.cleanup_database()

class WIP_FGF_L5_TB3_Test(VisualTest):
    def __init__(self):
        self.description = "Week In Progress, Featured Game Final, 5 Leaders Tied for First, Tiebreak 3 decides"
        self.link = "/1985/week/5/results"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('Note:  teams from 2013 needs to be loaded')
        v.append('There should be 5 leaders tied for first place')
        v.append('The leader should be labeled as the PROJECTED WINNER')
        return v

    def setup(self):
        testdata = WinnerData(1985,5,"wip_fgf_l5_tb3",leave_objects_in_datastore=True)
        testdata.set_week_state("in_progress")
        testdata.number_of_players(10)
        testdata.number_of_leaders(5)
        testdata.week_unofficial()
        testdata.tiebreaker_winner(3)
        testdata.make_tiebreak3_valid()
        testdata.featured_game_state("final")
        testdata.setup()

    def cleanup(self):
        testdata = WinnerData(1985,5,"wip_fgf_l5_tb3",leave_objects_in_datastore=True)
        testdata.cleanup_database()

class WIP_FGF_L5_TB3I_Test(VisualTest):
    def __init__(self):
        self.description = "Week In Progress, Featured Game Final, 5 Leaders Tied for First, Tiebreak 3 decides but indeterminate"
        self.link = "/1987/week/1/results"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('Note:  teams from 2013 needs to be loaded')
        v.append('There should be 5 leaders tied for first place')
        v.append('The leaders should be labeled as POSSIBLE WINNER')
        v.append('')
        return v

    def setup(self):
        testdata = WinnerData(1987,1,"wip_fgf_l5_tb3i",leave_objects_in_datastore=True)
        testdata.set_week_state("in_progress")
        testdata.number_of_players(10)
        testdata.number_of_leaders(5)
        testdata.week_unofficial()
        testdata.tiebreaker_winner(3)
        testdata.make_tiebreak3_indeterminate()
        testdata.featured_game_state("final")
        testdata.setup()

    def cleanup(self):
        testdata = WinnerData(1987,1,"wip_fgf_l5_tb3i",leave_objects_in_datastore=True)
        testdata.cleanup_database()



class WIP_FGIP_L1_Test(VisualTest):
    def __init__(self):
        self.description = "Week In Progress, Featured Game In Progress, Only 1 Leader"
        self.link = "/1985/week/6/results"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('Note:  teams from 2013 needs to be loaded')
        v.append('There should be 1 leader in first place')
        v.append('The leader should be labeled as the PROJECTED WINNER')
        return v

    def setup(self):
        testdata = WinnerData(1985,6,"wip_fgip_l1",leave_objects_in_datastore=True)
        testdata.set_week_state("in_progress")
        testdata.number_of_players(10)
        testdata.number_of_leaders(1)
        testdata.week_unofficial()
        testdata.featured_game_state("in_progress")
        testdata.setup()

    def cleanup(self):
        testdata = WinnerData(1985,6,"wip_fgip_l1",leave_objects_in_datastore=True)
        testdata.cleanup_database()


class WIP_FGIP_L5_TB0_Test(VisualTest):
    def __init__(self):
        self.description = "Week In Progress, Featured Game In Progress, 5 Leaders Tied for First, Tiebreak 0 decides"
        self.link = "/1985/week/7/results"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('Note:  teams from 2013 needs to be loaded')
        v.append('There should be 5 leaders tied for first place')
        v.append('The leader should be labeled as the PROJECTED WINNER')
        return v

    def setup(self):
        testdata = WinnerData(1985,7,"wip_fgip_l5_tb0",leave_objects_in_datastore=True)
        testdata.set_week_state("in_progress")
        testdata.number_of_players(10)
        testdata.number_of_leaders(5)
        testdata.week_unofficial()
        testdata.tiebreaker_winner(0)
        testdata.featured_game_state("in_progress")
        testdata.setup()

    def cleanup(self):
        testdata = WinnerData(1985,7,"wip_fgip_l5_tb0",leave_objects_in_datastore=True)
        testdata.cleanup_database()


class WIP_FGIP_L5_TB1_Test(VisualTest):
    def __init__(self):
        self.description = "Week In Progress, Featured Game In Progress, 5 Leaders Tied for First, Tiebreak 1 decides"
        self.link = "/1985/week/8/results"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('Note:  teams from 2013 needs to be loaded')
        v.append('There should be 5 leaders tied for first place')
        v.append('The leader should be labeled as the PROJECTED WINNER')
        return v

    def setup(self):
        testdata = WinnerData(1985,8,"wip_fgip_l5_tb1",leave_objects_in_datastore=True)
        testdata.set_week_state("in_progress")
        testdata.number_of_players(10)
        testdata.number_of_leaders(5)
        testdata.week_unofficial()
        testdata.tiebreaker_winner(1)
        testdata.featured_game_state("in_progress")
        testdata.setup()

    def cleanup(self):
        testdata = WinnerData(1985,8,"wip_fgip_l5_tb1",leave_objects_in_datastore=True)
        testdata.cleanup_database()


class WIP_FGIP_L5_TB2_Test(VisualTest):
    def __init__(self):
        self.description = "Week In Progress, Featured Game In Progress, 5 Leaders Tied for First, Tiebreak 2 decides"
        self.link = "/1985/week/9/results"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('Note:  teams from 2013 needs to be loaded')
        v.append('There should be 5 leaders tied for first place')
        v.append('The leader should be labeled as the PROJECTED WINNER')
        return v

    def setup(self):
        testdata = WinnerData(1985,9,"wip_fgip_l5_tb2",leave_objects_in_datastore=True)
        testdata.set_week_state("in_progress")
        testdata.number_of_players(10)
        testdata.number_of_leaders(5)
        testdata.week_unofficial()
        testdata.tiebreaker_winner(2)
        testdata.featured_game_state("in_progress")
        testdata.setup()

    def cleanup(self):
        testdata = WinnerData(1985,9,"wip_fgip_l5_tb2",leave_objects_in_datastore=True)
        testdata.cleanup_database()

class WIP_FGIP_L5_TB3_Test(VisualTest):
    def __init__(self):
        self.description = "Week In Progress, Featured Game In Progress, 5 Leaders Tied for First, Tiebreak 3 decides"
        self.link = "/1985/week/10/results"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('Note:  teams from 2013 needs to be loaded')
        v.append('There should be 5 leaders tied for first place')
        v.append('The leader should be labeled as the PROJECTED WINNER')
        return v

    def setup(self):
        testdata = WinnerData(1985,10,"wip_fgip_l5_tb3",leave_objects_in_datastore=True)
        testdata.set_week_state("in_progress")
        testdata.number_of_players(10)
        testdata.number_of_leaders(5)
        testdata.week_unofficial()
        testdata.tiebreaker_winner(3)
        testdata.make_tiebreak3_valid()
        testdata.featured_game_state("in_progress")
        testdata.setup()

    def cleanup(self):
        testdata = WinnerData(1985,10,"wip_fgip_l5_tb3",leave_objects_in_datastore=True)
        testdata.cleanup_database()

class WIP_FGIP_L5_TB3I_Test(VisualTest):
    def __init__(self):
        self.description = "Week In Progress, Featured Game In Progress, 5 Leaders Tied for First, Tiebreak 3 decides but indeterminate"
        self.link = "/1987/week/2/results"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('Note:  teams from 2013 needs to be loaded')
        v.append('There should be 5 leaders tied for first place')
        v.append('The leaders should be labeled as POSSIBLE WINNER')
        v.append('')
        return v

    def setup(self):
        testdata = WinnerData(1987,2,"wip_fgip_l5_tb3i",leave_objects_in_datastore=True)
        testdata.set_week_state("in_progress")
        testdata.number_of_players(10)
        testdata.number_of_leaders(5)
        testdata.week_unofficial()
        testdata.tiebreaker_winner(3)
        testdata.make_tiebreak3_indeterminate()
        testdata.featured_game_state("in_progress")
        testdata.setup()

    def cleanup(self):
        testdata = WinnerData(1987,2,"wip_fgip_l5_tb3i",leave_objects_in_datastore=True)
        testdata.cleanup_database()

class WIP_FGNS_L1_Test(VisualTest):
    def __init__(self):
        self.description = "Week In Progress, Featured Game Not Started, Only 1 Leader"
        self.link = "/1985/week/11/results"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('Note:  teams from 2013 needs to be loaded')
        v.append('There should be 1 leader in first place')
        v.append('No leader should be selected as the winner')
        return v

    def setup(self):
        testdata = WinnerData(1985,11,"wip_fgns_l1",leave_objects_in_datastore=True)
        testdata.set_week_state("in_progress")
        testdata.number_of_players(10)
        testdata.number_of_leaders(1)
        testdata.week_unofficial()
        testdata.featured_game_state("not_started")
        testdata.setup()

    def cleanup(self):
        testdata = WinnerData(1985,11,"wip_fgns_l1",leave_objects_in_datastore=True)
        testdata.cleanup_database()

class WIP_FGNS_L5_Test(VisualTest):
    def __init__(self):
        self.description = "Week In Progress, Featured Game Not Started, 5 Leaders Tied for First"
        self.link = "/1985/week/12/results"
        self.verify =  self.__verify_instructions()

    def __verify_instructions(self):
        v = []
        v.append('Note:  teams from 2013 needs to be loaded')
        v.append('There should be 5 leaders tied for first place')
        v.append('No leader should be selected as the winner')
        return v

    def setup(self):
        testdata = WinnerData(1985,12,"wip_fgns_l5",leave_objects_in_datastore=True)
        testdata.set_week_state("in_progress")
        testdata.number_of_players(10)
        testdata.number_of_leaders(5)
        testdata.week_unofficial()
        testdata.tiebreaker_winner(0)
        testdata.featured_game_state("not_started")
        testdata.setup()

    def cleanup(self):
        testdata = WinnerData(1985,12,"wip_fgns_l5",leave_objects_in_datastore=True)
        testdata.cleanup_database()

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
        testdata.featured_game_state("not_started")
        testdata.setup()

    def cleanup(self):
        testdata = WinnerData(1984,1,"wns",leave_objects_in_datastore=True)
        testdata.cleanup_database()
