import webapp2
import logging
from code.update import *
from code.database import *
from handler import *
import string
import re

# TODO:  move quarter/timeleft column values to this class
# TODO:  define base player results and fill in blocks with another html
# TODO: tests
#       + game not started:  view page with a game start date
#       + game not started:  view page with a game start date (different time zones)
#       + game not started:  view page with no game start date

class PlayerResultsPage(Handler):

    def __get_player_key(self,player_id):
        return db.Key.from_path('Player',player_id)

    def __is_player_id_valid(self,player_key):
        return player_key != None

    def __is_player_in_year(self,player_key,year,database):
        players_in_year = database.load_players(year)
        return str(player_key) in players_in_year

    def __get_top_row_game_status(self,result):
        # game not started
        # + no start date
        # + start date
        # game in progress
        # game final
        pass

    def get_game_status(self,result):
        if result.game_state == "not_started":
            return self.__game_not_started_status(result)

    def __game_not_started_status(self,result):
        if result.game_date == None:
            top_status = ""
            bottom_status = ""
            top_id = "status-empty"
            bottom_id = "status-empty"
        else:
            weekday_month_day = "%a %b %d"
            hour_minutes_ampm_timezone = "%I:%M %p %Z"
            top_status = result.game_date.strftime(weekday_month_day)
            bottom_status = result.game_date.strftime(hour_minutes_ampm_timezone)
            top_id = "game-time"
            bottom_id = "game-time"
        return top_status,bottom_status,top_id,bottom_id


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

        self.render("player_results.html",**params)
