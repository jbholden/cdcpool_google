from pages.handler import *
from models.teams import *
import datetime

class APIHandler(Handler):

    def build_team_object(self,team):
        t = dict()
        t['id'] = team.key().id()
        t['key'] = str(team.key())
        t['name'] = team.name
        t['conference'] = team.conference
        return t

    def build_game_object(self,game):
        g = dict()
        g['id'] = game.key().id()
        g['key'] = str(game.key())
        g['number'] = game.number
        g['team1'] = game.team1
        g['team2'] = game.team2
        g['team1_score'] = game.team1_score
        g['team2_score'] = game.team2_score
        g['favored'] = game.favored
        g['spread'] = game.spread
        g['state'] = game.state
        g['quarter'] = game.quarter
        g['time_left'] = game.time_left
        g['date'] = self.format_date(game.date)
        return g

    def is_field_missing(self,field,data):
        if field not in data:
            self.error(400)
            self.write('%s is missing' % (field))
            return True
        return False

    def format_date(self,date):
        if date == None:
            return None
        else:
            if date.month < 10:
                month = "0%s" % (date.month)
            else:
                month = "%s" % (date.month)

            if date.day < 10:
                day = "0%s" % (date.day)
            else:
                day = "%s" % (date.day)

            year = "%s" % (date.year)

            if date.hour < 10:
                hour = "0%s" % (date.hour)
            else:
                hour = "%s" % (date.hour)

            if date.minute < 10:
                minute = "0%s" % (date.minute)
            else:
                minute = "%s" % (date.minute)

            return "%s/%s/%s %s:%s" % (month,day,year,hour,minute)

    def convert_to_datetime(self,date_str):
        return datetime.datetime.strptime(date_str,"%m/%d/%Y %H:%M")
