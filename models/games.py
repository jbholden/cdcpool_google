from google.appengine.ext import db
from teams import *

class Game(db.Model):
    number = db.IntegerProperty()
    team1 = db.Key()
    team2 = db.Key()
    team1_score = db.IntegerProperty()
    team2_score = db.IntegerProperty()
    favored = db.StringProperty()
    spread = db.FloatProperty()
    state = db.StringProperty()
    quarter = db.StringProperty()
    time_left = db.StringProperty()
    date = db.DateTimeProperty()
