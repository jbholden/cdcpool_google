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
from create.create_week import *
from pages.visual_test_page import *
from pages.week_results_json import *
from pages.player_results_json import *
from pages.overall_results_json import *
from pages.week_results_page import *
from pages.player_results_page import *
from pages.overall_results_page import *
from pages.update_games_page import *
from pages.api.team_api import *
from pages.api.game_api import *
from pages.api.week_api import *
from pages.api.pick_api import *
from pages.api.player_api import *
from pages.api.cache_api import *
from google.appengine.api import taskqueue
from google.appengine.ext import db

# app.yaml configuration link:  https://developers.google.com/appengine/docs/python/config/appconfig

class MainHandler(webapp2.RequestHandler):

    def get(self):
        if is_debug():
            self.response.write('***DEVELOPMENT SERVER***')
        self.response.write('Main Page')
        return


app = webapp2.WSGIApplication([
    webapp2.Route(r'/', MainHandler),
    webapp2.Route(r'/<year_param:([0-9]+)>/week/<week_number_param:([0-9]+)>/player/<player_id_param:([0-9]+)>/results/json', PlayerResultsJson),
    webapp2.Route(r'/<year_param:([0-9]+)>/week/<week_number_param:([0-9]+)>/player/<player_id_param:([0-9]+)>/results', PlayerResultsPage),
    webapp2.Route(r'/<year_param:([0-9]+)>/week/<week_number_param:([0-9]+)>/results/json', WeekResultsJson),
    webapp2.Route(r'/<year_param:([0-9]+)>/week/<week_number_param:([0-9]+)>/results', WeekResultsPage),
    webapp2.Route(r'/<year_param:([0-9]+)>/week/<week_number_param:([0-9]+)>/games', UpdateGamesPage),
    webapp2.Route(r'/<year_param:([0-9]+)>/results/json', OverallResultsJson),
    webapp2.Route(r'/<year_param:([0-9]+)>/results', OverallResultsPage),
    webapp2.Route(r'/a/tests', MainTestPage),
    webapp2.Route(r'/a/visual_tests/setup', VisualSetupPage),
    webapp2.Route(r'/a/visual_tests/cleanup', VisualCleanupPage),
    webapp2.Route(r'/a/visual_tests', VisualTestPage),
    webapp2.Route(r'/a/delete', DeleteDatabase),
    webapp2.Route(r'/a/delete_players', DeletePlayers),
    webapp2.Route(r'/a/delete_teams', DeleteTeams),
    webapp2.Route(r'/a/delete_games', DeleteGames),
    webapp2.Route(r'/a/delete_weeks', DeleteWeeks),
    webapp2.Route(r'/a/delete_picks', DeletePicks),
    webapp2.Route(r'/a/delete_lookups', DeleteLookups),
    webapp2.Route(r'/a/load', LoadPage),
    webapp2.Route(r'/a/loadall', LoadEveryThingPage),
    webapp2.Route(r'/a/load_players', LoadPlayersPage),
    webapp2.Route(r'/a/load_teams', LoadTeamsPage),
    webapp2.Route(r'/a/load_games', LoadGamesPage),
    webapp2.Route(r'/a/load_weeks', LoadWeeksPage),
    webapp2.Route(r'/a/load_picks', LoadPicksPage),
    webapp2.Route(r'/a/create_week', CreateWeekPage),
    webapp2.Route(r'/api/team', TeamAPICreateDelete),
    webapp2.Route(r'/api/teams', TeamAPIGetDeleteAll),
    webapp2.Route(r'/api/team/name/<team_name>', TeamAPIGetByName),
    webapp2.Route(r'/api/team/id/<team_id:([0-9]+)>', TeamAPIGetById),
    webapp2.Route(r'/api/team/key/<team_key>', TeamAPIGetByKey),
    webapp2.Route(r'/api/game', GameAPICreateEditDelete),
    webapp2.Route(r'/api/games', GameAPIGetDeleteAll),
    webapp2.Route(r'/api/games/cache', GameAPIDeleteCache),
    webapp2.Route(r'/api/game/id/<game_id:([0-9]+)>', GameAPIGetById),
    webapp2.Route(r'/api/game/key/<game_key>', GameAPIGetByKey),
    webapp2.Route(r'/api/player', PlayerAPICreateEditDelete),
    webapp2.Route(r'/api/players', PlayerAPIGetDeleteAll),
    webapp2.Route(r'/api/players/cache', PlayerAPIDeleteCache),
    webapp2.Route(r'/api/players/year/<year:([0-9]+)>', PlayerAPIGetInYear),
    webapp2.Route(r'/api/player/name/<player_name>', PlayerAPIGetByName),
    webapp2.Route(r'/api/player/id/<player_id:([0-9]+)>', PlayerAPIGetById),
    webapp2.Route(r'/api/player/key/<player_key>', PlayerAPIGetByKey),
    webapp2.Route(r'/api/week', WeekAPICreateEditDelete),
    webapp2.Route(r'/api/weeks', WeekAPIGetDeleteAll),
    webapp2.Route(r'/api/weeks/year/<year:([0-9]+)>', WeekAPIGetInYear),
    webapp2.Route(r'/api/week/id/<week_id:([0-9]+)>', WeekAPIGetById),
    webapp2.Route(r'/api/week/key/<week_key>', WeekAPIGetByKey),
    webapp2.Route(r'/api/week/<week_number:([0-9]+)>/year/<year:([0-9]+)>', WeekAPIGetWeekInYear),
    webapp2.Route(r'/api/weeks/cache', WeekAPIDeleteCache),
    webapp2.Route(r'/api/pick', PickAPICreateEditDelete),
    webapp2.Route(r'/api/picks', PickAPIDeleteAll),
    webapp2.Route(r'/api/<year:([0-9]+)>/week/<week_number:([0-9]+)>/picks', PickAPIMultipleCreate),
    webapp2.Route(r'/api/pick/id/<pick_id:([0-9]+)>', PickAPIGetById),
    webapp2.Route(r'/api/pick/key/<pick_key>', PickAPIGetByKey),
    webapp2.Route(r'/api/picks/year/<year:([0-9]+)>/week/<week_number:([0-9]+)>', PickAPIGetWeekPicks),
    webapp2.Route(r'/api/picks/year/<year:([0-9]+)>/week/<week_number:([0-9]+)>/player/<name>', PickAPIGetPlayerPicks),
    webapp2.Route(r'/api/picks/cache', PickAPIDeleteCache),
    webapp2.Route(r'/api/cache', CacheAPILoadDelete),
    webapp2.Route(r'/api/cache/year/<year:([0-9]+)>', CacheAPILoadYear),
    webapp2.Route(r'/api/cache/year/<year:([0-9]+)>/week/<week_number:([0-9]+)>', CacheAPILoadWeek),
], debug=True)
