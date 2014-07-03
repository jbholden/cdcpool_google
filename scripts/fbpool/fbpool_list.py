ROOT_PATH = '../../.'
import sys
sys.path.append(ROOT_PATH)

from scripts.api.fbpool_api import *
from scripts.api.fbpool_api_exception import *
from scripts.excel.pool_spreadsheet import *
from scripts.excel.team import *
from fbpool_error import *
from fbpool_verbose import *
import string

class FBPoolList:

    def __init__(self,url,excel_dir,excel_workbook,quiet=False):
        self.url = url
        self.excel_dir = excel_dir
        self.excel_workbook = excel_workbook
        self.__verbose = FBPoolVerbose(quiet)

    def list_all_teams(self):
        self.__verbose.start("reading teams from database...")

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            teams = fbpool_api.getAllTeams()
        except FBAPIException as e:
            FBPoolError.exit_with_error("list all teams",e,"error getting teams")

        teams_sorted = sorted(teams,key=lambda team:team['name'])

        print ""
        print "Teams: (%d)" % (len(teams_sorted))
        print "----------------------------------------------------------------------------------"
        for team in teams_sorted:
            print "%-40s %s" % (team['name'],team['conference'])
        print "----------------------------------------------------------------------------------"
        print ""

    def list_all_players(self):
        self.__verbose.start("reading players from database...")

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            players = fbpool_api.getAllPlayers()
        except FBAPIException as e:
            FBPoolError.exit_with_error("list all players",e,"error getting players")

        players_sorted = sorted(players,key=lambda player:player['name'])

        print ""
        print "Players:"
        print "----------------------------------------------------------------------------------"
        for player in players_sorted:
            print "%-40s %s" % (player['name'],self.__array_str(player['years']))
        print "----------------------------------------------------------------------------------"
        print ""


    def list_all_weeks(self):
        self.__verbose.start("reading weeks from database...")

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            weeks = fbpool_api.getAllWeeks()
        except FBAPIException as e:
            FBPoolError.exit_with_error("list all weeks",e,"error getting weeks")

        years = sorted(set([week['year'] for week in weeks ]))

        print ""
        print "Weeks:"
        print "----------------------------------------------------------------------------------"
        for year in years:
            numbers = sorted([ week['number'] for week in weeks if week['year'] == year])

            for week_number in numbers:
                print "%d Week %d" % (year,week_number)

            print ""

        print "----------------------------------------------------------------------------------"
        print ""

    def __array_str(self,a):
        s = ""
        last = len(a)-1
        for i in range(last+1):
            if i == last:
                s += str(a[i])
            else:
                s += "%s, " % (a[i])
        return s

