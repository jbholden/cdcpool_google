ROOT_PATH = '../../.'
import sys
sys.path.append(ROOT_PATH)

from scripts.api.fbpool_api import *
from scripts.api.fbpool_api_exception import *
from scripts.excel.pool_spreadsheet import *
from scripts.excel.team import *
from fbpool_args import *
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

    def load_missing_teams(self,year):
        excel = PoolSpreadsheet(year,self.__excel_full_path())
        teams = excel.get_teams()

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            for team in teams:
                fbpool_api.createTeamIfDoesNotExist(team.name,team.conference)
        except FBAPIException as e:
            self.__load_error("teams",e)

    def load_teams(self,year):
        excel = PoolSpreadsheet(year,self.__excel_full_path())
        teams = excel.get_teams()

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            for team in teams:
                fbpool_api.createTeam(team.name,team.conference)
        except FBAPIException as e:
            self.__load_error("teams",e)

    def load_players(self,year):
        excel = PoolSpreadsheet(year,self.__excel_full_path())
        excel_players = excel.get_players()

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            for excel_player_name in excel_players:
                player_name = self.__remove_remote(excel_player_name)
                player = fbpool_api.createPlayerIfDoesNotExist(player_name,[year])
                if year not in player['years']:
                    data = { "years":player['years'] + [year] }
                    fbpool_api.editPlayerByKey(player['key'],data)
        except FBAPIException as e:
            self.__load_error("players",e)

    def __load_week_games(self,excel,week_number):
        excel_games = excel.get_games(week_number)
        week_games = []

        if self.verbose:
            print " : week games..."

        try:
            fbpool_api = FBPoolAPI(url=self.url)

            for excel_game in excel_games.values():
                team1 = fbpool_api.getTeam(excel_game.team1) 
                team2 = fbpool_api.getTeam(excel_game.team2) 

                data = dict()
                data['number'] = excel_game.number
                data['team1'] = team1['key']
                data['team2'] = team2['key']
                data['team1_score'] = excel_game.team1_score
                data['team2_score'] = excel_game.team2_score
                data['favored'] = excel_game.favored
                data['spread'] = excel_game.spread
                data['state'] = excel_game.state
                data['quarter'] = None
                data['time_left'] = None
                data['date'] = None

                game = fbpool_api.createGame(data)
                week_games.append(game)

        except FBAPIException as e:
            self.__load_error("week games",e)

        return week_games

    def __get_week_winner(self,excel,week):
        winner_name = excel.get_week_winner(week)
        if winner_name == None:
            return None

        winner_name = self.__remove_remote(winner_name)

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            player = fbpool_api.getPlayer(winner_name)
            return player['key']
        except FBAPIException as e:
            self.__load_error("week games",e)

        return None

    def __find_game_number(self,games,number):
        for game in games:
            if game['number'] == number:
                return game
        print "**ERROR** Encountered error when loading games"
        print "----------------------------------------------"
        print "Could not find game number %d" % (number)
        print ""
        sys.exit(1)


    def __load_week_picks(self,excel,week,week_games):
        excel_picks = excel.get_picks(week['number'])

        if self.verbose:
            print " : week picks..."

        try:
            fbpool_api = FBPoolAPI(url=self.url)

            players = fbpool_api.getPlayersInYear(week['year'])
            player_lookup = { player['name']:player for player in players }

            number_of_picks = len(excel_picks)
            for i,excel_pick in enumerate(excel_picks):

                if self.verbose and (i%50) == 0:
                    print " : week picks (%d of %d)..." % (i,number_of_picks)

                name = self.__remove_remote(excel_pick.player_name)
                player = player_lookup[name]
                game = self.__find_game_number(week_games,excel_pick.game_number)

                data = dict()
                data['week'] = week['key']
                data['player'] = player['key']
                data['game'] = game['key']

                if excel_pick.default:
                    data['winner'] = None
                    data['team1_score'] = None
                    data['team2_score'] = None
                else:
                    data['winner'] = excel_pick.winner
                    data['team1_score'] = excel_pick.team1_score
                    data['team2_score'] = excel_pick.team2_score

                pick = fbpool_api.createPick(data)
        except FBAPIException as e:
            self.__load_error("week picks",e)

    def delete_year(self,year):
        if self.verbose:
            print ""
            print "deleting year %d..." % (year)

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            weeks = fbpool_api.getWeeksInYear(year)
        except FBAPIException as e:
            self.__delete_year_error("could not get weeks in %d" % (year),e)

        for week in weeks:
            if self.verbose:
                print " : deleting %d week %d..." % (year,week['number'])
            self.__delete_week(fbpool_api,week)


    def delete_week(self,year,week_number):
        if self.verbose:
            print ""
            print "deleting year %d week %d..." % (year,week_number)

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            week = fbpool_api.getWeek(year,week_number)
        except FBAPIException as e:
            self.__delete_week_error("could not get %d week %d" % (year,week_number),e)

        self.__delete_week(fbpool_api,week)

    def __delete_week(self,fbpool_api,week):
        year = week['year']
        week_number = week['number']

        # try to delete as many games as possible, ignore errors
        if self.verbose:
            print " : deleting week games..."

        for game_key in week['games']:
            try:
                fbpool_api.deleteGameByKey(game_key)
            except FBAPIException as e:
                continue

        # try to delete as many picks as possible, ignore errors
        if self.verbose:
            print " : deleting week picks..."

        try:
            picks = fbpool_api.getWeekPicks(year,week_number)
        except FBAPIException as e:
            picks = None

        if picks != None:
            number_of_picks = len(picks)
            for i,pick in enumerate(picks):
                if self.verbose and (i%50) == 0:
                    print " : deleting week picks (%d of %d)..." % (i,number_of_picks)

                try:
                    fbpool_api.deletePickByKey(pick['key'])
                except FBAPIException as e:
                    continue

        # finally try and delete the week
        try:
            fbpool_api.deleteWeekByKey(week['key'])
        except FBAPIException as e:
            self.__delete_week_error("could not delete %d week %d" % (year,week_number),e)

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

    def delete_all(self):
        if self.verbose:
            print ""
            print "deleting entire database..."

        try:
            fbpool_api = FBPoolAPI(url=self.url)

            if self.verbose:
                print " : deleting teams..."
            fbpool_api.deleteAllTeams()

            if self.verbose:
                print " : deleting players..."
            fbpool_api.deleteAllPlayers()

            if self.verbose:
                print " : deleting weeks..."
            fbpool_api.deleteAllWeeks()

            if self.verbose:
                print " : deleting games..."
            fbpool_api.deleteAllGames()

            if self.verbose:
                print " : deleting picks..."
            fbpool_api.deleteAllPicks()

            if self.verbose:
                print " : flushing memcache..."
            fbpool_api.deleteCache()

        except FBAPIException as e:
            self.__delete_error(e)

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


    def load_week(self,year,week,load_teams_and_players=True,update_memcache=True):
        if self.verbose:
            print ""
            print "loading year %d week %d..." % (year,week)

        if load_teams_and_players:
            if self.verbose:
                print " : verifying week teams and players are loaded..."
            self.load_missing_teams(year)
            self.load_players(year)

        excel = PoolSpreadsheet(year,self.__excel_full_path())

        week_games = self.__load_week_games(excel,week)
        winner_key = self.__get_week_winner(excel,week)

        week_data = dict()
        week_data['year'] = year
        week_data['number'] = week
        week_data['winner'] = winner_key
        week_data['games'] = [ game['key'] for game in week_games ]
        week_data['lock_picks'] = None
        week_data['lock_scores'] = None

        if self.verbose:
            print " : week object..."

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            created_week = fbpool_api.createWeek(week_data)
        except FBAPIException as e:
            self.__load_error("week",e)

        self.__load_week_picks(excel,created_week,week_games)

        if self.verbose:
            print " : cleaning up..."

        try:
            fbpool_api.deletePicksCache()
            fbpool_api.deleteGamesCache()
            fbpool_api.deleteWeeksCache()
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            print "Not stopping because of exception..."

        if update_memcache:
            if self.verbose:
                print " : updating memcache..."

            try:
                fbpool_api.updateCacheForWeek(year,week)
            except FBAPIException as e:
                print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
                print "Not stopping because of exception..."

        if self.verbose:
            print "week %d loaded." % (week)
            print ""

    def load_year(self,year,load_teams_in_year=True,load_players_in_year=True):
        if self.verbose:
            print ""
            print "loading year %d..." % (year)

        excel = PoolSpreadsheet(year,self.__excel_full_path())
        week_numbers = excel.get_week_numbers()

        if load_teams_in_year:
            if self.verbose:
                print " : verifying teams are loaded..."
            self.load_missing_teams(year)

        if load_players_in_year:
            if self.verbose:
                print " : verifying players are loaded..."
            self.load_players(year)

        for week_number in week_numbers:
            self.load_week(year,week_number,load_teams_and_players=False,update_memcache=False)

        if self.verbose:
            print " : cleaning up..."

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            fbpool_api.deletePlayersCache()
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            print "Not stopping because of exception..."

        if self.verbose:
            print " : updating memcache..."

        try:
            fbpool_api.updateCacheForYear(year)
        except FBAPIException as e:
            print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
            print "Not stopping because of exception..."

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


    def __load_error(self,name,e):
        print "**ERROR** Encountered error when loading %s" % (name)
        print "---------------------------------------------"
        print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
        print "Database data may be in an invalid state."
        print ""
        sys.exit(1)

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
        print "**ERROR** Encountered error when deleting database"
        print "--------------------------------------------------"
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


    def __remove_remote(self,name):
        return string.replace(name,"Remote","").strip()


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
        fbpool = FBPool(url=url,excel_dir=args.excel_dir,excel_workbook=excel_file)
        fbpool.supress_output(args.quiet)
        fbpool.load_teams(most_recent_year)

    elif action == "load_teams_in_year":
        excel_file = fbpool_args.get_excel_file(args.year)
        fbpool = FBPool(url=url,excel_dir=args.excel_dir,excel_workbook=excel_file)
        fbpool.supress_output(args.quiet)
        fbpool.load_teams(args.year)

    elif action == "load_players_in_year":
        excel_file = fbpool_args.get_excel_file(args.year)
        fbpool = FBPool(url=url,excel_dir=args.excel_dir,excel_workbook=excel_file)
        fbpool.supress_output(args.quiet)
        fbpool.load_players(args.year)

    elif action == "load_players_all_years":
        excel_files = fbpool_args.get_excel_files()
        for year in excel_files:
            fbpool = FBPool(url=url,excel_dir=args.excel_dir,excel_workbook=excel_files[year])
            fbpool.supress_output(args.quiet)
            fbpool.load_players(year)

    elif action == "load_week":
        excel_file = fbpool_args.get_excel_file(args.year)
        fbpool = FBPool(url=url,excel_dir=args.excel_dir,excel_workbook=excel_file)
        fbpool.supress_output(args.quiet)
        fbpool.load_week(args.year,args.week)

    elif action == "load_year":
        excel_file = fbpool_args.get_excel_file(args.year)
        fbpool = FBPool(url=url,excel_dir=args.excel_dir,excel_workbook=excel_file)
        fbpool.supress_output(args.quiet)
        fbpool.load_year(args.year)

    elif action == "update_week":
        excel_file = fbpool_args.get_excel_file(args.year)
        fbpool = FBPool(url=url,excel_dir=args.excel_dir,excel_workbook=excel_file)
        fbpool.supress_output(args.quiet)
        fbpool.update_week(args.year,args.week)

    elif action == "delete_year":
        excel_file = fbpool_args.get_excel_file(args.year)
        fbpool = FBPool(url=url,excel_dir=args.excel_dir,excel_workbook=excel_file)
        fbpool.supress_output(args.quiet)
        fbpool.delete_year(args.year)

    elif action == "delete_week":
        excel_file = fbpool_args.get_excel_file(args.year)
        fbpool = FBPool(url=url,excel_dir=args.excel_dir,excel_workbook=excel_file)
        fbpool.supress_output(args.quiet)
        fbpool.delete_week(args.year,args.week)

    elif action == "delete_all":
        fbpool = FBPool(url=url,excel_dir=args.excel_dir,excel_workbook=None)
        fbpool.supress_output(args.quiet)
        fbpool.delete_all()

    elif action == "delete_players":
        pass

    elif action == "delete_teams":
        pass

    elif action == "flush_memcache":
        fbpool = FBPool(url=url,excel_dir=args.excel_dir,excel_workbook=None)
        fbpool.supress_output(args.quiet)
        fbpool.flush_memcache()

    elif action == "load_memcache":
        pass

    elif action == "cleanup_api":
        pass

    elif action == "search_for_unassociated_data":
        pass

    elif action == "search_for_errors":
        # duplicate weeks
        # unassociated data
        pass

    elif action == "list_teams":
        pass

    elif action == "list_players":
        pass

    elif action == "list_weeks":
        pass

    elif action == "list_picks":
        pass

    elif action == "list_games":
        pass



