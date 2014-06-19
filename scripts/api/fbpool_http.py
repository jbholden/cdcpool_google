import urllib2
import urllib
import json
import logging

class FBPoolHTTP:

    def __init__(self,url='http://cdcpool.appspot.com'):
        self.url = url

    def __geturl(self,address):
        return "%s%s" % (self.url,address)

    def httpGet(self,address):
        try:
            req = urllib2.Request(self.__geturl(address))
            response = urllib2.urlopen(req)
        except urllib2.HTTPError,err:
            response = err
        return response

    def httpPost(self,address,data):
        headers = { 'Content-Type' : 'application/json; charset=UTF-8' }
        data_json = json.dumps(data)
        try:
            req = urllib2.Request(self.__geturl(address),data_json,headers)
            response = urllib2.urlopen(req)
        except urllib2.HTTPError,err:
            response = err
        return response

    def httpDelete(self,address,data=None):
        if data != None:
            headers = { 'Content-Type' : 'application/json; charset=UTF-8' }
            data_json = json.dumps(data)
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        try:
            if data != None:
                req = urllib2.Request(self.__geturl(address),data_json,headers)
            else:
                req = urllib2.Request(self.__geturl(address))
            req.get_method = lambda: 'DELETE'
            response = opener.open(req)
        except urllib2.HTTPError,err:
            response = err
        return response

    def httpPut(self,address,data):
        headers = { 'Content-Type' : 'application/json; charset=UTF-8' }
        data_json = json.dumps(data)
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        try:
            req = urllib2.Request(self.__geturl(address),data_json,headers)
            req.get_method = lambda: 'PUT'
            response = opener.open(req)
        except urllib2.HTTPError,err:
            response = err
        return response

    def httpPostTeamCreate(self,name,conference):
        data = dict()
        data['name'] = name
        data['conference'] = conference
        return self.httpPost('/api/team',data)

    def httpDeleteTeam(self,name):
        data = dict()
        data['name'] = name
        return self.httpDelete('/api/team',data)

    def httpDeleteTeamByKey(self,team_key):
        data = dict()
        data['key'] = team_key
        return self.httpDelete('/api/team',data)

    def httpDeleteTeamByID(self,team_id):
        data = dict()
        data['id'] = team_id
        return self.httpDelete('/api/team',data)

    def httpDeleteAllTeams(self):
        return self.httpDelete('/api/teams')

    def httpGetTeam(self,name):
        name_encoded = urllib.quote(name)
        return self.httpGet('/api/team/name/%s' % (name_encoded))

    def httpGetTeamByKey(self,team_key):
        return self.httpGet('/api/team/key/%s' % (team_key))

    def httpGetTeamByID(self,team_id):
        return self.httpGet('/api/team/id/%d' % (team_id))

    def httpGetAllTeams(self):
        return self.httpGet('/api/teams')

    def httpPostGameCreate(self,data):
        return self.httpPost('/api/game',data)

    def httpDeleteGameByKey(self,game_key):
        data = dict()
        data['key'] = game_key
        return self.httpDelete('/api/game',data)

    def httpDeleteGameByID(self,game_id):
        data = dict()
        data['id'] = game_id
        return self.httpDelete('/api/game',data)

    def httpGetGameByID(self,game_id):
        return self.httpGet('/api/game/id/%d' % (game_id))

    def httpGetGameByKey(self,game_key):
        return self.httpGet('/api/game/key/%s' % (game_key))

    def httpDeleteAllGames(self):
        return self.httpDelete('/api/games')

    def httpGetAllGames(self):
        return self.httpGet('/api/games')

    def httpPutGameByKey(self,game_key,data):
        put_data = dict(data)
        put_data['key'] = game_key
        return self.httpPut('/api/game',put_data)

    def httpPutGameByID(self,game_id,data):
        put_data = dict(data)
        put_data['id'] = game_id
        return self.httpPut('/api/game',put_data)

    def httpDeleteGamesCache(self):
        return self.httpDelete('/api/games/cache')

    def httpDeletePlayersCache(self):
        return self.httpDelete('/api/players/cache')

    def httpDeleteWeeksCache(self):
        return self.httpDelete('/api/weeks/cache')

    def httpDeletePicksCache(self):
        return self.httpDelete('/api/picks/cache')

    def httpDeletePlayer(self,name):
        data = dict()
        data['name'] = name
        return self.httpDelete('/api/player',data)

    def httpDeletePlayerByKey(self,player_key):
        data = dict()
        data['key'] = player_key
        return self.httpDelete('/api/player',data)

    def httpDeletePlayerByID(self,player_id):
        data = dict()
        data['id'] = player_id
        return self.httpDelete('/api/player',data)

    def httpDeleteAllPlayers(self):
        return self.httpDelete('/api/players')

    def httpPostPlayerCreate(self,name,years):
        data = dict()
        data['name'] = name
        data['years'] = years
        return self.httpPost('/api/player',data)

    def httpGetPlayer(self,name):
        name_encoded = urllib.quote(name)
        return self.httpGet('/api/player/name/%s' % (name_encoded))

    def httpGetPlayerByKey(self,player_key):
        return self.httpGet('/api/player/key/%s' % (player_key))

    def httpGetPlayerByID(self,player_id):
        return self.httpGet('/api/player/id/%d' % (player_id))

    def httpGetAllPlayers(self):
        return self.httpGet('/api/players')

    def httpGetPlayersInYear(self,year):
        return self.httpGet('/api/players/year/%d' % (year))

    def httpPutPlayerByKey(self,player_key,data):
        put_data = dict(data)
        put_data['key'] = player_key
        return self.httpPut('/api/player',put_data)

    def httpPutPlayerByID(self,player_id,data):
        put_data = dict(data)
        put_data['id'] = player_id
        return self.httpPut('/api/player',put_data)

    def httpDeleteWeek(self,year,week_number):
        data = dict()
        data['year'] = year
        data['number'] = week_number
        return self.httpDelete('/api/week',data)

    def httpPostWeekCreate(self,data):
        return self.httpPost('/api/week',data)

    def httpDeleteWeekByKey(self,week_key):
        data = dict()
        data['key'] = week_key
        return self.httpDelete('/api/week',data)

    def httpDeleteWeekByID(self,week_id):
        data = dict()
        data['id'] = week_id
        return self.httpDelete('/api/week',data)

    def httpGetWeekByKey(self,week_key):
        return self.httpGet('/api/week/key/%s' % (week_key))

    def httpGetWeekByID(self,week_id):
        return self.httpGet('/api/week/id/%d' % (week_id))

    def httpDeleteAllWeeks(self):
        return self.httpDelete('/api/weeks')

    def httpGetAllWeeks(self):
        return self.httpGet('/api/weeks')

    def httpGetWeeksInYear(self,year):
        return self.httpGet('/api/weeks/year/%d' % (year))

    def httpGetWeek(self,year,week_number):
        return self.httpGet('/api/week/%d/year/%d' % (week_number,year))

    def httpPutWeekByKey(self,week_key,data):
        put_data = dict(data)
        put_data['key'] = week_key
        return self.httpPut('/api/week',put_data)

    def httpPutWeekByID(self,week_id,data):
        put_data = dict(data)
        put_data['id'] = week_id
        return self.httpPut('/api/week',put_data)

    def httpPostPickCreate(self,data):
        return self.httpPost('/api/pick',data)

    def httpGetPickByKey(self,pick_key):
        return self.httpGet('/api/pick/key/%s' % (pick_key))

    def httpGetPickByID(self,pick_id):
        return self.httpGet('/api/pick/id/%d' % (pick_id))

    def httpDeletePickByKey(self,pick_key):
        data = dict()
        data['key'] = pick_key
        return self.httpDelete('/api/pick',data)

    def httpDeletePickByID(self,pick_id):
        data = dict()
        data['id'] = pick_id
        return self.httpDelete('/api/pick',data)

    def httpGetWeekPicks(self,year,week_number):
        return self.httpGet('/api/picks/year/%d/week/%d' % (year,week_number))

    def httpGetPlayerPicks(self,year,week_number,player):
        name_encoded = urllib.quote(player)
        return self.httpGet('/api/picks/year/%d/week/%d/player/%s' % (year,week_number,name_encoded))

    def httpPutPickByKey(self,pick_key,data):
        put_data = dict(data)
        put_data['key'] = pick_key
        return self.httpPut('/api/pick',put_data)

    def httpPutPickByID(self,pick_id,data):
        put_data = dict(data)
        put_data['id'] = pick_id
        return self.httpPut('/api/pick',put_data)

    def httpDeleteAllPicks(self):
        return self.httpDelete('/api/picks')
