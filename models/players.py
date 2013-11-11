from google.appengine.ext import db

# combine years into 1 player or 1 instance per year?

class Player(db.Model):
    name = db.StringProperty(required=True)
    year = db.IntegerProperty(int,required=True)
    #years = db.ListProperty(int,required=True)
