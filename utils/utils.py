# Place to put globally useful utilities.

import os
import hmac
import datetime
import string
import re
from pytz.gae import pytz

secret = "cdcpool_abc1234"

def is_debug():
    return os.environ.get('SERVER_SOFTWARE', '').startswith('Development')

def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

def get_datetime_in_utc(datetime_value,initial_timezone):
    pytz_timezone = pytz.timezone(initial_timezone)
    date_in_timezone = pytz_timezone.localize(datetime_value)
    date_in_utc = date_in_timezone.astimezone(pytz.utc)
    return date_in_utc

def get_current_time_in_utc():
    return datetime.datetime.utcnow()

def escape_string(s):
    return string.replace(s,'"','\\\"')

def compress_html(html):
    s1 = string.replace(html,'\n','')
    return re.sub(r'\s\s+',' ',s1)

def memcache_time():
    return 604800
