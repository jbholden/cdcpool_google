from visual.week_results import *
from visual.player_results import *
from visual.overall_results import *
from visual.update_games import *
from visual.winner import *

# the tests dictionary are the tests that will be displayed on the visual tests page.
# the key represents a test category
# the values represent the test classes to run for that category
#
# the test classes are defined in /tests/visual

tests = dict()

tests['Week Results'] = [ FinalWeekResultsTest, 
                          WeekInProgressResultsTest, 
                          NotStartedWeekResultsTest, 
                          WeekInProgressGamesInProgressResultsTest, 
                          NotStartedDefaultersWeekResultsTest ]

tests['Overall Results'] = [ FinalResultsTest,
                             BadYearResultsTest,
                             NotStartedResultsTest,
                             NotStartedWithPlayersResultsTest,
                             EnterPicksResultsTest,
                             EnterPicksWeek1ResultsTest,
                             WeekNotStartedResultsTest,
                             WeekInProgressResultsTest,
                             WeekFinalResultsTest ]

tests['Player Results'] = [ FinalPlayerResultsTest,
                            NotStartedPlayerResultsTest,
                            NotStartedPlayerResultsDefaulterTest,
                            InProgressPlayerResultsTest,
                            BeforePickDeadlinePlayerResultsTest,
                            AfterPickDeadlinePlayerResultsTest,
                            BadYearPlayerResultsTest,
                            BadWeekNumberPlayerResultsTest,
                            BadPlayerPlayerResultsTest ]

tests['Update Games'] = [ GamesFinalTest, 
                          GamesNotStartedTest,
                          GamesInProgressTest,
                          ScoresLockedTest ]

tests['Week Results Winner'] = [ #WFO_L1_Test,
                          #WFO_L5_Test,
                          #WFU_L1_Test,
                          #WFU_L5_TB0_Test,
                          #WFU_L5_TB1_Test,
                          #WFU_L5_TB2_Test,
                          #WFU_L5_TB3_Test,
                          #WIP_FGF_L1_Test,
                          #WIP_FGF_L5_TB0_Test,
                          #WIP_FGF_L5_TB1_Test,
                          #WIP_FGF_L5_TB2_Test,
                          #WIP_FGF_L5_TB3_Test,
                          #WIP_FGIP_L1_Test,
                          #WIP_FGIP_L5_TB0_Test,
                          #WIP_FGIP_L5_TB1_Test,
                          #WIP_FGIP_L5_TB2_Test,
                          #WIP_FGIP_L5_TB3_Test,
                          #WIP_FGNS_L1_Test,
                          #WIP_FGNS_L5_Test,
                          WNS_Test ]
