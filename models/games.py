from google.appengine.ext import db
from teams import *

class Game(db.Model):
    number = db.IntegerProperty(required=True)
    away_team = db.ReferenceProperty(Team,required=True)
    home_team = db.ReferenceProperty(Team,required=True)
    away_score = db.IntegerProperty(required=True)
    home_score = db.IntegerProperty(required=True)
    favored = db.StringProperty(required=True)
    spread = db.FloatProperty(required=True)
    state = db.StringProperty(required=True)
    quarter = db.StringProperty()
    time_left = db.StringProperty()
    date = db.DateTimeProperty()
