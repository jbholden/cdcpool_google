from google.appengine.ext import db
from players import *
from weeks import *

class Pick(db.Model):
    week = db.StringProperty()    # string key of type Week
    player = db.StringProperty()  # string key of type Player
    game = db.StringProperty()    # string key of type Game
    winner = db.StringProperty()
    team1_score = db.IntegerProperty()
    team2_score = db.IntegerProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)
