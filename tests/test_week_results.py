from google.appengine.ext import db
from google.appengine.api import memcache
import logging
import unittest
import urllib2
import socket
from pages.week_results_page import *
from code.database import *
from code.update import *
from google.appengine.api import urlfetch


class TestWeekResults(unittest.TestCase):

    def setUp(self):
        self.hostname = socket.gethostname()
        urlfetch.set_default_fetch_deadline(60)

    def test_page_active(self):
        d = Database()
        weeks_and_years = d.load_weeks_and_years()
        self.__weeks_and_years_sanity_check(weeks_and_years)

        self.__ensure_data_loaded_into_memcache(weeks_and_years)

        for year in weeks_and_years:
            for week_number in weeks_and_years[year]:
                page_address = '/%d/week/%d/results' % (year,week_number)
                self.__test_page_active(page_address)

    def test_bad_pages(self):
        self.__test_page_error('/1900/week/1/results')
        self.__test_page_error('/2013/week/14/results')

        #response = urllib2.urlopen('http://%s/2013/week/1/results' % (self.hostname))
        #self.assertIsNotNone(response)
        #import pdb; pdb.set_trace()
        #url = response.geturl()
        #info = response.info()
        #code = response.getcode()
        #html = response.read()
        #response = self.testapp.get('/2013/week/1')
        #self.assertEqual(response.status_int,200)
        #self.assertEqual(response.content_type,"text/html")
        #self.assertEqual(response.normal_body,200)

    def __ensure_data_loaded_into_memcache(self,weeks_and_years):
        u = Update()
        for year in weeks_and_years:
            for week_number in weeks_and_years[year]:
                data = u.get_week_results(year,week_number)

    def __weeks_and_years_sanity_check(self,weeks_and_years):
        # should have at least years 2012 and 2013, each with 13 weeks
        self.assertIn(2012,weeks_and_years)
        self.assertIn(2013,weeks_and_years)
        for week_number in range(1,14):
            self.assertIn(week_number,weeks_and_years[2012])
            self.assertIn(week_number,weeks_and_years[2013])


    def __test_page_active(self,page):
        start = time.time()
        response = self.__get(page)
        page_load_time = time.time()-start
        self.assertIsNotNone(response)
        self.assertEqual(response.getcode(),200)
        self.assertEqual(response.info().getheader('content-type'),'text/html; charset=utf-8')
        # ignore this for now
        # self.assertLess(page_load_time,1.0)  # should load in less than 1 second

    def __test_page_error(self,page):
        try:
            response = self.__get(page)
            code = response.getcode()
        except urllib2.HTTPError,err:
            code = err.code
        self.assertEqual(code,400)

    def __get(self,address):
        url = 'http://%s%s' % (self.hostname,address)
        return urllib2.urlopen(url)


