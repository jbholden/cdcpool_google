from google.appengine.ext import db

class Database:

    def load_week_data(self,year,week_number):
        week = self.__get_week_in_database(year,week_number)
        games = self.__get_week_games_in_database(week)
        picks = self.__get_player_week_picks_in_database(week)
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

    def __get_player_week_picks_in_database(self,week):
        picks_query = db.GqlQuery('SELECT * FROM Pick WHERE week=:week',week=week)
        assert picks_query != None
        picks = list(picks_query)

        player_picks = dict()
        for pick in picks:
            if pick.player.name not in player_picks:
                player_picks[pick.player.name] = [ pick ]
            else:
                player_picks[pick.player.name].append(pick)

        return player_picks
