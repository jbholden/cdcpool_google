import webapp2
import unittest
import logging
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

  def get_list_of_teams():
    teams_query = db.GqlQuery('select * from Team')
    teams = list(teams_query)
    list_team_names = []
    for team in teams:
      list_team_names.append(team.name)
    list_team_names.sort()
    return list_team_names

  global teams
  teams = get_list_of_teams()

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
        team_specifier = 'game_' + str(game_number) + '_team' + str(team_number)
        form_dict[team_specifier] = self.request.get(team_specifier)
        form_dict_key = 'err_' + team_specifier
        if form_dict[team_specifier] == 'SELECT ONE':
          # CHECK Each game has a team1 and a team2.
          form_error = True
          #logging.info("Team not selected, form_error = True, " + team_specifier)
          form_dict[form_dict_key] = 'Must select ' + team_string[(int(team_specifier[-1:]) - 1)] + ' team'
        elif form_dict[team_specifier] in selected_teams:
          # CHECK No team is repeated.
          form_error = True
          #logging.info("Team repeated, form_error = True, " + team_specifier)
          form_dict[form_dict_key] = form_dict[team_specifier] + ' is a duplicate'
        else:
          selected_teams[form_dict[team_specifier]] = 1

      favorite_specifier = 'game_' + str(game_number) + '_favorite'
      try:
        form_dict[favorite_specifier] = int(self.request.get(favorite_specifier))
      except:
        form_dict[favorite_specifier] = 0
      if (form_dict[favorite_specifier] < 1) or (form_dict[favorite_specifier] > 2):
        # CHECK Each game has a favorite.
        form_error = True
        #logging.info("No favorite, form_error = True, " + favorite_specifier)
        form_dict.pop(favorite_specifier, None)
        form_dict_key = 'err_' + favorite_specifier
        form_dict[form_dict_key] = 'Favorite not selected'

      spread_specifier = 'game_' + str(game_number) + '_spread'
      form_dict[spread_specifier] = self.request.get(spread_specifier)
      try:
        f = float(form_dict[spread_specifier])
      except:
        f = 0.0
      if ((int((f * 10) / 5) % 2) == 0):
        # CHECK Each game has a point spread with 1/2 point offset (IOW, divide by 0.5, result should be odd number).
        form_error = True
        #logging.info("Bad spread, form_error = True, " + spread_specifier)
        form_dict_key = 'err_' + spread_specifier
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

    if (form_error):
      #logging.info("selected_teams = " + ','.join(selected_teams.keys()))
      form_dict['err_week_year_line'] = ';'.join(form_dict.get(i,'') for i in ['err_week_number', 'err_season_year'])
      form_dict['err_game_1_line']  = ';'.join(form_dict.get(i,'') for i in ['err_game_1_team1', 'err_game_1_team2', 'err_game_1_favorite', 'err_game_1_spread'])
      form_dict['err_game_2_line']  = ';'.join(form_dict.get(i,'') for i in ['err_game_2_team1', 'err_game_2_team2', 'err_game_2_favorite', 'err_game_2_spread'])
      form_dict['err_game_3_line']  = ';'.join(form_dict.get(i,'') for i in ['err_game_3_team1', 'err_game_3_team2', 'err_game_3_favorite', 'err_game_3_spread'])
      form_dict['err_game_4_line']  = ';'.join(form_dict.get(i,'') for i in ['err_game_4_team1', 'err_game_4_team2', 'err_game_4_favorite', 'err_game_4_spread'])
      form_dict['err_game_5_line']  = ';'.join(form_dict.get(i,'') for i in ['err_game_5_team1', 'err_game_5_team2', 'err_game_5_favorite', 'err_game_5_spread'])
      form_dict['err_game_6_line']  = ';'.join(form_dict.get(i,'') for i in ['err_game_6_team1', 'err_game_6_team2', 'err_game_6_favorite', 'err_game_6_spread'])
      form_dict['err_game_7_line']  = ';'.join(form_dict.get(i,'') for i in ['err_game_7_team1', 'err_game_7_team2', 'err_game_7_favorite', 'err_game_7_spread'])
      form_dict['err_game_8_line']  = ';'.join(form_dict.get(i,'') for i in ['err_game_8_team1', 'err_game_8_team2', 'err_game_8_favorite', 'err_game_8_spread'])
      form_dict['err_game_9_line']  = ';'.join(form_dict.get(i,'') for i in ['err_game_9_team1', 'err_game_9_team2', 'err_game_9_favorite', 'err_game_9_spread'])
      form_dict['err_game_10_line'] = ';'.join(form_dict.get(i,'') for i in ['err_game_10_team1', 'err_game_10_team2', 'err_game_10_favorite', 'err_game_10_spread'])
      self.render("create_week_commish.html", teams=teams, form_dict=form_dict)
    else:
      # TODO placeholder, this is where you would load database with new week picks.
      self.response.write(self.code())

  def get(self):
    form_dict = dict()
    self.render("create_week_commish.html", teams=teams, form_dict=form_dict)
    return

