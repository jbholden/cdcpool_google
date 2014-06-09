import webapp2
import logging
import json
from pages.api.api_handler import *
from models.weeks import *
from code.api import *
from code.api_exception import *

class WeekAPIGetDeleteAll(APIHandler):

    def get(self):
        try:
            api = API()
            weeks = api.get_weeks()
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

        data = [ self.build_week_object(week) for week in weeks ]
        self.render_json(data)

    def delete(self):
        try:
            api = API()
            api.delete_weeks()
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

class WeekAPIGetById(APIHandler):

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

class WeekAPIGetByKey(APIHandler):

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

class WeekAPIGetInYear(APIHandler):

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

class WeekAPIGetWeekInYear(APIHandler):

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
class WeekAPICreateEditDelete(APIHandler):

    # this creates a new week
    def post(self):
        data = json.loads(self.request.body) 

        required_fields = ['year','number','winner','games','lock_picks','lock_scores']

        for field in required_fields:
            if self.is_field_missing(field,data):
                return

        if data['lock_picks'] != None:
            data['lock_picks'] = self.convert_to_datetime(data['lock_picks'])

        if data['lock_scores'] != None:
            data['lock_scores'] = self.convert_to_datetime(data['lock_scores'])

        try:
            api = API()
            week = api.create_week(data)
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

        return_data = self.build_week_object(week)
        self.render_json(return_data)

    # this deletes a week object
    def delete(self):
        data = json.loads(self.request.body) 

        num_params = 0
        if 'id' in data: 
            num_params += 1
        if 'key' in data: 
            num_params += 1
        if 'year' in data and 'number' in data: 
            num_params += 1

        if num_params != 1:
            self.error(400) 
            self.write("only one parameter should be defined to find the week")
            return 

        try:
            api = API()
            if 'key' in data:
                api.delete_week_by_key(data['key'])
            elif 'id' in data:
                api.delete_week_by_id(data['id'])
            elif 'year' in data and 'number' in data:
                api.delete_week(data['year'],data['number'])
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
class WeekAPIDeleteCache(APIHandler):

    def delete(self):
        try:
            api = API()
            api.delete_players_cache()
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return
