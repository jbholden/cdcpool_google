from pages.handler import *
from models.teams import *

class APIHandler(Handler):

    def build_team_object(self,team):
        t = dict()
        t['id'] = team.key().id()
        t['key'] = str(team.key())
        t['name'] = team.name
        t['conference'] = team.conference
        return t
