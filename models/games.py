from google.appengine.ext import db
from teams import *

class Game(db.Model):
    number = db.IntegerProperty()
    away_team = db.ReferenceProperty(Team,collection_name="away_team")
    home_team = db.ReferenceProperty(Team,collection_name="home_team")
    away_score = db.IntegerProperty()
    home_score = db.IntegerProperty()
    favored = db.StringProperty()
    spread = db.FloatProperty()
    state = db.StringProperty()
    quarter = db.StringProperty()
    time_left = db.StringProperty()
    date = db.DateTimeProperty()
