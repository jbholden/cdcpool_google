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
        pass

    def deleteTeamByKey(self,team_key):
        pass

    def deleteTeamByID(self,team_id):
        pass

    def getTeam(self,name):
        pass

    def getTeamByKey(self,team_key):
        pass

    def getTeamByID(self,team_id):
        pass

    def getAllTeams(self):
        pass

    def deleteAllTeams(self):
        pass

    def deleteTeamIfExists(self,name):
        pass

    def addTeam(self,name,conference):
        pass

    def createTeams(self):
        pass

