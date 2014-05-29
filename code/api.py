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


