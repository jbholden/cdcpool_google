import webapp2
import logging
import json
from pages.api.api_handler import *
from models.games import *
from code.api import *
from code.api_exception import *

class GameAPIGetDeleteAll(APIHandler):

    def get(self):
        try:
            api = API()
            games = api.get_games()
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

        data = [ self.build_game_object(game) for game in games ]
        self.render_json(data)

    def delete(self):
        try:
            api = API()
            api.delete_games()
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

class GameAPIGetById(APIHandler):

    def get(self,game_id):
        try:
            api = API()
            game = api.get_game_by_id(int(game_id))
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

        data = self.build_game_object(game)
        self.render_json(data)

class GameAPIGetByKey(APIHandler):

    def get(self,game_key):
        try:
            api = API()
            game = api.get_game_by_key(game_key)
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

        data = self.build_game_object(game)
        self.render_json(data)


class GameAPICreateDelete(APIHandler):

    # this creates a new game
    def post(self):
        data = json.loads(self.request.body) 

        required_fields = ['number','team1','team2','team1_score','team2_score','favored','spread','state','quarter','time_left','date']

        for field in required_fields:
            if self.is_field_missing(field,data):
                return

        # change date format
        if data['date'] != None:
            data['date'] = self.convert_to_datetime(data['date'])

        try:
            api = API()
            game = api.create_game(data)
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

        return_data = self.build_game_object(game)
        self.render_json(return_data)

    # this deletes a game object
    def delete(self):
        data = json.loads(self.request.body) 

        num_params = 0
        if 'id' in data: 
            num_params += 1
        if 'key' in data: 
            num_params += 1

        if num_params != 1:
            self.error(400) 
            self.write("only one parameter should be defined to find the game")
            return 

        try:
            api = API()
            if 'key' in data:
                api.delete_game_by_key(data['key'])
            elif 'id' in data:
                api.delete_game_by_id(data['id'])
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

        if data['date'] != None:
            data['date'] = self.convert_to_datetime(data['date'])

        try:
            api = API()
            if 'key' in data:
                api.edit_game_by_key(data['key'],data)
            elif 'id' in data:
                api.edit_game_by_id(data['id'],data)
            else:
                raise AssertionError,"should not get here"

        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return


