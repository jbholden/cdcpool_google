from test_calculator import *
from test_week_data import *
from test_update import *
from test_week_results import *
from test_player_results import *
from test_update_games import *
from database.test_weeks import *
from database.test_players import *
from database.test_teams import *
from database.test_games import *
from database.test_picks import *
from database.test_load_week import *
from database.test_pool_state import *
from test_timezone import *
from api.test_team import *

# Instructions.
# 1. create a test using the unittest class
# 2. import the class
# 3. modify this array to contain the test (name,test class)
test_classes = [('test players in datastore',TestPlayers),
                ('test teams in datastore',TestTeams),
                ('test weeks in datastore',TestWeeks),
                ('test games in datastore',TestGames),
                ('test picks in datastore',TestPicks),
                ('test load week data',TestWeekLoad),
                ('test pool state',TestPoolState),
                ('test week data class',TestWeekData),
                ('test the calculator class',TestCalculator),
                ('test the update class',TestUpdate),
                ('test the week results page',TestWeekResults),
                ('test the player results page',TestPlayerResults),
                ('test the pytz timezone module',TestTimezone),
                ('test the update games form',TestUpdateGames) ]
