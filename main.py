#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import cgitb; cgitb.enable()
from utils.utils import is_debug
from models.games import *
from models.players import *
from models.teams import *
from models.weeks import *
from models.picks import *
from load.load import *
from load.delete_page import *
from load.load_page import *
from load.stats_page import *
from load.load_all_page import *
from code.update import *
from pages.test_page import *
from google.appengine.api import taskqueue
from google.appengine.ext import db

class MainHandler(webapp2.RequestHandler):

    def get(self):
        if is_debug():
            self.response.write('***DEVELOPMENT SERVER***')
        self.response.write('Main Page')
        return


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/a/tests', MainTestPage),
    ('/a/delete', DeleteDatabase),
    ('/a/delete_players', DeletePlayers),
    ('/a/delete_teams', DeleteTeams),
    ('/a/delete_games', DeleteGames),
    ('/a/delete_weeks', DeleteWeeks),
    ('/a/delete_picks', DeletePicks),
    ('/a/delete_lookups', DeleteLookups),
    ('/a/load', LoadPage),
    ('/a/loadall', LoadEveryThingPage),
    ('/a/load_players', LoadPlayersPage),
    ('/a/load_teams', LoadTeamsPage),
    ('/a/load_games', LoadGamesPage),
    ('/a/load_weeks', LoadWeeksPage),
    ('/a/load_picks', LoadPicksPage)
    #('/a/stats', DatabaseStats)
], debug=True)
