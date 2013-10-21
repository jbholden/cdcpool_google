from google.appengine.ext import db

class Team(db.Model):
    name = db.StringProperty(required=True)
    conference = db.StringProperty()
