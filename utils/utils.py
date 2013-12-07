# Place to put globally useful utilities.

import os
import hmac

secret = "cdcpool_abc1234"

def is_debug():
    return os.environ.get('SERVER_SOFTWARE', '').startswith('Development')

def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val
