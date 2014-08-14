import logging
import unittest
import urllib
import urllib2
import datetime
from code.api import *
from code.database import *
import socket
from google.appengine.api import urlfetch
from google.appengine.ext import db
from google.appengine.api import memcache

class TestUpdateGames(unittest.TestCase):

    def test_not_started(self):
        post_data = self.__create_form_with_all_games_not_started()
        self.__http_post('/2013/week/1/games',post_data)
        self.__verify_games_not_started()

    def test_edit_scores(self):
        post_data = self.__create_form_with_scores_edited()
        self.__http_post('/2013/week/1/games',post_data)
        self.__verify_game_scores()

    def test_edit_quarter_and_time(self):
        post_data = self.__create_form_with_quarter_time_edited()
        self.__http_post('/2013/week/1/games',post_data)
        self.__verify_game_quarter_time()

    def test_all_final(self):
        post_data = self.__create_form_with_final_games()
        self.__http_post('/2013/week/1/games',post_data)
        self.__verify_final_games()

    def setUp(self):
        self.hostname = socket.gethostname()
        urlfetch.set_default_fetch_deadline(60)
        self.__saved_games = self.__get_week_games(2013,1)
        self.__modify_week_winner(2013,1)

    def tearDown(self):
        api = API()

        games = self.__get_week_games(2013,1)
        for game in games:
            saved_game = self.__find_game(self.__saved_games,game.number)

            changed = False

            data = dict()

            if game.team1_score != saved_game.team1_score:
                data['team1_score'] = saved_game.team1_score
                changed = True

            if game.team2_score != saved_game.team2_score:
                data['team2_score'] = saved_game.team2_score
                changed = True

            if game.state != saved_game.state:
                data['state'] = saved_game.state
                changed = True

            if game.quarter != saved_game.quarter:
                data['quarter'] = saved_game.quarter
                changed = True

            if game.time_left != saved_game.time_left:
                data['time_left'] = saved_game.time_left
                changed = True

            if game.date != saved_game.date:
                data['date'] = saved_game.date
                changed = True

            if changed:
                game_key = game.key()
                api.edit_game_by_key(game_key,data)

        d = Database()
        d.update_games(2013,1)
        memcache.delete("week_games_2013_1")
        api.delete_games_cache()

        self.__restore_week_winner()


    def __find_game(self,games,number):
        for game in games:
            if game.number == number:
                return game
        return None

        

    def __verify_games_not_started(self):
        key = "games_2013_1"
        games = memcache.get(key)
        self.assertEquals(len(games),10)
        for game in games.values():
            self.assertEquals(game.state,"not_started")
            self.assertEquals(game.team1_score,None)
            self.assertEquals(game.team2_score,None)

    def __verify_final_games(self):
        # verify cache changed
        key = "games_2013_1"
        games = memcache.get(key)
        self.__verify_final_game_attributes(games.values())

        #v verify database changed
        games = self.__get_week_games(2013,1)
        self.__verify_final_game_attributes(games)


    def __verify_final_game_attributes(self,games):
        self.assertEquals(len(games),10)
        games_sorted = sorted(games,key=lambda game:game.number)

        game1 = games_sorted[0]
        game2 = games_sorted[1]
        game3 = games_sorted[2]
        game4 = games_sorted[3]
        game5 = games_sorted[4]
        game6 = games_sorted[5]
        game7 = games_sorted[6]
        game8 = games_sorted[7]
        game9 = games_sorted[8]
        game10 = games_sorted[9]

        self.assertEquals(game1.number,1)
        self.assertEquals(game1.state,"final")
        self.assertEquals(game1.team1_score,10)
        self.assertEquals(game1.team2_score,11)

        self.assertEquals(game2.number,2)
        self.assertEquals(game2.state,"final")
        self.assertEquals(game2.team1_score,33)
        self.assertEquals(game2.team2_score,42)

        self.assertEquals(game3.number,3)
        self.assertEquals(game3.state,"final")
        self.assertEquals(game3.team1_score,7)
        self.assertEquals(game3.team2_score,10)

        self.assertEquals(game4.number,4)
        self.assertEquals(game4.state,"final")
        self.assertEquals(game4.team1_score,14)
        self.assertEquals(game4.team2_score,23)

        self.assertEquals(game5.number,5)
        self.assertEquals(game5.state,"final")
        self.assertEquals(game5.team1_score,7)
        self.assertEquals(game5.team2_score,13)

        self.assertEquals(game6.number,6)
        self.assertEquals(game6.state,"final")
        self.assertEquals(game6.team1_score,21)
        self.assertEquals(game6.team2_score,30)

        self.assertEquals(game7.number,7)
        self.assertEquals(game7.state,"final")
        self.assertEquals(game7.team1_score,13)
        self.assertEquals(game7.team2_score,7)

        self.assertEquals(game8.number,8)
        self.assertEquals(game8.state,"final")
        self.assertEquals(game8.team1_score,31)
        self.assertEquals(game8.team2_score,3)

        self.assertEquals(game9.number,9)
        self.assertEquals(game9.state,"final")
        self.assertEquals(game9.team1_score,40)
        self.assertEquals(game9.team2_score,0)

        self.assertEquals(game10.number,10)
        self.assertEquals(game10.state,"final")
        self.assertEquals(game10.team1_score,3)
        self.assertEquals(game10.team2_score,8)


    def __verify_game_scores(self):
        key = "games_2013_1"
        games = memcache.get(key)
        self.assertEquals(len(games),10)
        games_sorted = sorted(games.values(),key=lambda game:game.number)

        game1 = games_sorted[0]
        game2 = games_sorted[1]
        game3 = games_sorted[2]
        game4 = games_sorted[3]
        game5 = games_sorted[4]
        game6 = games_sorted[5]
        game7 = games_sorted[6]
        game8 = games_sorted[7]
        game9 = games_sorted[8]
        game10 = games_sorted[9]

        self.assertEquals(game1.number,1)
        self.assertEquals(game1.state,"in_progress")
        self.assertEquals(game1.team1_score,10)
        self.assertEquals(game1.team2_score,11)

        self.assertEquals(game2.number,2)
        self.assertEquals(game2.state,"in_progress")
        self.assertEquals(game2.team1_score,33)
        self.assertEquals(game2.team2_score,42)

        self.assertEquals(game3.number,3)
        self.assertEquals(game3.state,"in_progress")
        self.assertEquals(game3.team1_score,7)
        self.assertEquals(game3.team2_score,10)

        self.assertEquals(game4.number,4)
        self.assertEquals(game4.state,"in_progress")
        self.assertEquals(game4.team1_score,14)
        self.assertEquals(game4.team2_score,23)

        self.assertEquals(game5.number,5)
        self.assertEquals(game5.state,"in_progress")
        self.assertEquals(game5.team1_score,7)
        self.assertEquals(game5.team2_score,13)

        self.assertEquals(game6.number,6)
        self.assertEquals(game6.state,"in_progress")
        self.assertEquals(game6.team1_score,21)
        self.assertEquals(game6.team2_score,30)

        self.assertEquals(game7.number,7)
        self.assertEquals(game7.state,"in_progress")
        self.assertEquals(game7.team1_score,13)
        self.assertEquals(game7.team2_score,7)

        self.assertEquals(game8.number,8)
        self.assertEquals(game8.state,"in_progress")
        self.assertEquals(game8.team1_score,31)
        self.assertEquals(game8.team2_score,3)

        self.assertEquals(game9.number,9)
        self.assertEquals(game9.state,"in_progress")
        self.assertEquals(game9.team1_score,40)
        self.assertEquals(game9.team2_score,0)

        self.assertEquals(game10.number,10)
        self.assertEquals(game10.state,"in_progress")
        self.assertEquals(game10.team1_score,3)
        self.assertEquals(game10.team2_score,8)

    def __verify_game_quarter_time(self):
        key = "games_2013_1"
        games = memcache.get(key)
        self.assertEquals(len(games),10)
        games_sorted = sorted(games.values(),key=lambda game:game.number)

        game1 = games_sorted[0]
        game2 = games_sorted[1]
        game3 = games_sorted[2]
        game4 = games_sorted[3]
        game5 = games_sorted[4]
        game6 = games_sorted[5]
        game7 = games_sorted[6]
        game8 = games_sorted[7]
        game9 = games_sorted[8]
        game10 = games_sorted[9]

        self.assertEquals(game1.number,1)
        self.assertEquals(game1.state,"in_progress")
        self.assertEquals(game1.quarter,"1st")
        self.assertEquals(game1.time_left,"5:00")

        self.assertEquals(game2.number,2)
        self.assertEquals(game2.state,"in_progress")
        self.assertEquals(game2.quarter,"2nd")
        self.assertEquals(game2.time_left,"4:01")

        self.assertEquals(game3.number,3)
        self.assertEquals(game3.state,"in_progress")
        self.assertEquals(game3.quarter,"3rd")
        self.assertEquals(game3.time_left,"3:10")

        self.assertEquals(game4.number,4)
        self.assertEquals(game4.state,"in_progress")
        self.assertEquals(game4.quarter,"4th")
        self.assertEquals(game4.time_left,"2:20")

        self.assertEquals(game5.number,5)
        self.assertEquals(game5.state,"in_progress")
        self.assertEquals(game5.quarter,"OT")
        self.assertEquals(game5.time_left,"1:30")

        self.assertEquals(game6.number,6)
        self.assertEquals(game6.state,"in_progress")
        self.assertEquals(game6.quarter,"2OT")
        self.assertEquals(game6.time_left,"5:40")

        self.assertEquals(game7.number,7)
        self.assertEquals(game7.state,"in_progress")
        self.assertEquals(game7.quarter,"3OT")
        self.assertEquals(game7.time_left,"4:50")

        self.assertEquals(game8.number,8)
        self.assertEquals(game8.state,"in_progress")
        self.assertEquals(game8.quarter,"4OT")
        self.assertEquals(game8.time_left,"3:59")

        self.assertEquals(game9.number,9)
        self.assertEquals(game9.state,"in_progress")
        self.assertEquals(game9.quarter,"Half")
        self.assertEquals(game9.time_left,"2:13")

        self.assertEquals(game10.number,10)
        self.assertEquals(game10.state,"in_progress")
        self.assertEquals(game10.quarter,"2nd")
        self.assertEquals(game10.time_left,"1:00")


    def __create_form_with_all_games_not_started(self):
        post_data = dict()
        for game_number in range(1,11):
            game_data = self.__not_started_game(game_number)
            self.__add_dict(post_data,game_data)
        self.__submit_button(post_data)
        return post_data

    def __create_form_with_quarter_time_edited(self):
        game1 = self.__in_progress_game_qtr_time(1,quarter="1st",time_left="5:00")
        game2 = self.__in_progress_game_qtr_time(2,quarter="2nd",time_left="4:01")
        game3 = self.__in_progress_game_qtr_time(3,quarter="3rd",time_left="3:10")
        game4 = self.__in_progress_game_qtr_time(4,quarter="4th",time_left="2:20")
        game5 = self.__in_progress_game_qtr_time(5,quarter="OT",time_left="1:30")
        game6 = self.__in_progress_game_qtr_time(6,quarter="2OT",time_left="5:40")
        game7 = self.__in_progress_game_qtr_time(7,quarter="3OT",time_left="4:50")
        game8 = self.__in_progress_game_qtr_time(8,quarter="4OT",time_left="3:59")
        game9 = self.__in_progress_game_qtr_time(9,quarter="Half",time_left="2:13")
        game10 = self.__in_progress_game_qtr_time(10,quarter="2nd",time_left="1:00")

        post_data = dict()
        self.__add_dict(post_data,game1)
        self.__add_dict(post_data,game2)
        self.__add_dict(post_data,game3)
        self.__add_dict(post_data,game4)
        self.__add_dict(post_data,game5)
        self.__add_dict(post_data,game6)
        self.__add_dict(post_data,game7)
        self.__add_dict(post_data,game8)
        self.__add_dict(post_data,game9)
        self.__add_dict(post_data,game10)

        self.__submit_button(post_data)

        return post_data

    def __create_form_with_scores_edited(self):
        game1 = self.__in_progress_game(1,10,11)
        game2 = self.__in_progress_game(2,33,42)
        game3 = self.__in_progress_game(3,7,10)
        game4 = self.__in_progress_game(4,14,23)
        game5 = self.__in_progress_game(5,7,13)
        game6 = self.__in_progress_game(6,21,30)
        game7 = self.__in_progress_game(7,13,7)
        game8 = self.__in_progress_game(8,31,3)
        game9 = self.__in_progress_game(9,40,0)
        game10 = self.__in_progress_game(10,3,8)

        post_data = dict()
        self.__add_dict(post_data,game1)
        self.__add_dict(post_data,game2)
        self.__add_dict(post_data,game3)
        self.__add_dict(post_data,game4)
        self.__add_dict(post_data,game5)
        self.__add_dict(post_data,game6)
        self.__add_dict(post_data,game7)
        self.__add_dict(post_data,game8)
        self.__add_dict(post_data,game9)
        self.__add_dict(post_data,game10)

        self.__submit_button(post_data)

        return post_data

    def __create_form_with_final_games(self):
        game1 = self.__final_game(1,10,11)
        game2 = self.__final_game(2,33,42)
        game3 = self.__final_game(3,7,10)
        game4 = self.__final_game(4,14,23)
        game5 = self.__final_game(5,7,13)
        game6 = self.__final_game(6,21,30)
        game7 = self.__final_game(7,13,7)
        game8 = self.__final_game(8,31,3)
        game9 = self.__final_game(9,40,0)
        game10 = self.__final_game(10,3,8)

        post_data = dict()
        self.__add_dict(post_data,game1)
        self.__add_dict(post_data,game2)
        self.__add_dict(post_data,game3)
        self.__add_dict(post_data,game4)
        self.__add_dict(post_data,game5)
        self.__add_dict(post_data,game6)
        self.__add_dict(post_data,game7)
        self.__add_dict(post_data,game8)
        self.__add_dict(post_data,game9)
        self.__add_dict(post_data,game10)

        self.__submit_button(post_data)

        return post_data

    def __add_dict(self,dict1,dict2):
        for key in dict2:
            dict1[key] = dict2[key]

    def __submit_button(self,post_data):
        post_data['submit_form'] = 'Submit'

    def __not_started_game(self,game_number):
        return self.__set_game_data(game_number,"","","","",False)

    def __in_progress_game(self,game_number,team1_score,team2_score):
        return self.__set_game_data(game_number,str(team1_score),str(team2_score),"","",False)

    def __in_progress_game_qtr_time(self,game_number,quarter,time_left):
        return self.__set_game_data(game_number,str("10"),str("17"),quarter,time_left,False)

    def __final_game(self,game_number,team1_score,team2_score):
        return self.__set_game_data(game_number,str(team1_score),str(team2_score),"","",True)

    def __set_game_data(self,game_number,team1_score,team2_score,quarter,time,final):
        team1_score_field = 'team1_score_%d' % (game_number)
        team2_score_field = 'team2_score_%d' % (game_number)
        quarter_field = 'quarter_%d' % (game_number)
        time_field = 'time_%d' % (game_number)
        final_checkbox = 'final_%d' % (game_number)

        data = dict()
        data[team1_score_field] = team1_score
        data[team2_score_field] = team2_score
        data[quarter_field] = quarter
        data[time_field] = time

        if final:
            data[final_checkbox] = "checked"

        return data

    def __get_week_games(self,year,week_number):
        api = API()
        api.delete_games_cache()
        week = api.get_week_in_year(year,week_number)
        api.delete_games_cache()  # ensure reading directly from database
        games = []
        for game_key in week.games:
            games.append(api.get_game_by_key(game_key))
        return games

    def __modify_week_winner(self,year,week_number):
        api = API()
        self.__saved_week = api.get_week_in_year(year,week_number)
        api.edit_week_by_key(str(self.__saved_week.key()),{'winner':None})
        d = Database()
        d.update_week_cache(year,week_number)

    def __restore_week_winner(self):
        api = API()
        api.edit_week_by_key(str(self.__saved_week.key()),{'winner':self.__saved_week.winner})
        d = Database()
        d.update_week_cache(self.__saved_week.year,self.__saved_week.number)

    def __http_post(self,address,data=None):
        url = "http://%s%s" % (self.hostname,address)
        data_encoded = urllib.urlencode(data)
        try:
            req = urllib2.Request(url,data_encoded)
            response = urllib2.urlopen(req)
        except urllib2.HTTPError,err:
            response = err
        self.assertEquals(response.code,200)

if __name__ == "__main__":
    unittest.main()
