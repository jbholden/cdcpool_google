class OverallResults:
    rank = None
    projected_rank = None
    player_id = None
    player_name = None
    overall = None
    projected = None
    possible = None
    week_points = None
    last_week_projected = None
    last_week_possible = None

    def get_dict(self):
        d = dict()
        d['rank'] = self.rank
        d['projected_rank'] = self.projected_rank
        d['player_id'] = self.player_id
        d['player_name'] = self.player_name
        d['overall'] = self.overall
        d['projected'] = self.projected
        d['possible'] = self.possible
        d['week_points'] = self.week_points
        d['last_week_projected'] = self.last_week_projected
        d['last_week_possible'] = self.last_week_possible
        return d

class OverallResultsSummary:
    # possible states:  
    # - pool_not_started
    # - pool_in_progress
    #   + week created, no picks made
    #   + picks have been made for the week, games not started
    #   + games in progress
    #   + games complete, week is final
    # - pool_final
    overall_state = None    # not_started, in_progress, final
    last_week_state = None  # not_started, in_progress, final
    winner = None  # TODO remove? ties? nice for json, 2nd place, third place?

    def get_dict(self):
        d = dict()
        d['overall_state'] = self.overall_state
        d['last_week_state'] = self.last_week_state
        d['winner'] = self.winner
        return d
