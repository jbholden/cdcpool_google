from google.appengine.ext import db
from google.appengine.api import memcache
import logging
from models.teams import *
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

        db.delete(player)
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


