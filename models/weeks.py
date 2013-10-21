from google.appengine.ext import db
from players import *
from weeks import *

class Week(db.Model):
    year = db.IntegerProperty(required=True)
    number = db.IntegerProperty(required=True)
    winner = db.ReferenceProperty(Player,required=True)
    games = db.ListProperty(Game)
