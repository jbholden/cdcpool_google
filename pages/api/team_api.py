import webapp2
import logging
import json
from pages.api.api_handler import *
from models.teams import *
from code.api import *
from code.api_exception import *

class TeamAPIGetDeleteAll(APIHandler):

    def get(self):
        try:
            api = API()
            teams = api.get_teams()
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

        data = [ self.build_team_object(team) for team in teams ]
        self.render_json(data)

    def delete(self):
        try:
            api = API()
            api.delete_teams()
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

class TeamAPIGetByName(APIHandler):

    def get(self,team_name):
        try:
            api = API()
            team = api.get_team(team_name)
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

        data = self.build_team_object(team)
        self.render_json(data)

class TeamAPIGetById(APIHandler):

    def get(self,team_id):
        try:
            api = API()
            team = api.get_team_by_id(int(team_id))
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

        data = self.build_team_object(team)
        self.render_json(data)

class TeamAPIGetByKey(APIHandler):

    def get(self,team_key):
        try:
            api = API()
            team = api.get_team_by_key(team_key)
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

        data = self.build_team_object(team)
        self.render_json(data)


class TeamAPICreateDelete(APIHandler):

    # this creates a new team
    def post(self):
        data = json.loads(self.request.body) 

        if 'name' not in data: 
            self.error(400) 
            self.write("name is missing") 
            return 

        if 'conference' not in data: 
            self.error(400) 
            self.write("conference is missing") 
            return 

        try:
            api = API()
            team = api.create_team(data['name'],data['conference'])
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

        return_data = self.build_team_object(team)
        self.render_json(return_data)

    # this deletes a team object
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
            self.write("only one parameter should be defined to find the team")
            return 

        try:
            api = API()
            if 'name' in data:
                team = api.delete_team(data['name'])
            elif 'key' in data:
                team = api.delete_team_by_key(data['key'])
            elif 'id' in data:
                team = api.delete_team_by_id(data['id'])
            else:
                raise AssertionError,"should not get here"

        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return


