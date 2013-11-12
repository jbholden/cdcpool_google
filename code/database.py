from google.appengine.ext import db
import logging
import time

class Database:

    def load_week_data(self,year,week_number):
        start = time.time()
        week = self.__get_week_in_database(year,week_number)
        week_elapsed_time = time.time()-start
        start = time.time()
        games = self.__get_week_games_in_database(week)
        games_elapsed_time = time.time()-start
        start = time.time()
        picks = self.__get_player_week_picks_in_database(week)
        picks_elapsed_time = time.time()-start
        logging.debug("Load weeks = %f" % (week_elapsed_time))
        logging.debug("Load games = %f" % (games_elapsed_time))
        logging.debug("Load picks = %f" % (picks_elapsed_time))
        return week,games,picks

    def __get_week_in_database(self,year,week):
        weeks_query = db.GqlQuery('SELECT * FROM Week WHERE year=:year and number=:week',year=year,week=week)
        assert weeks_query != None
        weeks = list(weeks_query)
        assert len(weeks) == 1
        return weeks[0]

    def __get_week_games_in_database(self,week):
        games = []
        for game_key in week.games:
            games.append(db.get(game_key))
        assert len(games) == 10
        return games

    def __get_players_in_database(self,year):
        players_query = db.GqlQuery('select * from Player where year=:year',year=year)
        assert players_query != None
        return list(players_query)

    def __get_player_week_picks_in_database(self,week):
        start = time.time()
        picks_query = db.GqlQuery('select * from Pick where week=:week',week=week)
        assert picks_query != None
        picks = list(picks_query) 
        elapsed = time.time()-start
        logging.debug("Load picks time 1 = %f" % (elapsed))

        start = time.time()
        players = self.__get_players_in_database(week.year)
        elapsed = time.time()-start
        logging.debug("Load picks time 2 = %f" % (elapsed))

        start = time.time()
        player_picks = { player.name:[] for player in players }
        elapsed = time.time()-start
        logging.debug("Load picks time 3 = %f" % (elapsed))
        start = time.time()
        name_time = 0.0
        dict_time = 0.0
        for pick in picks:

            # idea:  create key,value dict with player_key,player_name
            # idea:  create key,value dict with player_key,picks array

            nstart = time.time()
            player_key = pick.player.key()
            #player_name = str(player_key)
            player_name = db.get(player_key).name
            #player_name = pick.player.name
            elapsed = time.time()-nstart
            name_time += elapsed

            pstart = time.time()
            player_picks[player_name].append(pick)
            elapsed = time.time()-pstart
            dict_time += elapsed
        elapsed = time.time()-start
        logging.debug("Load picks name time = %f" % (name_time))
        logging.debug("Load picks dict time = %f" % (dict_time))
        logging.debug("Load picks time 4 = %f" % (elapsed))

        return player_picks
