import urllib2
import urllib
import json
from fbpool_http import *
from fbpool_api_exception import *

class FBPoolAPI:

    def __init__(self,url='http://localhost:10090'):
        self.__fbpool = FBPoolHTTP(url) 

    def createTeam(self,name,conference):
        response = self.__fbpool.httpPostTeamCreate(name,conference)
        if response.code == 200:
            data = json.loads(response.read())
            return data
        raise FBAPIException(response.code,response.read())

    def deleteTeam(self,name):
        response = self.__fbpool.httpDeleteTeam(name)
        if response.code != 200:
            raise FBAPIException(response.code,response.read())

    def deleteTeamByKey(self,team_key):
        response = self.__fbpool.httpDeleteTeamByKey(team_key)
        if response.code != 200:
            raise FBAPIException(response.code,response.read())

    def deleteTeamByID(self,team_id):
        response = self.__fbpool.httpDeleteTeamByID(team_id)
        if response.code != 200:
            raise FBAPIException(response.code,response.read())

    def getTeam(self,name):
        response = self.__fbpool.httpGetTeam(name)
        if response.code != 200:
            raise FBAPIException(response.code,response.read())
        data = json.loads(response.read())
        return data

    def getTeamByKey(self,team_key):
        response = self.__fbpool.httpGetTeamByKey(team_key)
        if response.code != 200:
            raise FBAPIException(response.code,response.read())
        data = json.loads(response.read())
        return data

    def getTeamByID(self,team_id):
        response = self.__fbpool.httpGetTeamByID(team_id)
        if response.code != 200:
            raise FBAPIException(response.code,response.read())
        data = json.loads(response.read())
        return data

    def getAllTeams(self):
        response = self.__fbpool.httpGetAllTeams()
        if response.code != 200:
            raise FBAPIException(response.code,response.read())
        data = json.loads(response.read())
        return data

    def deleteAllTeams(self):
        response = self.__fbpool.httpDeleteAllTeams()
        if response.code != 200:
            raise FBAPIException(response.code,response.read())

    def deleteTeamIfExists(self,name):
        try:
            self.deleteTeam(name)
        except FBAPIException as e:
            if e.http_code == 404 and e.errmsg == "could not find the team":
                return
            raise FBAPIException(e.http_code,e.errmsg)

    def createTeamIfDoesNotExist(self,name,conference):
        try:
            team = self.createTeam(name,conference)
        except FBAPIException as e:
            if e.http_code == 409 and e.errmsg == "team already exists":
                team = self.getTeam(name)
                return team
            raise FBAPIException(e.http_code,e.errmsg)
        return team

    def addTeam(self,name,conference):
        pass

    def createTeams(self):
        pass

    def createGame(self,data):
        response = self.__fbpool.httpPostGameCreate(data)
        if response.code == 200:
            data = json.loads(response.read())
            return data
        raise FBAPIException(response.code,response.read())

    def deleteGameByKey(self,game_key):
        response = self.__fbpool.httpDeleteGameByKey(game_key)
        if response.code != 200:
            raise FBAPIException(response.code,response.read())

    def deleteGameByID(self,game_id):
        response = self.__fbpool.httpDeleteGameByID(game_id)
        if response.code != 200:
            raise FBAPIException(response.code,response.read())

    def getGameByKey(self,game_key):
        response = self.__fbpool.httpGetGameByKey(game_key)
        if response.code != 200:
            raise FBAPIException(response.code,response.read())
        data = json.loads(response.read())
        return data

    def getGameByID(self,game_id):
        response = self.__fbpool.httpGetGameByID(game_id)
        if response.code != 200:
            raise FBAPIException(response.code,response.read())
        data = json.loads(response.read())
        return data

    def deleteAllGames(self):
        response = self.__fbpool.httpDeleteAllGames()
        if response.code != 200:
            raise FBAPIException(response.code,response.read())

    def getAllGames(self):
        response = self.__fbpool.httpGetAllGames()
        if response.code != 200:
            raise FBAPIException(response.code,response.read())
        data = json.loads(response.read())
        return data

    def editGameByKey(self,game_key,data):
        response = self.__fbpool.httpPutGameByKey(game_key,data)
        if response.code != 200:
            raise FBAPIException(response.code,response.read())

    def editGameByID(self,game_id,data):
        response = self.__fbpool.httpPutGameByID(game_id,data)
        if response.code != 200:
            raise FBAPIException(response.code,response.read())

    def deleteGamesCache(self):
        response = self.__fbpool.httpDeleteGamesCache()
        if response.code != 200:
            raise FBAPIException(response.code,response.read())

    def deletePlayersCache(self):
        response = self.__fbpool.httpDeletePlayersCache()
        if response.code != 200:
            raise FBAPIException(response.code,response.read())

    def deletePlayerIfExists(self,name):
        try:
            self.deletePlayer(name)
        except FBAPIException as e:
            if e.http_code == 404 and e.errmsg == "could not find the player":
                return
            raise FBAPIException(e.http_code,e.errmsg)

    def deletePlayer(self,name):
        response = self.__fbpool.httpDeletePlayer(name)
        if response.code != 200:
            raise FBAPIException(response.code,response.read())

    def deletePlayerByKey(self,player_key):
        response = self.__fbpool.httpDeletePlayerByKey(player_key)
        if response.code != 200:
            raise FBAPIException(response.code,response.read())

    def deletePlayerByID(self,player_id):
        response = self.__fbpool.httpDeletePlayerByID(player_id)
        if response.code != 200:
            raise FBAPIException(response.code,response.read())

    def createPlayer(self,name,years):
        response = self.__fbpool.httpPostPlayerCreate(name,years)
        if response.code == 200:
            data = json.loads(response.read())
            return data
        raise FBAPIException(response.code,response.read())

    def createPlayerIfDoesNotExist(self,name,years):
        try:
            player = self.createPlayer(name,years)
        except FBAPIException as e:
            if e.http_code == 409 and e.errmsg == "player already exists":
                player = self.getPlayer(name)
                return player
            raise FBAPIException(e.http_code,e.errmsg)
        return player

    def getPlayer(self,name):
        response = self.__fbpool.httpGetPlayer(name)
        if response.code != 200:
            raise FBAPIException(response.code,response.read())
        data = json.loads(response.read())
        return data

    def getPlayerByKey(self,player_key):
        response = self.__fbpool.httpGetPlayerByKey(player_key)
        if response.code != 200:
            raise FBAPIException(response.code,response.read())
        data = json.loads(response.read())
        return data

    def getPlayerByID(self,player_id):
        response = self.__fbpool.httpGetPlayerByID(player_id)
        if response.code != 200:
            raise FBAPIException(response.code,response.read())
        data = json.loads(response.read())
        return data

    def getAllPlayers(self):
        response = self.__fbpool.httpGetAllPlayers()
        if response.code != 200:
            raise FBAPIException(response.code,response.read())
        data = json.loads(response.read())
        return data

    def getPlayersInYear(self,year):
        response = self.__fbpool.httpGetPlayersInYear(year)
        if response.code != 200:
            raise FBAPIException(response.code,response.read())
        data = json.loads(response.read())
        return data

    def deleteAllPlayers(self):
        response = self.__fbpool.httpDeleteAllPlayers()
        if response.code != 200:
            raise FBAPIException(response.code,response.read())

    def editPlayerByKey(self,player_key,data):
        response = self.__fbpool.httpPutPlayerByKey(player_key,data)
        if response.code != 200:
            raise FBAPIException(response.code,response.read())

    def editPlayerByID(self,player_id,data):
        response = self.__fbpool.httpPutPlayerByID(player_id,data)
        if response.code != 200:
            raise FBAPIException(response.code,response.read())

    def deleteWeekIfExists(self,year,week_number):
        try:
            self.deleteWeek(year=year,week_number=week_number)
        except FBAPIException as e:
            if e.http_code == 404 and e.errmsg == "could not find the week":
                return
            raise FBAPIException(e.http_code,e.errmsg)

    def deleteWeek(self,year,week_number):
        response = self.__fbpool.httpDeleteWeek(year=year,week_number=week_number)
        if response.code != 200:
            raise FBAPIException(response.code,response.read())

    def deleteWeekByKey(self,week_key):
        response = self.__fbpool.httpDeleteWeekByKey(week_key)
        if response.code != 200:
            raise FBAPIException(response.code,response.read())

    def deleteWeekByID(self,week_id):
        response = self.__fbpool.httpDeleteWeekByID(week_id)
        if response.code != 200:
            raise FBAPIException(response.code,response.read())

    def createWeek(self,data):
        response = self.__fbpool.httpPostWeekCreate(data)
        if response.code == 200:
            data = json.loads(response.read())
            return data
        raise FBAPIException(response.code,response.read())

    def getWeekByKey(self,week_key):
        response = self.__fbpool.httpGetWeekByKey(week_key)
        if response.code != 200:
            raise FBAPIException(response.code,response.read())
        data = json.loads(response.read())
        return data

    def getWeekByID(self,week_id):
        response = self.__fbpool.httpGetWeekByID(week_id)
        if response.code != 200:
            raise FBAPIException(response.code,response.read())
        data = json.loads(response.read())
        return data

    def deleteAllWeeks(self):
        response = self.__fbpool.httpDeleteAllWeeks()
        if response.code != 200:
            raise FBAPIException(response.code,response.read())

    def getAllWeeks(self):
        response = self.__fbpool.httpGetAllWeeks()
        if response.code != 200:
            raise FBAPIException(response.code,response.read())
        data = json.loads(response.read())
        return data

    def getWeeksInYear(self,year):
        response = self.__fbpool.httpGetWeeksInYear(year)
        if response.code != 200:
            raise FBAPIException(response.code,response.read())
        data = json.loads(response.read())
        return data

    def getWeek(self,year,week_number):
        response = self.__fbpool.httpGetWeek(year,week_number)
        if response.code != 200:
            raise FBAPIException(response.code,response.read())
        data = json.loads(response.read())
        return data

    def editWeekByKey(self,week_key,data):
        response = self.__fbpool.httpPutWeekByKey(week_key,data)
        if response.code != 200:
            raise FBAPIException(response.code,response.read())

    def editWeekByID(self,week_id,data):
        response = self.__fbpool.httpPutWeekByID(week_id,data)
        if response.code != 200:
            raise FBAPIException(response.code,response.read())


