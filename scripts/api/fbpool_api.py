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
