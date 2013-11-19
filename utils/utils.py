# Place to put globally useful utilities.

import os

def is_debug():
    return os.environ.get('SERVER_SOFTWARE', '').startswith('Development')
