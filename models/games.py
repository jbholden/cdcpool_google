from google.appengine.ext import db
from teams import *

class Game(db.Model):
    number = db.IntegerProperty()
    team1 = db.StringProperty()     # key of type Team
    team2 = db.StringProperty()     # key of type Team
    team1_score = db.IntegerProperty()
    team2_score = db.IntegerProperty()
    favored = db.StringProperty()
    spread = db.FloatProperty()
    state = db.StringProperty()
    quarter = db.StringProperty()
    time_left = db.StringProperty()
    date = db.DateTimeProperty()
