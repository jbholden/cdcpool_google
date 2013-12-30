import webapp2
import unittest
import logging
from pages.handler import *
from google.appengine.ext import db
from code.database import *
from load.loadgames import *
from load.loadweeks import *
#import pdb

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

  def get_sorted_teams(self):
    db = Database()
    team_dictionary = db.load_teams()
    team_objects = team_dictionary.values()
    team_names = [team.name for team in team_objects]
    team_names.sort()
    return team_names

  def code(self):
    c  = '<html><head>'
    c += '</head><body>'
    c += '<h1>Placeholder - POST create_week was successful</h1>'
    c += '</body></html>'
    return c

  def post(self):
    form_error = False
    #logging.info("Init form_error")
    form_dict = dict()

    team_string = ['visitor', 'home']
    selected_teams = dict()

    for game_number in range(1,11):
      for team_number in range(1,3):
        specifier = 'game_' + str(game_number) + '_team' + str(team_number)
        form_dict[specifier] = self.request.get(specifier)
        form_dict_key = 'err_' + specifier
        if form_dict[specifier] == 'SELECT ONE':
          # CHECK Each game has a team1 and a team2.
          form_error = True
          #logging.info("Team not selected, form_error = True, " + specifier)
          form_dict[form_dict_key] = 'Must select ' + team_string[(int(specifier[-1:]) - 1)] + ' team'
        elif form_dict[specifier] in selected_teams:
          # CHECK No team is repeated.
          form_error = True
          #logging.info("Team repeated, form_error = True, " + specifier)
          form_dict[form_dict_key] = form_dict[specifier] + ' is a duplicate'
        else:
          selected_teams[form_dict[specifier]] = 1

      specifier = 'game_' + str(game_number) + '_favorite'
      try:
        form_dict[specifier] = int(self.request.get(specifier))
      except:
        form_dict[specifier] = 0
      if (form_dict[specifier] < 1) or (form_dict[specifier] > 2):
        # CHECK Each game has a favorite.
        form_error = True
        #logging.info("No favorite, form_error = True, " + specifier)
        form_dict.pop(specifier, None)
        form_dict_key = 'err_' + specifier
        form_dict[form_dict_key] = 'Favorite not selected'

      specifier = 'game_' + str(game_number) + '_spread'
      form_dict[specifier] = self.request.get(specifier)
      try:
        f = float(form_dict[specifier])
      except:
        f = 0.0
      if ((int((f * 10) / 5) % 2) == 0):
        # CHECK Each game has a point spread with 1/2 point offset (IOW, divide by 0.5, result should be odd number).
        form_error = True
        #logging.info("Bad spread, form_error = True, " + specifier)
        form_dict_key = 'err_' + specifier
        form_dict[form_dict_key] = 'Need 1/2 point spread'

    form_dict['week_number'] = int(self.request.get('week_number'))
    if ((form_dict['week_number'] < 1) or (form_dict['week_number'] > 13)):
      # CHECK Week number should be selected.
      form_error = True
      #logging.info("Bad week, form_error = True")
      form_dict['err_week_number'] = 'Must select valid Week Number'

    try:
      form_dict['season_year'] = int(self.request.get('season_year'))
    except:
      form_dict['season_year'] = 0
    if (form_dict['season_year'] < 2013):
      # CHECK Year should be >= current year.
      form_error = True
      #logging.info("Bad year, form_error = True")
      form_dict.pop('season_year', None)
      form_dict['err_season_year'] = 'Specified year must be 2013 or higher'

    db = Database()
    if form_dict.get('season_year') and form_dict.get('week_number') and db.is_week_valid(form_dict['week_number'], form_dict['season_year']):
      # CHECK Target week should not already exist.
      form_error = True
      form_dict['err_season_week'] = 'Specified week/year already exists'

    #pdb.set_trace()

    if (form_error):
      teams = self.get_sorted_teams()
      form_dict['err_week_year_line'] = ';'.join(form_dict.get(i) for i in ['err_week_number', 'err_season_year', 'err_season_week'] if form_dict.get(i))
      if not form_dict['err_week_year_line']: form_dict.pop('err_week_year_line', None)
      error_items = ['team1', 'team2', 'favorite', 'spread']
      for g in range(1,11):
        error_line = 'err_game_' + str(g) + '_line'
        error_list = [('err_game_' + str(g) + '_' + item) for item in error_items]
        form_dict[error_line] = ';'.join(form_dict.get(i) for i in error_list if form_dict.get(i))
        if not form_dict[error_line]: form_dict.pop(error_line, None)

      self.render("create_week_commish.html", teams=teams, form_dict=form_dict)
    else:
      # TODO placeholder, this is where you would load database with new week picks.
      lg = LoadGames()
      game = dict()
      for i in range(1,11):
        leader = 'game_' + str(i) + '_'
        game['number'] = i
        game['team1'] = form_dict[leader + 'team1']
        game['team2'] = form_dict[leader + 'team2']
        game['favored'] = 'team' + str(form_dict[leader + 'favorite'])
        game['spread'] = float(form_dict[leader + 'spread'])
        game['team1_score'] = None
        game['team2_score'] = None
        game['state'] = 'not_started'
        # TODO Figure out how to determine recno
        #game['recno'] = 1000 + i
        #lg.add_game(game)

      lw = LoadWeeks()
      week = dict()
      week['number'] = form_dict['week_number']
      week['year'] = form_dict['season_year']
      # TODO Figure out how to determine recno
      #week['recno'] = 1000 + i
      #lw.add_week(week)

      self.response.write(self.code())

  def get(self):
    teams = self.get_sorted_teams()
    form_dict = dict()
    self.render("create_week_commish.html", teams=teams, form_dict=form_dict)
    return

