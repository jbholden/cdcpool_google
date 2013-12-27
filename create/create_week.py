import webapp2
import unittest
from pages.handler import *

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
#    - Week number should be selected.
#    - Year should be >= current year.
#    - Target week should not already exist.
######################################################################################

class CreateWeekPage(Handler):

  def list_of_teams(self):
    list_teams = (
        'Boston College',
        'Clemson',
        'Duke',
        'Florida State',
        'Georgia Tech',
        'Maryland',
        'Miami-Florida',
        'North Carolina',
        'NC State',
        'Pittsburgh',
        'Syracuse',
        'Virginia',
        'Virginia Tech',
        'Wake Forest',
        'Alabama',
        'Arkansas',
        'Auburn',
        'Florida',
        'Georgia',
        'Kentucky',
        'LSU',
        'Mississippi',
        'Mississippi State',
        'Missouri',
        'South Carolina',
        'Tennessee',
        'Texas A&M',
        'Vanderbilt',
    )
    return list_teams

  def code(self):
    c  = '<html><head>'
    c += '</head><body>'
    c += '<h1>Placeholder - POST create_week</h1>'
    c += '</body></html>'
    return c

  def post(self):
    self.response.write(self.code())

  def get(self):
    teams = self.list_of_teams()
    self.render("create_week_commish.html", teams=teams)
    return

