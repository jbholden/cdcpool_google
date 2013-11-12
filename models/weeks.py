from google.appengine.ext import db
from players import *
from weeks import *
from games import *

class Week(db.Model):
    year = db.IntegerProperty(required=True)
    number = db.IntegerProperty(required=True)
    winner = db.Key()
    games = db.ListProperty(db.Key)
    lock_picks = db.DateTimeProperty()    # note: when setting need to consider UTC and timezone
    lock_scores = db.DateTimeProperty()   # note: when setting need to consider UTC and timezone
