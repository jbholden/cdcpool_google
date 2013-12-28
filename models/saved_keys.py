from google.appengine.ext import db

# these are the keys of objects created for testing
# these keys are saved in order to delete them at a later time
class SavedKeys(db.Model):
    name = db.StringProperty()   
    key_list = db.StringListProperty()
