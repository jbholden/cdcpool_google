import unittest
import pytz.gae as pytz
import datetime
from utils.utils import *

class TestTimezone(unittest.TestCase):

    def test_assign_date_in_datastore(self):
        # this test attempts to emulate the following test case:
        # + user enters a date on the web page (in this example time is entered in eastern time zone)
        # + web page code gets the date (initially naive), converts it to UTC, and assigns to the datastore
        date_from_webpage = datetime.datetime(2010,2,24,19,30)

        eastern = pytz.pytz.timezone('US/Eastern')
        date_in_eastern = eastern.localize(date_from_webpage)

        date_in_utc = date_in_eastern.astimezone(pytz.pytz.utc)
        # assign date_in_utc to datastore object date property

        # do some verification to see if this makes sense
        fmt = "%I:%M %p %Z"
        self.assertEqual(date_in_eastern.strftime(fmt),"07:30 PM EST")
        self.assertEqual(date_in_utc.strftime(fmt),"12:30 AM UTC")

    def test_assign_date_in_datastore_using_util_function(self):
        # same as the test_assign_date_in_datastore test but uses the utils.py function
        date_from_webpage = datetime.datetime(2010,2,24,19,30)
        date_in_utc = get_datetime_in_utc(date_from_webpage,'US/Eastern')

        fmt = "%I:%M %p %Z"
        self.assertEqual(date_in_utc.strftime(fmt),"12:30 AM UTC")


    def test_pytz_timezone_names_list(self):
        self.assertGreater(len(pytz.pytz.all_timezones),0)
        self.assertIn('US/Eastern',pytz.pytz.all_timezones)
        self.assertIn('US/Central',pytz.pytz.all_timezones)
        self.assertIn('US/Mountain',pytz.pytz.all_timezones)
        self.assertIn('US/Pacific',pytz.pytz.all_timezones)
        self.assertIn('Europe/London',pytz.pytz.all_timezones)


    def test_standard_time_conversions(self):
        utc = pytz.pytz.utc
        eastern = pytz.pytz.timezone('US/Eastern')
        central = pytz.pytz.timezone('US/Central')
        mountain = pytz.pytz.timezone('US/Mountain')
        pacific = pytz.pytz.timezone('US/Pacific')
        london = pytz.pytz.timezone('Europe/London')

        # assign date to 2/24/2010 7:30 PM eastern
        test_date_naive = datetime.datetime(2010,2,24,19,30)
        test_date_localized = eastern.localize(test_date_naive)
        test_date_utc = test_date_localized.astimezone(utc)

        fmt = "%I:%M %p %Z"
        date_utc = test_date_utc.astimezone(utc).strftime(fmt)
        date_eastern = test_date_utc.astimezone(eastern).strftime(fmt)
        date_central = test_date_utc.astimezone(central).strftime(fmt)
        date_mountain = test_date_utc.astimezone(mountain).strftime(fmt)
        date_pacific = test_date_utc.astimezone(pacific).strftime(fmt)
        date_london = test_date_utc.astimezone(london).strftime(fmt)

        self.assertEqual(date_utc,"12:30 AM UTC")
        self.assertEqual(date_london,"12:30 AM GMT")
        self.assertEqual(date_eastern,"07:30 PM EST")
        self.assertEqual(date_central,"06:30 PM CST")
        self.assertEqual(date_mountain,"05:30 PM MST")
        self.assertEqual(date_pacific,"04:30 PM PST")


    def test_daylight_time_conversions(self):
        utc = pytz.pytz.utc
        eastern = pytz.pytz.timezone('US/Eastern')
        central = pytz.pytz.timezone('US/Central')
        mountain = pytz.pytz.timezone('US/Mountain')
        pacific = pytz.pytz.timezone('US/Pacific')
        london = pytz.pytz.timezone('Europe/London')

        # assign date to 3/10/2014 7:30 PM eastern
        test_date_naive = datetime.datetime(2014,3,10,19,30)
        test_date_localized = eastern.localize(test_date_naive)
        test_date_utc = test_date_localized.astimezone(utc)

        fmt = "%I:%M %p %Z"
        date_utc = test_date_utc.astimezone(utc).strftime(fmt)
        date_eastern = test_date_utc.astimezone(eastern).strftime(fmt)
        date_central = test_date_utc.astimezone(central).strftime(fmt)
        date_mountain = test_date_utc.astimezone(mountain).strftime(fmt)
        date_pacific = test_date_utc.astimezone(pacific).strftime(fmt)
        date_london = test_date_utc.astimezone(london).strftime(fmt)

        self.assertEqual(date_utc,"11:30 PM UTC")
        self.assertEqual(date_london,"11:30 PM GMT")
        self.assertEqual(date_eastern,"07:30 PM EDT")
        self.assertEqual(date_central,"06:30 PM CDT")
        self.assertEqual(date_mountain,"05:30 PM MDT")
        self.assertEqual(date_pacific,"04:30 PM PDT")

