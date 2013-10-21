from google.appengine.ext import db
from players import *
from weeks import *

class Pick(db.Model):
    week = db.ReferenceProperty(Week,required=True)
    player = db.ReferenceProperty(Player,required=True)
    game = db.ReferenceProperty(Game,required=True)
    winner = db.StringProperty()
    away_score = db.IntegerProperty()
    home_score = db.IntegerProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)
