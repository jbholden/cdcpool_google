import urllib2
import urllib
import json

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

    def httpDelete(self,address):
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        try:
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
