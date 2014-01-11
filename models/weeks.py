from google.appengine.ext import db
from players import *
from weeks import *
from games import *

class Week(db.Model):
    year = db.IntegerProperty(required=True)
    number = db.IntegerProperty(required=True)
    winner = db.StringProperty()   # winner key string
    games = db.ListProperty(db.Key)
    lock_picks = db.DateTimeProperty()    
    lock_scores = db.DateTimeProperty()   
