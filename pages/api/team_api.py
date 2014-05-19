import webapp2
import logging
import json
from pages.api.api_handler import *
from models.teams import *
from code.api import *
from code.api_exception import *


class TeamAPIPage(APIHandler):

    def get(self):
        data = json.loads(self.request.body) 
             
        if 'name' not in data: 
            self.error(400) 
            self.write("user name is missing") 
            return 

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
