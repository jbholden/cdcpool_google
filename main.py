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
from models.games import *
from models.players import *
from models.teams import *
from models.weeks import *
from models.picks import *
from load.load import *
from load.delete_page import *
from load.load_page import *
from load.stats_page import *
from code.update import *
from pages.test_page import *
from google.appengine.api import taskqueue
from google.appengine.ext import db

class MainHandler(webapp2.RequestHandler):

    def get(self):
        self.response.write('Main Page')
        return

# run a worker to get around request timeout in 30 seconds.
class LoadDatabasePage(webapp2.RequestHandler):
    def get(self):
        taskqueue.add(url='/worker')
        self.response.write('Running worker')

class Worker(webapp2.RequestHandler):
    def __load_player(self):
        p = Player(name="Brent",year=2013)
        p.put()

    def post(self):
        load = LoadDatabase()
        load.load_players()
        #self.__load_player()
        #load = LoadDatabase()
        #load.load_players()
        #def txn():
            #load = LoadDatabase()
            #load.load_players()
            #load.load_all()
        #db.run_in_transaction(txn)

class Purge(webapp2.RequestHandler):
    def get(self):
        q = taskqueue.Queue('default')
        q.purge()
        self.response.write('Taskqueue Purged.')

class TaskqueueStatus(webapp2.RequestHandler):
    def get(self):
        players = Player.all()
        if not(players):
            self.response.write('Players loaded=0.')
        else:
            self.response.write('Players loaded=%d' % (players.count()))

class LoadPlayersTest(webapp2.RequestHandler):
    def get(self):
        index = self.request.get('index')
        batch = self.request.get('batch_size')

        if not(index):
            start_index = 0
        else:
            start_index = int(index)

        if not(batch):
            batch_size = 1
        else:
            batch_size = int(batch)

        load_all = not(index) and not(batch)
        end_index = start_index + batch_size

        if load_all:
            load = LoadDatabase()
            done = load.load_players()
        else:
            load = LoadDatabase()
            done = load.load_players(start_index,batch_size)

        finished = done == "done"

        if finished:
            self.response.write('Finished loading players.')
        else:
            code = "<form type='post'>"
            code += "<input type='hidden' name='index' value='%s'>" % (end_index)
            code += "<input type='hidden' name='batch_size' value='%s'>" % (batch_size)
            code += "Load Next Batch&nbsp;"
            code += "<input type='submit' value='next'>"
            code += "</form>"
            self.response.write(code)
            #rs = '/loadplayers?index=%d&batch_size=%d' % (end_index,batch_size)
            #self.response.write('Redirect: %s' % (rs))

    def post(self):
        self.response.write('Redirecting...')
        index = self.request.get("index")
        batch_size = self.request.get("batch_size")
        self.redirect('/loadplayers?index=%s&batch_size=%s' % (index,batch_size))

class DatabaseTest(webapp2.RequestHandler):

    def __week_str(self,week):
        s = ''
        s += 'year=%d<br>' % (week.year)
        s += 'number=%d<br>' % (week.number)
        s += 'winner=%s<br>' % (week.winner.name)
        s += 'games=%s<br>' % (week.games)
        return s

    def __game_str(self,game):
        s = ''
        s += 'game.number=%d<br>' % (game.number)
        s += 'game.away_team=%s<br>' % (game.away_team.name)
        s += 'game.home_team=%s<br>' % (game.home_team.name)
        return s

    def __pick_str(self,pick):
        s = ''
        s += 'pick.week.number=%d<br>' % (pick.week.number)
        s += 'pick.week.year=%d<br>' % (pick.week.year)
        s += 'pick.player.name=%s<br>' % (pick.player.name)
        return s

    def get(self):
        u = Update()
        week,games,picks = u.run_test()

        week_str = self.__week_str(week)
        game_str = ''
        for g in games:
            game_str += self.__game_str(g)

        #pick_str = self.__pick_str(picks[0])

        self.response.write('Test Complete<br>week:<br>%s<br>games<br>%s<br>picks<br>%s<br>'%(week_str,game_str,picks))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    #('/delete', DeleteDatabase),
    ('/dbtest',DatabaseTest),
    ('/load', LoadDatabasePage),
    ('/worker', Worker),
    ('/purge', Purge),
    ('/status', TaskqueueStatus),
    ('/loadplayers', LoadPlayersTest),
    ('/a/tests', MainTestPage),
    ('/a/delete', DeleteDatabase),
    ('/a/delete_players', DeletePlayers),
    ('/a/delete_teams', DeleteTeams),
    ('/a/delete_games', DeleteGames),
    ('/a/delete_weeks', DeleteWeeks),
    ('/a/delete_picks', DeletePicks),
    ('/a/delete_lookups', DeleteLookups),
    ('/a/load', LoadAllPage),
    ('/a/load_players', LoadPlayersPage),
    ('/a/load_teams', LoadTeamsPage),
    ('/a/load_games', LoadGamesPage),
    ('/a/load_weeks', LoadWeeksPage),
    ('/a/load_picks', LoadPicksPage),
    ('/a/stats', DatabaseStats)
], debug=True)
