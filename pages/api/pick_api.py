import webapp2
import logging
import json
from pages.api.api_handler import *
from models.weeks import *
from code.api import *
from code.api_exception import *

class PickAPIDeleteAll(APIHandler):

    def delete(self):
        try:
            api = API()
            api.delete_picks()
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return


class PickAPIGetById(APIHandler):

    def get(self,pick_id):
        try:
            api = API()
            pick = api.get_pick_by_id(int(pick_id))
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

        data = self.build_pick_object(pick)
        self.render_json(data)


class PickAPIGetByKey(APIHandler):

    def get(self,pick_key):
        try:
            api = API()
            pick = api.get_pick_by_key(pick_key)
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

        data = self.build_pick_object(pick)
        self.render_json(data)


class PickAPIGetWeekPicks(APIHandler):

    def get(self,year,week_number):
        try:
            api = API()
            picks = api.get_week_picks(int(year),int(week_number))
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

        data = [ self.build_pick_object(pick) for pick in picks ]
        self.render_json(data)

class PickAPIGetPlayerPicks(APIHandler):

    def get(self,year,week_number,name):
        try:
            api = API()
            picks = api.get_player_week_picks(int(year),int(week_number),name)
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

        data = [ self.build_pick_object(pick) for pick in picks ]
        self.render_json(data)




class PickAPICreateEditDelete(APIHandler):

    # this creates a new pick
    def post(self):
        data = json.loads(self.request.body) 

        required_fields = ['week','player','game','winner','team1_score','team2_score']

        for field in required_fields:
            if self.is_field_missing(field,data):
                return

        try:
            api = API()
            pick = api.create_pick(data)
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

        return_data = self.build_pick_object(pick)
        self.render_json(return_data)

    # this deletes a pick object
    def delete(self):
        data = json.loads(self.request.body) 

        num_params = 0
        if 'id' in data: 
            num_params += 1
        if 'key' in data: 
            num_params += 1

        if num_params != 1:
            self.error(400) 
            self.write("only one parameter should be defined to find the pick")
            return 

        try:
            api = API()
            if 'key' in data:
                api.delete_pick_by_key(data['key'])
            elif 'id' in data:
                api.delete_pick_by_id(data['id'])
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
                api.edit_pick_by_key(data['key'],data)
            elif 'id' in data:
                api.edit_pick_by_id(data['id'],data)
            else:
                raise AssertionError,"should not get here"

        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

# TODO
class PickAPIDeleteCache(APIHandler):

    def delete(self):
        try:
            api = API()
            api.delete_players_cache()
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return
