import webapp2
import logging
from code.update import *
from code.database import *
from handler import *
import string
import re
from pytz.gae import pytz

# TODO:  define base player results and fill in blocks with another html
# TODO: tests
#       + game not started:  view page with a game start date
#       + game not started:  view page with a game start date (different time zones)
#       + game not started:  view page with no game start date
#       + game in progress:  view page with quarter/time combinations
#       + game final:  view page with game final


class PlayerResultsPage(Handler):

    def __get_player_key(self,player_id):
        return db.Key.from_path('Player',player_id)

    def __is_player_id_valid(self,player_key):
        return player_key != None

    def __is_player_in_year(self,player_key,year,database):
        players_in_year = database.load_players(year)
        return str(player_key) in players_in_year

    def set_game_status_params(self,params,results):
        top_ids = []
        top_statuses = []
        bottom_ids = []
        bottom_statuses = []

        for result in results:
            top_status,bottom_status,top_id,bottom_id = self.get_game_status(result)

            top_ids.append(top_id)
            top_statuses.append(top_status)
            bottom_ids.append(bottom_id)
            bottom_statuses.append(bottom_status)

        params['top_status_id'] = top_ids
        params['top_status'] = top_statuses
        params['bottom_status_id'] = bottom_ids
        params['bottom_status'] = bottom_statuses


    def get_game_status(self,result):
        if result.game_state == "not_started":
            return self.__game_not_started_status(result)
        elif result.game_state == "in_progress":
            return self.__game_in_progress_status(result)
        elif result.game_state == "final":
            return self.__game_final_status()
        raise AssertionError,"bad game state: %s" % (result.game_state)


    def __game_not_started_status(self,result):
        if result.game_date == None:
            top_status = ""
            bottom_status = ""
            top_id = "status-empty"
            bottom_id = "status-empty"
        else:
            utc_date = pytz.utc.localize(result.game_date)
            local_game_date = utc_date.astimezone(self.__get_local_timezone())
            weekday_month_day = "%a %m/%d"
            hour_minutes_ampm_timezone = "%I:%M %p %Z"
            top_status = local_game_date.strftime(weekday_month_day)
            bottom_status = local_game_date.strftime(hour_minutes_ampm_timezone)
            top_id = "game-time"
            bottom_id = "game-time"
        return top_status,bottom_status,top_id,bottom_id

    def __game_in_progress_status(self,result):
        quarter_missing = not(result.game_quarter) or result.game_quarter == ""
        time_left_missing = not(result.game_time_left) or result.game_time_left == ""

        if quarter_missing and time_left_missing:
            top_status = ""
            bottom_status = "in progress"
            top_id = "status-empty"
            bottom_id = "game-in-progress"
        elif quarter_missing and not(time_left_missing):
            top_status = ""
            bottom_status = result.game_time_left
            top_id = "status-empty"
            bottom_id = "game-time-in-progress"
        elif not(quarter_missing) and time_left_missing:
            top_status = ""
            bottom_status = result.game_quarter
            top_id = "status-empty"
            bottom_id = "game-quarter"
        else:
            top_status = result.game_quarter 
            bottom_status = result.game_time_left
            top_id = "game-quarter"
            bottom_id = "game-time-in-progress"

        return top_status,bottom_status,top_id,bottom_id

    def __game_final_status(self):
        top_status = ""
        bottom_status = "final"
        top_id = "status-empty"
        bottom_id = "game-final"

        return top_status,bottom_status,top_id,bottom_id


    def __get_local_timezone(self):
        # TODO:  change this code to player's preferred timezone
        # TODO:  test view page with a different timezone
        try:
            return self.__timezone
        except AttributeError:
            return pytz.timezone('US/Eastern')


    def set_timezone_for_testing(self,timezone_name):
        self.__timezone = pytz.timezone(timezone_name)


    def get(self,year_param,week_number_param,player_id_param):
        year = int(year_param)
        week_number = int(week_number_param)
        player_id = int(player_id_param)

        database = Database()
        if not(database.is_week_valid(week_number,year)):
            self.error(400)
            self.render("bad_week.html",year=year,week_number=week_number)
            return

        player_key = self.__get_player_key(player_id)

        if not(self.__is_player_id_valid(player_key)):
            self.error(400)
            self.render("bad_player.html",year=year,player_id=player_id,error="bad_id");
            return

        if not(self.__is_player_in_year(player_key,year,database)):
            self.error(400)
            self.render("bad_player.html",year=year,player_id=player_id,error="bad_year");
            return

        u = Update()
        summary, results = u.get_player_results(player_id,year,week_number)

        params = dict()
        params['year'] = year
        params['week_number'] = week_number
        params['weeks_in_year'] = database.get_week_numbers(year)
        params['summary'] = summary
        params['results'] = results

        self.set_game_status_params(params,results)

        self.render("player_results.html",**params)
