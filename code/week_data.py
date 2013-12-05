class WeekData:
    week = None
    games = None
    player_picks = None
    picks = None
    teams = None
    players = None

    def get_game(self,game_key):
        return self.games[game_key]

    def get_pick(self,pick_key):
        return self.picks[pick_key]

    def get_team(self,team_key):
        return self.teams[team_key]

    def get_player(self,player_key):
        return self.players[player_key]

    def get_player_key(self,player_name):
        for player_key in self.players:
            player = self.get_player(player_key)
            if player and player.name == player_name:
                return player_key
        raise AssertionError,"Could not find player %s" % (player_name)

    def get_player_picks(self,player_key):
        return self.player_picks[player_key]

    def get_player_name_picks(self,player_name):
        player_key = self.get_player_key(player_name)
        return self.get_player_picks(player_key)

    def get_team1_name(self,game_key):
        game = self.get_game(game_key)
        team = self.get_team(game.team1)
        return team.name

    def get_team2_name(self,game_key):
        game = self.get_game(game_key)
        team = self.get_team(game.team2)
        return team.name
