FBPool API
===========
This directory contains scripts that make API calls using python to the FBPool API.
`fbpool_api.py` is the main file that should be used to make API calls.

## Files
* `fbpool_api.py` this is the file that contains the methods that can be used to make API calls
* `fbpool_api_exception.py` this exception is raised by the fbpool_api.py if an error occurs
* `fbpool_http.py` this implements the HTTP calls to connect to the API

## Example

This example creates a new team.

``
from api.fbpool_api import *

api = FBPoolAPI(url='http://cdcpool.appspot.com')
team = api.createTeam('Georgia Tech','Atlantic Coast')
``

