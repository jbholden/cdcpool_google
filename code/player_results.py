class PlayerResult:
    player_pick = None
    result = None
    team1 = None
    team2 = None
    team1_score = None
    team2_score = None
    game_state = None
    favored = None
    favored_spread = None
    winning_team = None
    game_spread = None
    game_quarter = None
    game_time_left = None
    game_date = None

    def __get_date_str(self,d):
        if not(d):
            return None
        date_format = "%a %m/%d/%Y %I:%M %p UTC"
        return d.strftime(date_format)

    def get_dict(self):
        d = dict()
        d['player_pick'] = self.player_pick
        d['result'] = self.result
        d['team1'] = self.team1
        d['team2'] = self.team2
        d['team1_score'] = self.team1_score
        d['team2_score'] = self.team2_score
        d['game_state'] = self.game_state
        d['favored'] = self.favored
        d['favored_spread'] = self.favored_spread
        d['winning_team'] = self.winning_team
        d['game_spread'] = self.game_spread
        d['game_quarter'] = self.game_quarter
        d['game_time_left'] = self.game_time_left
        d['game_date'] = self.__get_date_str(self.game_date)
        return d


class PlayerSummary:
    player_id = None
    player_name = None
    wins = None
    losses = None
    win_pct = None
    possible_wins = None
    projected_wins = None
    week_state = None

    def get_dict(self):
        d = dict()
        d['player_id'] = self.player_id
        d['player_name'] = self.player_name
        d['wins'] = self.wins
        d['losses'] = self.losses
        d['win_pct'] = self.win_pct
        d['possible_wins'] = self.possible_wins
        d['projected_wins'] = self.projected_wins
        d['week_state'] = self.week_state
        return d
