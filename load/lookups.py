from google.appengine.ext import db

class Lookup(db.Model):
    name = db.StringProperty()
    recno = db.IntegerProperty()
    instance_key = db.StringProperty()
    #instance_key = db.Key()
