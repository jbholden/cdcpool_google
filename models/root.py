from google.appengine.ext import db

# These functions construct keys intended to be used as 
# ancestors for strong consistency.

def root_teams():
    return db.Key.from_path("FBPoolRoot","root_teams")

def root_players():
    return db.Key.from_path("FBPoolRoot","root_players")

def root_weeks():
    return db.Key.from_path("FBPoolRoot","root_weeks")

def root_games_master():
    return db.Key.from_path("FBPoolRoot","root_games")

def root_games(year,week_number):
    game_key = "root_games_%d_%d" % (year,week_number)
    return db.Key.from_path("FBPoolRoot",game_key,parent=root_games_master())

def root_picks_master():
    return db.Key.from_path("FBPoolRoot","root_picks")

def root_picks(year,week_number):
    pick_key = "root_picks_%d_%d" % (year,week_number)
    return db.Key.from_path("FBPoolRoot",pick_key,parent=root_picks_master())

def root_savedkeys():
    return db.Key.from_path("FBPoolRoot","root_saved_keys")


