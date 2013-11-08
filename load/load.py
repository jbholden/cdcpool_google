from models.games import *
from models.players import *
from models.teams import *
from models.weeks import *
from models.picks import *
from loadplayers import *
from loadteams import *
from loadweeks import *
from loadpicks import *
from loadgames import *

# this class breaks up the database load into smaller batch sizes.
# google app engine times out in 30 seconds and this is not enough
# time to load the entire database.
class LoadDatabase:

    def __load(self,load,index,batch_size):
        num_txns = load.num_transactions()
        load_all = index == None

        if load_all:
            load.run_transactions(range(num_txns))
            done = True
            return done
        else:
            last = index+batch_size
            load.run_transactions(range(index,last))
            done = last >= num_txns
            return done


    def load_players(self,index=None,batch_size=1):
        return self.__load(LoadPlayers(),index,batch_size)

    def load_teams(self,index=None,batch_size=1):
        return self.__load(LoadTeams(),index,batch_size)

    def load_games(self,index=None,batch_size=1):
        return self.__load(LoadGames(),index,batch_size)

    def load_weeks(self,index=None,batch_size=1):
        return self.__load(LoadWeeks(),index,batch_size)

    def load_picks(self,index=None,batch_size=1):
        return self.__load(LoadPicks(),index,batch_size)

    def load_all(self):
        done = self.load_players()
        done = self.load_teams()
        done = self.load_games()
        done = self.load_weeks()
        done = self.load_picks()

    def delete_all(self):
        self.delete_players()
        self.delete_teams()
        self.delete_games()
        self.delete_weeks()
        self.delete_picks()
        self.delete_lookups()

    def delete_players(self):
        players = Player.all()
        if not(players):
            return
        for player in players:
            db.delete(player)

    def delete_teams(self):
        teams = Team.all()
        if not(teams):
            return
        for team in teams:
            db.delete(team)

    def delete_games(self):
        games = Game.all()
        if not(games):
            return
        for game in games:
            db.delete(game)

    def delete_picks(self):
        picks = Pick.all()
        if not(picks):
            return
        for pick in picks:
            db.delete(pick)

    def delete_weeks(self):
        weeks = Week.all()
        if not(weeks):
            return
        for week in weeks:
            db.delete(week)

    def delete_lookups(self):
        lookups = Lookup.all()
        if not(lookups):
            return
        for lookup in lookups:
            db.delete(lookup)
