ROOT_PATH = '../../.'
import sys
sys.path.append(ROOT_PATH)

from scripts.api.fbpool_api import *
from scripts.api.fbpool_api_exception import *
from scripts.excel.pool_spreadsheet import *
from scripts.excel.team import *
from fbpool_args import *
from fbpool_load import *
from fbpool_delete import *
import string

class FBPool:
    def __init__(self,url,excel_dir,excel_workbook):
        self.url = url
        self.excel_dir = excel_dir
        self.excel_workbook = excel_workbook
        self.verbose = True

    def supress_output(self,supress):
        if supress == None or supress == False:
            self.verbose = True
        else:
            self.verbose = False

    def __excel_full_path(self):
        return "%s/%s" % (self.excel_dir,self.excel_workbook)

    def cleanup_api(self):
        if self.verbose:
            print "Flushing API data from the memcache..."

        try:
            fbpool_api.deletePicksCache()
            fbpool_api.deleteGamesCache()
            fbpool_api.deleteWeeksCache()
            fbpool_api.deletePlayersCache()
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)

        if self.verbose:
            print ""

    def flush_memcache(self):
        if self.verbose:
            print ""
            print "flushing entire memcache..."

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            fbpool_api.deleteCache()
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)

        if self.verbose:
            print ""

    def load_memcache(self):
        if self.verbose:
            print ""
            print "loading entire memcache..."

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            fbpool_api.updateCache()
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)

        if self.verbose:
            print ""

    def load_memcache_for_year(self,year):
        if self.verbose:
            print ""
            print "loading %d into memcache..." % (year)

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            fbpool_api.updateCacheForYear(year)
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)

        if self.verbose:
            print ""

    def load_memcache_for_week(self,year,week_number):
        if self.verbose:
            print ""
            print "loading %d week %d into memcache..." % (year,week_number)

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            fbpool_api.updateCacheForWeek(year,week_number)
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)

        if self.verbose:
            print ""


    def update_week(self,year,week_number):
        if self.verbose:
            print ""
            print "updating results for year %d week %d..." % (year,week_number)

        excel = PoolSpreadsheet(year,self.__excel_full_path())
        week_winner_name = excel.get_week_winner(week_number)
        excel_games = excel.get_games(week_number)

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            week = fbpool_api.getWeek(year,week_number)

            # update the week winner
            if week_winner_name == None and week['winner'] != None:
                edit_data = dict()
                edit_data['winner'] = None
                fbpool_api.editWeekByKey(week['key'],edit_data)
            elif week_winner_name != None:
                player = fbpool_api.getPlayer(week_winner_name)
                winner_key = player['key']
                winner_changed = winner_key != week['winner']
                if winner_changed:
                    edit_data = dict()
                    edit_data['winner'] = winner_key
                    fbpool_api.editWeekByKey(week['key'],edit_data)

            # update the game info
            for game_key in week['games']:
                game = fbpool_api.getGameByKey(game_key)
                excel_game = excel_games.get(game['number'])
                if excel_game == None:
                    continue

                edit_data = dict()
                edit_data['team1_score'] = excel_game.team1_score
                edit_data['team2_score'] = excel_game.team2_score
                edit_data['state'] = excel_game.state

                fbpool_api.editGameByKey(game_key,edit_data)


        except FBAPIException as e:
            self.__update_week_error(e)

        if self.verbose:
            print ""


    def verify_player_exists(self,player_name,year):
        try:
            fbpool_api = FBPoolAPI(url=self.url)
            player = fbpool_api.getPlayer(player_name)
        except FBAPIException as e:
            player_does_not_exist = e.http_code == 404 and e.errmsg == "could not find the player"
            if player_does_not_exist:
                return False

            print "**ERROR** Encountered error when getting players in year %d" % (year)
            print "---------------------------------------------------------------------"
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            print ""
            sys.exit(1)

        if year in player['years']:
            return True
        return False

    def verify_team_exists(self,team_name):
        try:
            fbpool_api = FBPoolAPI(url=self.url)
            team = fbpool_api.getTeam(team_name)
        except FBAPIException as e:
            team_does_not_exist = e.http_code == 404 and e.errmsg == "could not find the team"
            if team_does_not_exist:
                return False

            print "**ERROR** Encountered error when getting team %s" % (team_name)
            print "---------------------------------------------------------------------"
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            print ""
            sys.exit(1)

        return True

    def check_for_missing_weeks_and_years(self):
        if self.verbose:
            print ""
            print "checking for missing weeks..."

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            weeks = fbpool_api.getAllWeeks()
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            sys.exit(1)

        years = sorted(set([week['year'] for week in weeks ]))

        # check for missing years
        first_year = min(years)
        last_year = max(years)
        missing_years = []
        for year in range(first_year,last_year+1):
            if year not in years:
                missing_years.append(year)

        # check for missing weeks
        week_numbers = dict()
        for year in years:
            numbers = sorted([ week['number'] for week in weeks if week['year'] == year])
            week_numbers[year] = numbers

        missing = dict()
        for year in years:
            if year != last_year:
                for number in range(1,14):
                    if number not in week_numbers[year]:
                        if year not in missing:
                            missing[year] = [number]
                        else:
                            missing[year].append(number)
        
        last_week = max(week_numbers[last_year])
        for number in range(1,last_week+1):
            if number not in week_numbers[last_year]:
                if last_year not in missing:
                    missing[last_year] = [number]
                else:
                    missing[last_year].append(number)

        duplicates = dict()
        for year in years:
            first = min(week_numbers[year])
            last = max(week_numbers[year])
            for number in range(first,last+1):
                count = 0
                for current_number in week_numbers[year]:
                    if number == current_number:
                        count += 1
                if count > 1:
                    if year not in duplicates:
                        duplicates[year] = [number]
                    else:
                        duplicates[year].append(number)

        extras = dict()
        for year in years:
            for number in week_numbers[year]:
                if number < 1 or number > 13:
                    if year not in extras:
                        extras[year] = [number]
                    else:
                        extras[year].append(number)

        print ""
        if len(missing_years) == 0:
            print "Missing Years   :  None"
        else:
            print "Missing Years   : %s" % (self.__array_str(missing_years))

        if len(missing) == 0:
            print "Missing Weeks   :  None"
        else:
            print "Missing Weeks   :"
            for year in missing:
                print "           %s : %s" % (year,self.__array_str(missing[year]))

        if len(duplicates) == 0:
            print "Duplicate Weeks :  None"
        else:
            print "Duplicate Weeks :  "
            for year in duplicates:
                print "           %s : %s" % (year,self.__array_str(duplicates[year]))

        if len(extra) == 0:
            print "Extra Weeks     :  None"
        else:
            print "Extra Weeks     :  "
            for year in extra:
                print "           %s : %s" % (year,self.__array_str(extra[year]))

        print ""

    def list_all_teams(self):
        if self.verbose:
            print ""
            print "reading teams from database..."

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            teams = fbpool_api.getAllTeams()
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            sys.exit(1)

        teams_sorted = sorted(teams,key=lambda team:team['name'])

        print ""
        print "Teams: (%d)" % (len(teams_sorted))
        print "----------------------------------------------------------------------------------"
        for team in teams_sorted:
            print "%-40s %s" % (team['name'],team['conference'])
        print "----------------------------------------------------------------------------------"
        print ""

    def list_all_players(self):
        if self.verbose:
            print ""
            print "reading players from database..."

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            players = fbpool_api.getAllPlayers()
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            sys.exit(1)

        players_sorted = sorted(players,key=lambda player:player['name'])

        print ""
        print "Players:"
        print "----------------------------------------------------------------------------------"
        for player in players_sorted:
            print "%-40s %s" % (player['name'],self.__array_str(player['years']))
        print "----------------------------------------------------------------------------------"
        print ""

    def list_all_weeks(self):
        if self.verbose:
            print ""
            print "reading weeks from database..."

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            weeks = fbpool_api.getAllWeeks()
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            sys.exit(1)

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


    def __update_week_error(self,e):
        print "**ERROR** Encountered error when updating week"
        print "----------------------------------------------"
        print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
        print ""
        sys.exit(1)

    def __delete_week_error(self,message,e):
        print "**ERROR** Encountered error when deleting week"
        print "----------------------------------------------"
        print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
        print message
        print ""
        sys.exit(1)

    def __delete_error(self,e):
        print "**ERROR** Encountered error when deleting"
        print "-----------------------------------------"
        print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
        print ""
        sys.exit(1)

    def __delete_year_error(self,message,e):
        print "**ERROR** Encountered error when deleting year"
        print "----------------------------------------------"
        print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
        print message
        print ""
        sys.exit(1)


if __name__ == "__main__":

    fbpool_args = FBPoolArgs()
    url = fbpool_args.get_url()
    args = fbpool_args.get_args()
    action = fbpool_args.get_action()

    # TODO:  cleanup cache, load memcache
    # TODO:  verbose option
    # TODO:  finer grain:  load week picks, load week games, load week, load specific player week picks (?)
    # TODO:  delete week, etc.
    # TODO:  search for unassociated data
    # TODO:  conflicts:  teams, player names
    # TODO:  check if players in year loaded or not?  teams in year?
    # TODO:  update week results
    # TODO:  query for data?  list players, list games in week, etc.

    if action == "load_teams_most_recent_year":
        most_recent_year,excel_file = fbpool_args.get_latest_pool_file_and_year()
        fbpool = FBPoolLoad(url=url,excel_dir=args.excel_dir,excel_workbook=excel_file,quiet=args.quiet)
        fbpool.load_teams(most_recent_year)

    elif action == "load_teams_in_year":
        excel_file = fbpool_args.get_excel_file(args.year)
        fbpool = FBPoolLoad(url=url,excel_dir=args.excel_dir,excel_workbook=excel_file,quiet=args.quiet)
        fbpool.load_teams(args.year)

    elif action == "load_players_in_year":
        excel_file = fbpool_args.get_excel_file(args.year)
        fbpool = FBPoolLoad(url=url,excel_dir=args.excel_dir,excel_workbook=excel_file,quiet=args.quiet)
        fbpool.load_players(args.year)

    elif action == "load_players_all_years":
        excel_files = fbpool_args.get_excel_files()
        for year in excel_files:
            fbpool = FBPoolLoad(url=url,excel_dir=args.excel_dir,excel_workbook=excel_files[year],quiet=args.quiet)
            fbpool.load_players(year)

    elif action == "load_week":
        excel_file = fbpool_args.get_excel_file(args.year)
        fbpool = FBPoolLoad(url=url,excel_dir=args.excel_dir,excel_workbook=excel_file,quiet=args.quiet)
        fbpool.load_week(args.year,args.week)

    elif action == "load_year":
        excel_file = fbpool_args.get_excel_file(args.year)
        fbpool = FBPoolLoad(url=url,excel_dir=args.excel_dir,excel_workbook=excel_file,quiet=args.quiet)
        fbpool.load_year(args.year)

    elif action == "update_week":
        excel_file = fbpool_args.get_excel_file(args.year)
        fbpool = FBPool(url=url,excel_dir=args.excel_dir,excel_workbook=excel_file)
        fbpool.supress_output(args.quiet)
        fbpool.update_week(args.year,args.week)

    elif action == "delete_year":
        excel_file = fbpool_args.get_excel_file(args.year)
        fbpool = FBPoolDelete(url=url,excel_dir=args.excel_dir,excel_workbook=excel_file,quiet=args.quiet)
        fbpool.delete_year(args.year)

    elif action == "delete_week":
        excel_file = fbpool_args.get_excel_file(args.year)
        fbpool = FBPoolDelete(url=url,excel_dir=args.excel_dir,excel_workbook=excel_file,quiet=args.quiet)
        fbpool.delete_week(args.year,args.week)

    elif action == "delete_all":
        fbpool = FBPoolDelete(url=url,excel_dir=args.excel_dir,excel_workbook=None,quiet=args.quiet)
        fbpool.delete_all()

    elif action == "delete_all_players":
        fbpool = FBPoolDelete(url=url,excel_dir=args.excel_dir,excel_workbook=None,quiet=args.quiet)
        fbpool.delete_players()

    elif action == "delete_players_from_year":
        fbpool = FBPoolDelete(url=url,excel_dir=args.excel_dir,excel_workbook=None,quiet=args.quiet)
        fbpool.delete_players_from_year(args.year)

    elif action == "delete_teams":
        fbpool = FBPoolDelete(url=url,excel_dir=args.excel_dir,excel_workbook=None,quiet=args.quiet)
        fbpool.delete_teams()

    elif action == "flush_memcache":
        fbpool = FBPool(url=url,excel_dir=args.excel_dir,excel_workbook=None)
        fbpool.supress_output(args.quiet)
        fbpool.flush_memcache()

    elif action == "load_memcache":
        fbpool = FBPool(url=url,excel_dir=args.excel_dir,excel_workbook=None)
        fbpool.supress_output(args.quiet)
        fbpool.load_memcache()

    elif action == "load_memcache_for_year":
        fbpool = FBPool(url=url,excel_dir=args.excel_dir,excel_workbook=None)
        fbpool.supress_output(args.quiet)
        fbpool.load_memcache_for_year(args.year)

    elif action == "load_memcache_for_week":
        fbpool = FBPool(url=url,excel_dir=args.excel_dir,excel_workbook=None)
        fbpool.supress_output(args.quiet)
        fbpool.load_memcache_for_year(args.year,args.week)

    elif action == "cleanup_api":
        fbpool = FBPool(url=url,excel_dir=args.excel_dir,excel_workbook=None)
        fbpool.supress_output(args.quiet)
        fbpool.cleanup_api()

    elif action == "search_for_unassociated_data":
        pass

    elif action == "search_for_errors":
        # duplicate weeks
        # unassociated data
        pass

    elif action == "list_teams":
        fbpool = FBPool(url=url,excel_dir=args.excel_dir,excel_workbook=None)
        fbpool.supress_output(args.quiet)
        fbpool.list_all_teams()

    elif action == "list_players":
        fbpool = FBPool(url=url,excel_dir=args.excel_dir,excel_workbook=None)
        fbpool.supress_output(args.quiet)
        fbpool.list_all_players()

    elif action == "list_weeks":
        fbpool = FBPool(url=url,excel_dir=args.excel_dir,excel_workbook=None)
        fbpool.supress_output(args.quiet)
        fbpool.list_all_weeks()

    elif action == "list_picks":
        pass

    elif action == "list_games":
        pass



