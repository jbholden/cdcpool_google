from google.appengine.ext import db
from google.appengine.api import memcache
import logging
from models.teams import *
from models.picks import *
from api_exception import *
from database import *

class API:

    def create_team(self,name,conference):
        d = Database()
        team_names = d.load_teams("teamkeys").keys()

        if name in team_names:
            raise APIException(409,"team already exists")
            return

        team = Team(name=name,conference=conference)
        team.put()
        d.add_team_to_memcache(team)
        return team

    def delete_team(self,name):
        d = Database()
        teams = d.load_teams("teamkeys")

        if name not in teams:
            raise APIException(404,"could not find the team")
            return

        team = db.get(teams[name])
        db.delete(team)

        d.delete_team_from_memcache(team)

    def delete_team_by_id(self,team_id):
        try:
            team_key = db.Key.from_path('Team',team_id)
        except:
            raise APIException(500,"exception when getting key")
            return
        self.delete_team_by_key(str(team_key))

    def delete_team_by_key(self,team_key):
        d = Database()
        teams = d.load_teams("teams")

        if team_key not in teams:
            raise APIException(404,"could not find the team")
            return

        team = db.get(team_key)
        db.delete(team)

        d.delete_team_from_memcache(team)

    def delete_teams(self):
        d = Database()
        teams = d.load_teams("teams",update=True)

        for team_key in teams:
            team = db.get(team_key)
            db.delete(team)

        memcache.delete("teamkeys")
        memcache.delete("teams")

    def get_team(self,name):
        d = Database()
        teams = d.load_teams("teamkeys")

        if name not in teams:
            raise APIException(404,"could not find the team")
            return

        # TODO:  read from memcache instead?
        team = db.get(teams[name])
        return team

    def get_team_by_key(self,team_key):
        d = Database()
        teams = d.load_teams("teams")

        if team_key not in teams:
            raise APIException(404,"could not find the team")
            return

        team = db.get(team_key)
        return team

    def get_team_by_id(self,team_id):
        try:
            team_key = db.Key.from_path('Team',team_id)
        except:
            raise APIException(500,"exception when getting key")
            return
        return self.get_team_by_key(str(team_key))

    def get_teams(self):
        d = Database()
        teams = d.load_teams("teams").values()
        return teams

    def create_game(self,data):
        game = Game()
        game.number = data['number']
        game.team1 = data['team1']
        game.team2 = data['team2']
        game.team1_score = data['team1_score']
        game.team2_score = data['team2_score']
        game.favored = data['favored']
        game.spread = data['spread']
        game.state = data['state']
        game.quarter = data['quarter']
        game.time_left = data['time_left']
        game.date = data['date']

        game.put()

        # store temporarily in memcache for subsequent get calls
        # once done with API calls, can delete this with DELETE /api/games/cache
        self.__add_to_memcache_dict("games_id",game.key().id(),game)
        self.__add_to_memcache_dict("games_key",str(game.key()),game)

        return game

    def delete_game_by_id(self,game_id):
        try:
            game_key = db.Key.from_path('Game',game_id)
        except:
            raise APIException(500,"exception when getting key")
            return
        self.delete_game_by_key(str(game_key))


    def delete_game_by_key(self,game_key):
        game = db.get(game_key)
        game_id = game.key().id()
        db.delete(game)
        self.__delete_from_memcache_dict("games_id",game_id)
        self.__delete_from_memcache_dict("games_key",game_key)

    def get_game_by_key(self,game_key):
        games = memcache.get("games_key")
        if games != None and game_key in games:
            return games[game_key]

        game = db.get(game_key)
        if game == None:
            raise APIException(404,"could not find the game")
            return

        return game

    def get_game_by_id(self,game_id):
        games = memcache.get("games_id")
        if games != None and game_id in games:
            return games[game_id]

        try:
            game_key = db.Key.from_path('Game',game_id)
        except:
            raise APIException(500,"exception when getting key")
            return
        return self.get_game_by_key(str(game_key))

    def delete_games(self):
        games_query = db.GqlQuery('select * from Game')
        if games_query != None:
            for game in games_query:
                db.delete(game)

        memcache.delete("games_key")
        memcache.delete("games_id")

        # TODO:  weekly games still in memcache?

    def get_games(self):
        games_query = db.GqlQuery('select * from Game')
        if games_query == None:
            return []
        results = list(games_query)
        return [ result for result in results ]

    def edit_game_by_id(self,game_id,data):
        try:
            game_key = db.Key.from_path('Game',game_id)
        except:
            raise APIException(500,"exception when getting key")
            return
        self.edit_game_by_key(str(game_key),data)

    def edit_game_by_key(self,game_key,data):
        cache_data = memcache.get("games_key")
        if cache_data and game_key in cache_data:
            game = cache_data[game_key]
        else:
            game = db.get(game_key)

        if 'number' in data:
            game.number = data['number']

        if 'team1' in data:
            game.team1 = data['team1']

        if 'team2' in data:
            game.team2 = data['team2']

        if 'team1_score' in data:
            game.team1_score = data['team1_score']

        if 'team2_score' in data:
            game.team2_score = data['team2_score']

        if 'favored' in data:
            game.favored = data['favored']

        if 'spread' in data:
            game.spread = data['spread']

        if 'state' in data:
            game.state = data['state']

        if 'quarter' in data:
            game.quarter = data['quarter']

        if 'time_left' in data:
            game.time_left = data['time_left']

        if 'date' in data:
            game.date = data['date']

        game.put()

        game_id = game.key().id()

        self.__delete_from_memcache_dict("games_id",game_id)
        self.__delete_from_memcache_dict("games_key",game_key)
        self.__add_to_memcache_dict("games_id",game_id,game)
        self.__add_to_memcache_dict("games_key",game_key,game)

    def delete_games_cache(self):
        memcache.delete("games_key")
        memcache.delete("games_id")

    def delete_players_cache(self):
        memcache.delete("players")

    def create_player(self,name,years):
        players = self.__load_players_in_memcache()

        for player in players.values():
            if player.name == name:
                raise APIException(409,"player already exists")
                return

        player = Player(name=name,years=years)
        player.put()

        self.__add_to_memcache_dict("players",player.key().id(),player)
        return player


    def delete_player(self,name):
        player = self.__find_player_in_memcache(name)
        if player != None:
            player_key = player.key()
            player_obj = db.get(player_key)
        else:
            player_obj = self.__find_player_in_database(name)
            if player_obj:
                player_key = player_obj.key()

        if player_obj == None:
            raise APIException(404,"could not find the player")
            return

        db.delete(player_obj)
        self.__delete_from_memcache_dict("players",player_key)

    def delete_player_by_id(self,player_id):
        try:
            player_key = db.Key.from_path('Player',player_id)
        except:
            raise APIException(500,"exception when getting key")
            return
        self.delete_player_by_key(str(player_key))

    def delete_player_by_key(self,player_key):
        player = db.get(player_key)
        if player == None:
            raise APIException(404,"could not find the player")
            return

        db.delete(player)
        self.__delete_from_memcache_dict("players",player_key)

    def delete_players(self):
        players_query = db.GqlQuery('select * from Player')
        if players_query != None:
            for player in players_query:
                db.delete(player)

        memcache.delete("players")

    def get_players(self):
        players_by_key = self.__load_players_in_memcache()
        return players_by_key.values()

    def get_players_in_year(self,year):
        players_by_key = self.__load_players_in_memcache()
        players_in_year = [ player for player in players_by_key.values() if year in player.years]
        return players_in_year

    def get_player(self,name):
        # see if player is in memcache
        player = self.__find_player_in_memcache(name)
        if player:
            return player

        # now check if is in database
        players = self.__load_players_in_memcache()
        player = self.__find_player_in_memcache(name)
        if player:
            return player

        raise APIException(404,"could not find the player")
        return

    def get_player_by_key(self,player_key):
        # try memcache first
        players = memcache.get("players")
        if player_key in players:
            return players[player_key]

        # next try the database
        players = self.__load_players_in_memcache()
        if player_key in players:
            return players[player_key]

        raise APIException(404,"could not find the player")
        return

    def get_player_by_id(self,player_id):
        try:
            player_key = db.Key.from_path('Player',player_id)
        except:
            raise APIException(500,"exception when getting key")
            return
        return self.get_player_by_key(str(player_key))

    def edit_player_by_id(self,player_id,data):
        try:
            player_key = db.Key.from_path('Player',player_id)
        except:
            raise APIException(500,"exception when getting key")
            return
        self.edit_player_by_key(str(player_key),data)

    def edit_player_by_key(self,player_key,data):
        cache_data = memcache.get("players")
        if cache_data and player_key in cache_data:
            player = cache_data[player_key]
        else:
            player = db.get(player_key)

        if player == None:
            raise APIException(404,"could not find the player")
            return

        if 'name' in data:
            existing_name = self.__find_player_in_database(data['name'])
            if existing_name != None:
                raise APIException(409,"player already exists")
                return
            player.name = data['name']

        if 'years' in data:
            player.years = data['years']

        player.put()

        self.__delete_from_memcache_dict("players",player_key)
        self.__add_to_memcache_dict("players",player_key,player)

    def delete_week_by_id(self,week_id):
        try:
            week_key = db.Key.from_path('Week',week_id)
        except:
            raise APIException(500,"exception when getting key")
            return
        self.delete_week_by_key(str(week_key))

    def delete_week_by_key(self,week_key):
        week = db.get(week_key)
        if week == None:
            raise APIException(404,"could not find week")
            return

        db.delete(week)

        # update memcache
        d = Database()
        tmp = d.load_weeks_and_years(update=True)
        tmp = d.load_week(week.year,week.number)

    def delete_week(self,year,number):
        if not self.__does_week_exist(year,number):
            raise APIException(404,"could not find the week")
            return

        d = Database()
        cached_week = d.load_week(year,number)

        week = db.get(str(cached_week.key()))
        db.delete(week)

        # update memcache
        tmp = d.load_weeks_and_years(update=True)
        tmp = d.load_week(year,number)

    def __add_to_memcache_dict(self,key,dict_key,dict_value):
        data = memcache.get(key)
        if not(data):
            data = dict()
        data[dict_key] = dict_value
        memcache.set(key,data)

    def __delete_from_memcache_dict(self,key,dict_key):
        data = memcache.get(key)
        if data != None and dict_key in data:
            del data[dict_key]
            memcache.set(key,data)

    def __load_players_in_memcache(self):
        players = dict()
        players_query = db.GqlQuery('select * from Player')
        if players_query != None:
            players = {str(player.key()):player for player in players_query}
        memcache.set("players",players)
        return players

    def __find_player_in_memcache(self,name):
        players = memcache.get("players")
        if players == None:
            return
        players_with_name = [player for player in players.values() if player.name == name]
        if len(players_with_name) > 1:
            raise APIException(500,"Found multiple players with the same name")
        if len(players_with_name) == 1:
            return players_with_name[0]
        return None

    def __find_player_in_database(self,name):
        players_query = db.GqlQuery('select * from Player')
        if players_query != None:
            for player in players_query:
                if player.name == name:
                    return player
        return None

    def create_week(self,data):
        if self.__does_week_exist(data['year'],data['number']):
            raise APIException(409,"week already exists")
            return

        week = Week(year=data['year'],number=data['number'])
        week.winner = data['winner']
        week.lock_picks = data['lock_picks']
        week.lock_scores = data['lock_scores']

        if data['games'] == None:
            week.games = None
        else:
            week.games = [db.Key(game_key) for game_key in data['games'] ]

        week.put()

        # update the memcache
        d = Database()
        tmp = d.load_weeks_and_years(update=True)
        tmp = d.load_week(week.year,week.number,update=True)

        return week

    def __does_week_exist(self,year,week_number):
        d = Database()
        weeks_and_years = d.load_weeks_and_years()
        return year in weeks_and_years and week_number in weeks_and_years[year]

    def get_week_by_key(self,week_key):
        week = db.get(week_key)
        if week == None:
            raise APIException(404,"could not find week")
            return
        return week

    def get_week_by_id(self,week_id):
        try:
            week_key = db.Key.from_path('Week',week_id)
        except:
            raise APIException(500,"exception when getting key")
            return
        return self.get_week_by_key(str(week_key))

    def get_weeks(self):
        d = Database()
        weeks_and_years = d.load_weeks_and_years(update=True)
        weeks = []
        for year in weeks_and_years:
            week_numbers = weeks_and_years[year]
            weeks += [d.load_week(year,number) for number in week_numbers]
        return weeks

    def delete_weeks(self):
        d = Database()
        weeks_and_years = d.load_weeks_and_years(update=True)

        weeks_query = db.GqlQuery('select * from Week')
        if weeks_query != None:
            for week in weeks_query:
                db.delete(week)

        memcache.delete("weeks_and_years")
        for year in weeks_and_years:
            week_numbers = weeks_and_years[year]
            for number in week_numbers:
                memcache.delete("week_%d_%d" % (year,number))

    def get_weeks_in_year(self,year):
        d = Database()
        weeks_and_years = d.load_weeks_and_years(update=True)

        if year not in weeks_and_years:
            raise APIException(404,"could not find any weeks in year")
            return

        weeks = []
        week_numbers = weeks_and_years[year]
        weeks += [d.load_week(year,number) for number in week_numbers]
        return weeks

    def get_week_in_year(self,year,number):
        d = Database()
        weeks_and_years = d.load_weeks_and_years(update=True)

        if year not in weeks_and_years:
            raise APIException(404,"could not find week in year")
            return

        if number not in weeks_and_years[year]:
            raise APIException(404,"could not find week in year")
            return

        return d.load_week(year,number)

    def edit_week_by_id(self,week_id,data):
        try:
            week_key = db.Key.from_path('Week',week_id)
        except:
            raise APIException(500,"exception when getting key")
            return
        self.edit_week_by_key(str(week_key),data)


    def edit_week_by_key(self,week_key,data):
        d = Database()
        weeks_and_years = d.load_weeks_and_years(update=True)

        week = db.get(week_key)

        if 'year' in data:
            changed_year = True
            week.year = data['year']

        if 'number' in data:
            changed_number = True
            week.number = data['number']

        if changed_year or changed_number:
            if self.__does_week_exist(week.year,week.number):
                raise APIException(409,"week already exists")
                return

        if 'winner' in data:
            week.winner = data['winner']

        if 'lock_picks' in data:
            week.lock_picks = data['lock_picks']

        if 'lock_scores' in data:
            week.lock_scores = data['lock_scores']

        if 'games' in data:
            if data['games'] == None:
                week.games = None
            else:
                week.games = [db.Key(game_key) for game_key in data['games'] ]

        week.put()

        # update memcache
        tmp = d.load_weeks_and_years(update=True)
        tmp = d.load_week(week.year,week.number,update=True)


    def create_pick(self,data):
        pick = Pick()
        pick.week = data['week']
        pick.player = data['player']
        pick.game = data['game']
        pick.winner = data['winner']
        pick.team1_score = data['team1_score']
        pick.team2_score = data['team2_score']

        pick.put()

        # store temporarily in memcache for subsequent get calls
        # once done with API calls, can delete this with DELETE /api/picks/cache
        self.__add_to_memcache_dict("picks_id",pick.key().id(),pick)
        self.__add_to_memcache_dict("picks_key",str(pick.key()),pick)

        return pick

    def delete_pick_by_id(self,pick_id):
        try:
            pick_key = db.Key.from_path('Pick',pick_id)
        except:
            raise APIException(500,"exception when getting key")
            return
        self.delete_pick_by_key(str(pick_key))


    def delete_pick_by_key(self,pick_key):
        pick = db.get(pick_key)
        pick_id = pick.key().id()
        db.delete(pick)
        self.__delete_from_memcache_dict("picks_id",pick_id)
        self.__delete_from_memcache_dict("picks_key",pick_key)

    def delete_picks(self):
        picks_query = db.GqlQuery('select * from Pick')
        if picks_query != None:
            for pick in picks_query:
                db.delete(pick)

        memcache.delete("picks_key")
        memcache.delete("picks_id")

