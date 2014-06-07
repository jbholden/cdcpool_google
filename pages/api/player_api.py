import webapp2
import logging
import json
from pages.api.api_handler import *
from models.games import *
from code.api import *
from code.api_exception import *

class PlayerAPIGetDeleteAll(APIHandler):

    def get(self):
        try:
            api = API()
            players = api.get_players()
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

        data = [ self.build_player_object(player) for player in players ]
        self.render_json(data)

    def delete(self):
        try:
            api = API()
            api.delete_players()
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

class PlayerAPIGetById(APIHandler):

    def get(self,player_id):
        try:
            api = API()
            player = api.get_player_by_id(int(player_id))
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

        data = self.build_player_object(player)
        self.render_json(data)

class PlayerAPIGetByKey(APIHandler):

    def get(self,player_key):
        try:
            api = API()
            player = api.get_player_by_key(player_key)
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

        data = self.build_player_object(player)
        self.render_json(data)

class PlayerAPIGetInYear(APIHandler):

    def get(self,year):
        try:
            api = API()
            players = api.get_players_in_year(int(year))
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

        data = [ self.build_player_object(player) for player in players ]
        self.render_json(data)


# TODO
class PlayerAPICreateEditDelete(APIHandler):

    # this creates a new player
    def post(self):
        data = json.loads(self.request.body) 

        required_fields = ['name','years']

        for field in required_fields:
            if self.is_field_missing(field,data):
                return

        try:
            api = API()
            player = api.create_player(data['name'],data['years'])
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

        return_data = self.build_player_object(player)
        self.render_json(return_data)

    # this deletes a player object
    def delete(self):
        data = json.loads(self.request.body) 

        num_params = 0
        if 'id' in data: 
            num_params += 1
        if 'key' in data: 
            num_params += 1
        if 'name' in data: 
            num_params += 1

        if num_params != 1:
            self.error(400) 
            self.write("only one parameter should be defined to find the player")
            return 

        try:
            api = API()
            if 'key' in data:
                api.delete_player_by_key(data['key'])
            elif 'id' in data:
                api.delete_player_by_id(data['id'])
            elif 'name' in data:
                api.delete_player(data['name'])
            else:
                raise AssertionError,"should not get here"

        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

    def put(self):
        data = json.loads(self.request.body) 

        num_params = 0
        if 'id' in data: 
            num_params += 1
        if 'key' in data: 
            num_params += 1

        if num_params != 1:
            self.error(400) 
            self.write("id or key must be passed in")
            return 

        try:
            api = API()
            if 'key' in data:
                api.edit_player_by_key(data['key'],data)
            elif 'id' in data:
                api.edit_player_by_id(data['id'],data)
            else:
                raise AssertionError,"should not get here"

        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

# TODO
class PlayerAPIDeleteCache(APIHandler):

    def delete(self):
        try:
            api = API()
            api.delete_games_cache()
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

class PlayerAPIGetByName(APIHandler):

    def get(self,player_name):
        try:
            api = API()
            player = api.get_player(player_name)
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

        data = self.build_player_object(player)
        self.render_json(data)
