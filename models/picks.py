from google.appengine.ext import db
from players import *
from weeks import *

class Pick(db.Model):
    week = db.ReferenceProperty(Week)
    player = db.ReferenceProperty(Player)
    game = db.ReferenceProperty(Game)
    winner = db.StringProperty()
    team1_score = db.IntegerProperty()
    team2_score = db.IntegerProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)
