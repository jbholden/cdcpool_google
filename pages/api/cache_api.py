import webapp2
import logging
import json
from pages.api.api_handler import *
from code.api import *
from code.api_exception import *

class CacheAPILoadDelete(APIHandler):

    def delete(self):
        try:
            api = API()
            api.flush_cache()
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

    def post(self):
        try:
            api = API()
            api.update_cache()
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

class CacheAPILoadYear(APIHandler):

    def post(self,year):
        try:
            api = API()
            api.update_cache_for_year(int(year))
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return

class CacheAPILoadWeek(APIHandler):

    def post(self,year,week_number):
        try:
            api = API()
            api.update_cache_for_week(int(year),int(week_number))
        except APIException as e:
            self.error(e.http_code)
            self.write(e.errmsg)
            return
