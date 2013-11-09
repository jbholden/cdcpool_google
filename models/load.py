from games import *
from players import *
from teams import *
from weeks import *
from picks import *
from loadplayers import *
from loadteams import *
from loadweeks import *
from loadpicks import *
from loadgames import *

class LoadDatabase:

    def load_players(self):
        load_players = LoadPlayers()
        player_lookup = load_players.load()

    def load_teams(self):
        load_teams = LoadTeams()
        team_lookup = load_teams.load()

    def load_games(self):
        pass

    def load_weeks(self):
        pass

    def load_picks(self):
        pass

    # this is taking too long?
    def load_all(self):
        load_players = LoadPlayers()
        player_lookup = load_players.load()

        load_teams = LoadTeams()
        team_lookup = load_teams.load()

        load_games = LoadGames(team_lookup)
        game_lookup = load_games.load()

        load_weeks = LoadWeeks(player_lookup,game_lookup)
        week_lookup = load_weeks.load()

        load_picks = LoadPicks(player_lookup,game_lookup,week_lookup)
        pick_lookup = load_picks.load()

    def delete_all(self):
        self.__delete_players()
        self.__delete_teams()
        self.__delete_games()
        self.__delete_weeks()
        self.__delete_picks()

    def __delete_players(self):
        players = Player.all()
        if not(players):
            return
        for player in players:
            db.delete(player)

    def __delete_teams(self):
        teams = Team.all()
        if not(teams):
            return
        for team in teams:
            db.delete(team)

    def __delete_games(self):
        games = Game.all()
        if not(games):
            return
        for game in games:
            db.delete(game)

    def __delete_picks(self):
        picks = Pick.all()
        if not(picks):
            return
        for pick in picks:
            db.delete(pick)

    def __delete_weeks(self):
        weeks = Week.all()
        if not(weeks):
            return
        for week in weeks:
            db.delete(week)
