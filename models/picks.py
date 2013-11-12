from google.appengine.ext import db
from players import *
from weeks import *

class Pick(db.Model):
    week = db.Key()
    player = db.Key()
    game = db.Key()
    winner = db.StringProperty()
    team1_score = db.IntegerProperty()
    team2_score = db.IntegerProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)
