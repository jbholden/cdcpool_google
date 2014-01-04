import webapp2
import unittest
import re
import logging
import utils.timezone as tz
from datetime import *
from pages.handler import *
from google.appengine.ext import db
from code.database import *
from models.games import *
from models.weeks import *
from pytz.gae import pytz
import pdb

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
# A few words about form_dict, a dictionary that is used to aggregate form data.
#  o The idea is to do something like this:
#    - form_dict['game_1']['team1'] = self.request.get('game_1_team1')
#    - form_dict['logistics']['season_year'] = self.request.get('season_year')
#    - form_dict['game_10']['errors'][0] = '<team> is a duplicate'
#    - form_dict['logistics']['errors'][1] = 'Specified week/year already exists'
#  o form_dict takes the form:
#    - form_dict[<form_line>][<form_sel_name>] is a value
#    - form_dict[<form_line>]['errors'] is a list
######################################################################################

class CreateWeekPage(Handler):

  def get_teams(self):
    d = Database()
    team_dictionary = d.load_teams(key="teams")
    team_objects = team_dictionary.values()
    team_names = [team.name for team in team_objects]
    return team_names

  def code(self):
    c  = '<html><head>'
    c += '</head><body>'
    c += '<h1>Placeholder - POST create_week was successful</h1>'
    c += '</body></html>'
    return c

  def post(self):
    mytz = pytz.timezone('US/Eastern')
    form_error = False
    form_dict = dict()

    team_string = ['visitor', 'home']
    selected_teams = dict()

    for game_number in range(1,11):
      form_line = 'game_' + str(game_number)
      form_dict[form_line] = dict()
      form_dict[form_line]['errors'] = list()
      for form_sel_name in ['team1', 'team2']:
        form_field_name = form_line + '_' + form_sel_name
        form_dict[form_line][form_sel_name] = self.request.get(form_field_name)
        if form_dict[form_line][form_sel_name] == 'SELECT ONE':
          # CHECK Each game has a team1 and a team2.
          form_error = True
          form_dict[form_line]['errors'].append('Must select ' + team_string[(int(form_sel_name[-1:]) - 1)] + ' team')
        elif form_dict[form_line][form_sel_name] in selected_teams:
          # CHECK No team is repeated.
          form_error = True
          form_dict[form_line]['errors'].append(form_dict[form_line][form_sel_name] + ' is a duplicate')
        else:
          selected_teams[form_dict[form_line][form_sel_name]] = 1

      form_sel_name = 'favorite'
      form_field_name = form_line + '_' + form_sel_name
      try:
        form_dict[form_line][form_sel_name] = int(self.request.get(form_field_name))
      except:
        form_dict[form_line][form_sel_name] = 0
      if (form_dict[form_line][form_sel_name] < 1) or (form_dict[form_line][form_sel_name] > 2):
        # CHECK Each game has a favorite.
        form_error = True
        del form_dict[form_line][form_sel_name]
        form_dict[form_line]['errors'].append('Favorite not selected')

      form_sel_name = 'spread'
      form_field_name = form_line + '_' + form_sel_name
      form_dict[form_line][form_sel_name] = self.request.get(form_field_name)
      try:
        f = float(form_dict[form_line][form_sel_name])
      except:
        f = 0.0
      if ((int((f * 10) / 5) % 2) == 0) or (f < 0.0):
        # CHECK Each game has a point spread with 1/2 point offset (IOW, divide by 0.5, result should be odd number).
        form_error = True
        form_dict[form_line]['errors'].append('Need positive 1/2 point spread')

      KICKOFF_DATETIME_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2})$")
      form_sel_name = 'kickoff'
      form_field_name = form_line + '_' + form_sel_name
      form_dict[form_line][form_sel_name] = self.request.get(form_field_name)
      m = KICKOFF_DATETIME_RE.match(form_dict[form_line][form_sel_name])
      if not m:
        form_error = True
        form_dict[form_line]['errors'].append('Kickoff Date/Time fmt yyyy-mm-dd hh:mm')

    form_dict['logistics'] = dict()
    form_dict['logistics']['errors'] = list()
    form_dict['logistics']['week_number'] = int(self.request.get('week_number'))
    if ((form_dict['logistics']['week_number'] < 1) or (form_dict['logistics']['week_number'] > 13)):
      # CHECK Week number should be selected.
      form_error = True
      form_dict['logistics']['errors'].append('Must select valid Week Number')

    try:
      form_dict['logistics']['season_year'] = int(self.request.get('season_year'))
    except:
      form_dict['logistics']['season_year'] = 0
    if (form_dict['logistics']['season_year'] < 2013):
      # CHECK Year should be >= current year.
      form_error = True
      del form_dict['logistics']['season_year']
      form_dict['logistics']['errors'].append('Specified year must be 2013 or higher')

    d = Database()
    if form_dict['logistics'].get('season_year') and form_dict['logistics'].get('week_number') and d.is_week_valid(form_dict['logistics']['week_number'], form_dict['logistics']['season_year']):
      # CHECK Target week should not already exist.
      form_error = True
      form_dict['logistics']['errors'].append('Specified week/year already exists')

    #pdb.set_trace()

    if (form_error):
      teams = self.get_teams()
      teams.sort()
      # re-render using existing form_dict
      self.render("create_week_commish.html", teams=teams, form_dict=form_dict)

    else:
      teamkeys = d.load_teams(key="teamkeys")
      #pdb.set_trace()
      games = dict()
      for i in range(1,11):
        gindex = str(i)
        games[gindex] = dict()
        form_line = 'game_' + str(i)
        games[gindex]['number'] = i
        games[gindex]['team1'] = teamkeys[form_dict[form_line]['team1']]
        games[gindex]['team2'] = teamkeys[form_dict[form_line]['team2']]
        games[gindex]['favored'] = 'team' + str(form_dict[form_line]['favorite'])
        games[gindex]['spread'] = float(form_dict[form_line]['spread'])
        games[gindex]['state'] = 'not_started'
        m = KICKOFF_DATETIME_RE.match(form_dict[form_line]['kickoff'])
        games[gindex]['date'] = mytz.localize(datetime(int(m.group(1)),int(m.group(2)),int(m.group(3)),int(m.group(4)),int(m.group(5)))) #TODO need user TZ

      week = dict()
      week['year'] = form_dict['logistics']['season_year']
      week['number'] = form_dict['logistics']['week_number']
      week['winner'] = None

      d.put_games_week_in_database(games,week)

      self.response.write(self.code())

  def get(self):
    teams = self.get_teams()
    teams.sort()

    # Initialize form_dict (required for tests in html/jinja)
    form_dict_indexes = ['game_' + str(i) for i in range(1,11)]
    form_dict_indexes.append('logistics')
    form_dict = dict((index,dict([('errors',list())])) for index in form_dict_indexes)

    d = Database()
    (form_dict['logistics']['season_year'], form_dict['logistics']['week_number']) = d.get_next_year_week_for_create_week()
    form_dict['logistics']['week_number'] = int(form_dict['logistics']['week_number'])

    # Initialize 'kickoff' datetime for each game by Assuming that the commissioner is creating the pick sheet
    # the week that the games are played, so default kickoff date is the subsequent Saturday after today's date.
    today = date.today()
    days_before_saturday = (5 - today.weekday()) % 7
    saturday = today + (days_before_saturday * timedelta(days=1))
    for i in range(1,11):
      form_dict['game_'+str(i)]['kickoff'] = saturday.strftime("%Y-%m-%dT13:00")

    self.render("create_week_commish.html", teams=teams, form_dict=form_dict)
    return

