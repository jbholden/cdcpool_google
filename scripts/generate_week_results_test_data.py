from xlrd import *
import string

class Data:
    rank = None
    projected_rank = None
    player_name = None
    wins = None
    losses = None
    win_pct = None
    projected_wins = None
    possible_wins = None
    winner = None

class TestDataImport:

    def __init__(self,excel_file,week_number):
        self.__wb = open_workbook(excel_file)
        self.__import_players()
        self.__import_week(week_number)
        self.__setup_data()

    def __setup_data(self):
        data = []
        for player_name in self.players:
            d = Data()
            d.rank = 1
            d.projected_rank = 1
            d.player_name = player_name
            d.wins = self.points[player_name]
            d.losses = 10-d.wins
            d.win_pct = self.__get_win_pct(d.wins,d.losses)
            d.projected_wins = d.wins
            d.possible_wins = d.wins

            if player_name == self.winner:
                d.winner = player_name

            data.append(d)

        self.data = self.__assign_rank(data,self.winner)


    def print_code(self):
        for d in self.data:
            s = "        TestData.add_result(week,results,rank=%d,projected_rank=%d," % (d.rank,d.projected_rank)
            s += "player_name='%s'," % (self.__hide_lastname(d.player_name))
            s += "wins=%d,losses=%d,win_pct=%f," % (d.wins,d.losses,d.win_pct)
            s += "projected_wins=%d,possible_wins=%d" % (d.projected_wins,d.possible_wins)
            if d.winner != None:
                s += ",winner='%s'" % (self.__hide_lastname(d.winner))
            s += ')'
            print s

    def __import_players(self):
        first_player_row = 7
        player_col = 1

        sheet = self.__get_sheet("Standings")

        players = []
        for row in range(first_player_row,sheet.nrows):
            player_name = str(sheet.cell(row,player_col).value)
            players.append(player_name)
        self.players = players

    def __import_week(self,week):
        player_row = 1
        first_player_col = 10
        points_row = 24
        winner_row = 27
        winner_label_column = 1
        sheet = self.__get_weekly_sheet(week)

        # just verify winner row is correct
        assert str(sheet.cell(winner_row,winner_label_column).value) == "WINNER"

        points = dict()
        winner = None
        num_winners = 0
        for col in range(first_player_col,sheet.ncols):
            player_name = str(sheet.cell(player_row,col).value)
            if player_name == "":
                break

            if self.__player_default(sheet,col):
                player_points = 0.0
            elif week == 9 and player_name == "Carter, Chris":
                player_points = 6.0    # fix bug reading the excel sheet
            else:
                player_points = str(sheet.cell(points_row,col).value)
            points[player_name] = int(float(player_points))

            s = str(sheet.cell(winner_row,col).value)
            player_won = s != "" and float(s) == 1.0
            if player_won:
                num_winners += 1
                winner = player_name

        assert num_winners == 1
        self.winner = winner
        self.points = points

    def __player_default(self,sheet,player_col):
        tiebreak_score_team1_row = 22
        tiebreak_score_team2_row = 23

        team1_score = str(sheet.cell(tiebreak_score_team1_row,player_col).value)
        team2_score = str(sheet.cell(tiebreak_score_team2_row,player_col).value)

        return team1_score == '' or team2_score == ''

    def __hide_lastname(self,name):
        words = name.split(',')
        assert len(words) == 2
        last_name = words[0].strip()
        first_name = self.__remove_remote_and_middle_name(words[1]).strip()
        conflicting_names = self.__adjust_for_same_name(last_name)
        if conflicting_names == None:
            return "%s %s." % (first_name,last_name[0])
        else:
            return conflicting_names

    def __adjust_for_same_name(self,last_name):
        if last_name == "Ferguson":
            return "Scott Fe."
        if last_name == "Freedman":
            return "Scott Fr."
        return None

    def __remove_remote_and_middle_name(self,name):
        words = name.strip().split(' ')
        assert len(words) > 0
        return string.replace(words[0],"Remote","").strip()

    def __get_sheet(self,name):
        for sheet in self.__wb.sheets():
            if sheet.name == name:
                break
        return sheet

    def __get_weekly_sheet(self,week):
        sheet_name = self.__get_weekly_sheet_name(week)
        return self.__get_sheet(sheet_name)

    def __get_weekly_sheet_name(self,week):
        name = "Wk"
        if week < 10:
            name += "0"
        name += str(week)
        return name

    def __get_win_pct(self,wins,losses):
        total = wins+losses
        if total == 0:
            return 0.00
        return float(wins) / float(total)

    def __assign_rank(self,results,winner=None):
        sorted_by_losses = sorted(results,key=lambda result:result.losses)
        sorted_results = sorted(sorted_by_losses,key=lambda result:result.wins,reverse=True)

        assigned_results = []

        if winner:
            self.__move_winner_to_top_of_results(sorted_results,winner)
            next_rank = 2   # no ties for first place
        else:
            next_rank = 1   # there can be ties for first place

        wins = sorted_results[0].wins
        losses = sorted_results[0].losses

        for i,player_result in enumerate(sorted_results):

            first_place = i == 0
            second_place = i == 1

            if first_place:
                player_result.rank = 1
                player_result.projected_rank = 1
                assigned_results.append(player_result)
                continue

            if second_place and winner:
                player_result.rank = 2
                player_result.projected_rank = 2
                wins = player_result.wins
                losses = player_result.losses
            else:
                record_changed = player_result.wins != wins or player_result.losses != losses

                if record_changed:
                    next_rank = i+1
                    player_result.rank = next_rank
                    player_result.projected_rank = next_rank
                    wins = player_result.wins
                    losses = player_result.losses
                else:
                    player_result.rank = next_rank
                    player_result.projected_rank = next_rank

            assigned_results.append(player_result)

        return assigned_results

    def __move_winner_to_top_of_results(self,results,winner):
        winner_index = None
        for i,player in enumerate(results):
            if player.player_name == winner:
                winner_index = i
        assert winner_index != None,"Could not find the winning player in the results"
        results.insert(0,results.pop(winner_index))

if __name__ == "__main__":
    excel_file = 'pool_2013_standings.xlsm'
    week_number = int(sys.argv[1])
    test_data = TestDataImport(excel_file,week_number)
    test_data.print_code()

