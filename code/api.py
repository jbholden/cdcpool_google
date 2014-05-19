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

        team = Team(name=name,conference=conference)
        team.put()
        d.add_team_to_memcache(team)
        return team
