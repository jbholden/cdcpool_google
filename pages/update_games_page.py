import webapp2
import logging
from code.update import *
from code.database import *
from handler import *
import string
import re
from utils.utils import *

class BadInputException(Exception):
    def __init__(self,errmsg):
        self.errmsg = errmsg


class UpdateGamesPage(Handler):

    def get(self,year_param,week_number_param):
        year = int(year_param)
        week_number = int(week_number_param)

        weeks_in_year = self.__get_weeks_in_year(year,week_number)
        if not(weeks_in_year):
            self.error(400)
            self.render("bad_week.html",year=year,week_number=week_number)
            return

        u = Update()

        params = dict()
        params['year'] = year
        params['week_number'] = week_number
        params['weeks_in_year'] = weeks_in_year
        params['games'] = u.get_week_games(year,week_number)
        params['locked'] = self.__is_week_scores_locked(year,week_number)

        self.render("update_games.html",**params)

    def post(self,year_param,week_number_param):
        year = int(year_param)
        week_number = int(week_number_param)

        weeks_in_year = self.__get_weeks_in_year(year,week_number)
        if not(weeks_in_year):
            self.error(400)
            self.render("bad_week.html",year=year,week_number=week_number)
            return

        cancel_clicked = self.request.get("cancel_form")
        if cancel_clicked:
            self.redirect("results")
            return

        submit_clicked = self.request.get("submit_form")
        if not submit_clicked:
            self.error(400)
            errmsg = "Unexpected Error!  Expected submit button to be clicked but wasn't"
            self.render("error_message.html",message=errmsg)
            return

        if self.__is_week_scores_locked(year,week_number):
            self.error(400)
            errmsg = "The scores for %d Week %d are locked." % (year,week_number)
            self.render("error_message.html",message=errmsg)
            return


        u = Update()
        week_games = u.get_week_games(year,week_number)

        try:
            for game_number in range(1,11):
                input_data = self.__get_game_input_data(game_number)

                index = game_number - 1
                assert week_games[index].number == game_number

                week_games[index].team1_score = input_data['team1_score']
                week_games[index].team2_score = input_data['team2_score']
                week_games[index].quarter = input_data['quarter']
                week_games[index].time_left = input_data['time_left']
                week_games[index].state = input_data['state']

        except BadInputException as e:
            self.error(400)
            self.render("error_message.html",message=e.errmsg)
            return

        u.update_week_games(year,week_number,week_games)
        self.redirect("results")

    def __is_week_scores_locked(self,year,week_number):
        d = Database()
        data = d.load_week_data(year,week_number)
        lock_date_utc = data.week.lock_scores
        if lock_date_utc == None:
            return False

        current_time = get_current_time_in_utc()

        return current_time >= lock_date_utc


    def __get_game_input_data(self,game_number):
        team1_score_input = "team1_score_%d" % (game_number)
        quarter_input = "quarter_%d" % (game_number)
        team2_score_input = "team2_score_%d" % (game_number)
        time_input = "time_%d" % (game_number)
        final_input = "final_%d" % (game_number)

        data = dict()

        team1_score_str = self.request.get(team1_score_input)
        team2_score_str = self.request.get(team2_score_input)
        final_checked_str = self.request.get(final_input)

        final_checked = final_checked_str == "checked"

        data['quarter'] = self.request.get(quarter_input)
        data['time_left'] = self.request.get(time_input)
        data['team1_score'] = self.__convert_score_to_int(game_number,1,team1_score_str)
        data['team2_score'] = self.__convert_score_to_int(game_number,2,team2_score_str)

        scores_blank = data['team1_score'] == "" or data['team2_score'] == ""
        not_started = not final_checked and scores_blank
        in_progress = not final_checked and not scores_blank
        final = final_checked

        if not_started:
            data['state'] = "not_started"
            data['quarter'] = ""
            data['team1_score'] = ""
            data['team2_score'] = ""
        elif in_progress:
            data['state'] = "in_progress"
        elif final:
            data['state'] = "final"
            data['quarter'] = ""
            data['time_left'] = ""

        return data


    def __convert_score_to_int(self,game_number,team,score_str):
        if score_str == None or score_str == "":
            return ""

        try:
            score = int(score_str)
        except ValueError:
            raise BadInputException("Game %d Team %d score must be blank or an Integer" % (game_number,team))

        return score


    def __get_weeks_in_year(self,year,week_number):
        d = Database()
        weeks_and_years = d.load_weeks_and_years()
        if self.__invalid_year_or_week_number(weeks_and_years,year,week_number):
            return None
        weeks_in_year = sorted(weeks_and_years[year])
        return weeks_in_year

    def __invalid_year_or_week_number(self,weeks_and_years,year,week_number):
        weeks_in_year = weeks_and_years.get(year)
        if not(weeks_in_year):
            return True
        return week_number not in weeks_in_year
