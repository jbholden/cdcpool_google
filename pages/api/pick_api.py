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

#TODO
class PickAPIGetById(APIHandler):

    def get(self,week_id):
        try:
            api = API()
            week = api.get_week_by_id(int(week_id))
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

        data = self.build_week_object(week)
        self.render_json(data)

#TODO
class PickAPIGetByKey(APIHandler):

    def get(self,week_key):
        try:
            api = API()
            week = api.get_week_by_key(week_key)
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

        data = self.build_week_object(week)
        self.render_json(data)

#TODO
class PickAPIGetInYear(APIHandler):

    def get(self,year):
        try:
            api = API()
            weeks = api.get_weeks_in_year(int(year))
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

        data = [ self.build_week_object(week) for week in weeks ]
        self.render_json(data)

#TODO
class PickAPIGetWeekInYear(APIHandler):

    def get(self,week_number,year):
        try:
            api = API()
            week = api.get_week_in_year(int(year),int(week_number))
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

        data = self.build_week_object(week)
        self.render_json(data)



# TODO
class PickAPICreateEditDelete(APIHandler):

    # this creates a new week
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

        if 'lock_picks' in data and data['lock_picks'] != None:
            data['lock_picks'] = self.convert_to_datetime(data['lock_picks'])

        if 'lock_scores' in data and data['lock_scores'] != None:
            data['lock_scores'] = self.convert_to_datetime(data['lock_scores'])

        try:
            api = API()
            if 'key' in data:
                api.edit_week_by_key(data['key'],data)
            elif 'id' in data:
                api.edit_week_by_id(data['id'],data)
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
