from google.appengine.ext import db
import logging
import time

class Database:

    def load_week_data(self,year,week_number):
        week = self.__get_week_in_database(year,week_number)
        games = self.__get_week_games_in_database(week)
        picks = self.__get_player_week_picks_in_database(week)
        return week,games,picks

    def load_week_data_timed(self,year,week_number):
        start = time.time()
        week = self.__get_week_in_database(year,week_number)
        week_elapsed_time = time.time()-start
        start = time.time()
        games = self.__get_week_games_in_database(week)
        games_elapsed_time = time.time()-start
        start = time.time()
        picks = self.__get_player_week_picks_in_database(week)
        picks_elapsed_time = time.time()-start
        logging.info("Load weeks = %f" % (week_elapsed_time))
        logging.info("Load games = %f" % (games_elapsed_time))
        logging.info("Load picks = %f" % (picks_elapsed_time))
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
        players_query = db.GqlQuery('select * from Player where years IN :year',year=[year])
        assert players_query != None
        return list(players_query)

    def __get_player_week_picks_in_database_v2(self,week):
        players = self.__get_players_in_database(week.year)

        week_key = str(week.key())

        player_picks = dict()
        for player in players:
            player_key = str(player.key())

            picks_query = db.GqlQuery('select * from Pick where week=:week and player=:player',week=week_key,player=player_key)
            assert picks_query != None
            picks = list(picks_query) 

            player_picks[player.name] = picks
        return player_picks

    def __get_player_week_picks_in_database(self,week):
        picks_query = db.GqlQuery('select * from Pick where week=:week',week=str(week.key()))
        assert picks_query != None
        picks = list(picks_query) 

        players = self.__get_players_in_database(week.year)

        player_picks = { player.name:[] for player in players }

        # speedup idea: do query for each player's picks instead of all the picks

        for pick in picks:

            # idea:  create key,value dict with player_key,player_name
            # idea:  create key,value dict with player_key,picks array

            player = db.get(db.Key(pick.player))
            player_picks[player.name].append(pick)

        return player_picks
