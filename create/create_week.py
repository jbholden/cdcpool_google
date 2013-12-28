import webapp2
import unittest
from pages.handler import *
from google.appengine.ext import db

######################################################################################
# This is what a commissioner uses to create a new set of weekly picks.
#  o There will be 10 games.
#  o Each game:
#    - Drop down lists to select Visitor and Home teams.
#    - Radio buttons will select one or the other as the favorite.
#    - Text box is used to enter the point spread.
#  o Checks that need to be performed at post:
#    - Each game has a team1 and a team2.
#    - Each game has a favorite.
#    - Each game has a point spread with 1/2 point offset (IOW, divide by 0.5, result should be odd number).
#    - No team is repeated.
#    - Week number should be selected.
#    - Year should be >= current year.
#    - Target week should not already exist.
######################################################################################

class CreateWeekPage(Handler):

  def get_list_of_teams(self):
    teams_query = db.GqlQuery('select * from Team')
    teams = list(teams_query)
    list_team_names = []
    for team in teams:
      list_team_names.append(team.name)
    list_team_names.sort()
    return list_team_names

  def code(self):
    c  = '<html><head>'
    c += '</head><body>'
    c += '<h1>Placeholder - POST create_week</h1>'
    c += '</body></html>'
    return c

  def post(self):
    self.response.write(self.code())

  def get(self):
    teams = self.get_list_of_teams()
    self.render("create_week_commish.html", teams=teams)
    return

