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

    def __excel_full_path(self):
        return "%s/%s" % (self.excel_dir,self.excel_workbook)

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

        try:
            fbpool_api = FBPoolAPI(url=self.url)

            players = fbpool_api.getPlayersInYear(week['year'])
            player_lookup = { player['name']:player for player in players }


            for excel_pick in excel_picks:
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

    def load_week(self,year,week):
        # ensure players are loaded
        # ensure teams are loaded

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

        try:
            fbpool_api = FBPoolAPI(url=self.url)
            week = fbpool_api.createWeek(week_data)
        except FBAPIException as e:
            self.__load_error("week",e)

        self.__load_week_picks(excel,week,week_games)

    def load_year(self,year):
        excel = PoolSpreadsheet(year,self.__excel_full_path())
        week_numbers = excel.get_week_numbers()

        self.load_teams(year)
        self.load_players(year)

        for week_number in week_numbers:
            self.load_week(year,week_number)


    def __load_error(self,name,e):
        print "**ERROR** Encountered error when loading %s" % (name)
        print "---------------------------------------------"
        print "FBAPIException: code=%d, msg=%s" % (e.http_code,e.errmsg)
        print "Database data may be in an invalid state."
        print ""
        sys.exit(1)

    def __remove_remote(self,name):
        return string.replace(name,"Remote","").strip()


if __name__ == "__main__":

    fbpool_args = FBPoolArgs()
    url = fbpool_args.get_url()
    args = fbpool_args.get_args()
    action = fbpool_args.get_action()

    # TODO:  cleanup cache
    # TODO:  verbose option

    if action == "load_teams_most_recent_year":
        most_recent_year,excel_file = fbpool_args.get_latest_pool_file_and_year()
        fbpool = FBPool(url=url,excel_dir=args.excel_dir,excel_workbook=excel_file)
        fbpool.load_teams(most_recent_year)

    elif action == "load_teams_in_year":
        excel_file = fbpool_args.get_excel_file(args.year)
        fbpool = FBPool(url=url,excel_dir=args.excel_dir,excel_workbook=excel_file)
        fbpool.load_teams(args.year)

    elif action == "load_players_in_year":
        excel_file = fbpool_args.get_excel_file(args.year)
        fbpool = FBPool(url=url,excel_dir=args.excel_dir,excel_workbook=excel_file)
        fbpool.load_players(args.year)

    elif action == "load_players_all_years":
        excel_files = fbpool_args.get_excel_files()
        for year in excel_files:
            fbpool = FBPool(url=url,excel_dir=args.excel_dir,excel_workbook=excel_files[year])
            fbpool.load_players(year)

    elif action == "load_week":
        excel_file = fbpool_args.get_excel_file(args.year)
        fbpool = FBPool(url=url,excel_dir=args.excel_dir,excel_workbook=excel_file)
        fbpool.load_week(args.year,args.week)

    elif action == "load_year":
        excel_file = fbpool_args.get_excel_file(args.year)
        fbpool = FBPool(url=url,excel_dir=args.excel_dir,excel_workbook=excel_file)
        fbpool.load_year(args.year)

