import urllib2
import urllib
import json
import logging

class FBPoolHTTP:

    def __init__(self,url='http://cdcpool.appspot.com'):
        self.url = url

    def __geturl(self,address):
        return "%s%s" % (self.url,address)

    def httpGet(self,address,data=None):
        if data != None:
            headers = { 'Content-Type' : 'application/json; charset=UTF-8' }
            data_json = json.dumps(data)
        try:
            if data != None:
                req = urllib2.Request(self.__geturl(address),data_json,headers)
            else:
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

    def httpDelete(self,address,data):
        headers = { 'Content-Type' : 'application/json; charset=UTF-8' }
        data_json = json.dumps(data)
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        try:
            req = urllib2.Request(self.__geturl(address),data_json,headers)
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

    def httpGetTeam(self,name):
        data = dict()
        data['name'] = name
        return self.httpGet('/api/team',data)

    def httpGetTeamByKey(self,team_key):
        data = dict()
        data['key'] = team_key
        return self.httpGet('/api/team',data)

    def httpGetTeamByID(self,team_id):
        data = dict()
        data['id'] = team_id
        return self.httpGet('/api/team',data)

if __name__ == "__main__":
    api = FBPoolHTTP("http://localhost:10090")
    response = api.httpDeleteTeam("Team1")
