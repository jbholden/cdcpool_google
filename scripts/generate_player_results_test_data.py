from xlrd import *
import string

class Data:
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
    game_number = None
    team1_tiebreak = None
    team2_tiebreak = None

class Game:
    number = None
    team1 = None
    team2 = None
    team1_score = None
    team2_score = None
    winner = None
    favored = None
    favored_spread = None
    game_winner = None
    game_spread = None


class TestDataImport:

    def __init__(self,excel_file,week_number):
        self.__wb = open_workbook(excel_file)
        self.__import_players()
        sheet = self.__get_weekly_sheet(week_number)
        self.__data = dict()
        self.__games = []
        self.__import_games(sheet)
        self.__import_players_picks(sheet)

    def print_code(self):
        for player_name in self.__data:
            for d in self.__data[player_name]:
                s = "        PlayerTestData.add_result(results,"
                s += "player_name='%s'," % (self.__hide_lastname(player_name))
                s += "player_pick=%s," % (self.__fmt(d.player_pick,'string'))
                s += "result=%s," % (self.__fmt(d.result,'string'))
                s += "team1=%s," % (self.__fmt(d.team1,'string'))
                s += "team2=%s," % (self.__fmt(d.team2,'string'))
                s += "team1_score=%s," % (self.__fmt(d.team1_score,'int'))
                s += "team2_score=%s," % (self.__fmt(d.team2_score,'int'))
                s += "game_state=%s," % (self.__fmt(d.game_state,'string'))
                s += "favored=%s," % (self.__fmt(d.favored,'string'))
                s += "favored_spread=%s," % (self.__fmt(d.favored_spread,'float'))
                s += "winning_team=%s," % (self.__fmt(d.winning_team,'string'))
                s += "game_spread=%s," % (self.__fmt(d.game_spread,'int'))
                s += "game_quarter=%s,"% (self.__fmt(d.game_quarter,'string'))
                s += "game_time_left=%s,"% (self.__fmt(d.game_time_left,'string'))
                s += "game_date=%s,"% (self.__fmt(d.game_date,'date'))
                s += "game_number=%s," % (self.__fmt(d.game_number,'int'))
                s += "team1_tiebreak=%s," % (self.__fmt(d.team1_tiebreak,'int'))
                s += "team2_tiebreak=%s" % (self.__fmt(d.team2_tiebreak,'int'))
                s += ')'
                print s

    def __fmt(self,value,value_type="string"):
        if value == None:
            return "None"
        if value_type == "string":
            return "'%s'" % (value)
        if value_type == "int":
            return "%d" % (value)
        if value_type == "float":
            return "%0.1f" % (value)
        if value_type == "date":
            return "'%s'" % (value)

    def __import_players_picks(self,sheet):
        player_row = 1
        first_player_col = 10
        for col in range(first_player_col,sheet.ncols):
            player_name = str(sheet.cell(player_row,col).value)
            if player_name == "":
                break
            self.__import_player_results(sheet,col,player_name)

    def __import_player_results(self,sheet,player_col,player_name):
        if self.__player_default(sheet,player_col):
            self.__create_player_default(player_name)
            return

        first_game_row = 2
        row = first_game_row
        results = []
        for game in self.__games:
            d = Data()
            d.player_pick = self.__get_player_pick(sheet,row,player_col,game)
            d.result = self.__get_result(game,d.player_pick)
            d.team1 = game.team1
            d.team2 = game.team2
            d.team1_score = game.team1_score
            d.team2_score = game.team2_score
            d.game_state = "final"
            d.favored = game.favored
            d.favored_spread = game.favored_spread
            d.winning_team = game.game_winner
            d.game_spread = game.game_spread
            d.game_quarter = None
            d.game_time_left = None
            d.game_date = None
            d.game_number = game.number

            if d.game_number == 10:
                team1_tiebreak,team2_tiebreak = self.__get_tiebreak_score(sheet,player_col)
                d.team1_tiebreak = team1_tiebreak
                d.team2_tiebreak = team2_tiebreak
            else:
                d.team1_tiebreak = None
                d.team2_tiebreak = None

            results.append(d)
            row += 2
        self.__data[player_name] = results

    def __get_tiebreak_score(self,sheet,col):
        team1_score_row = 22 
        team2_score_row = 23
        team1_score = int(float(str(sheet.cell(team1_score_row,col).value)))
        team2_score = int(float(str(sheet.cell(team2_score_row,col).value)))
        return team1_score,team2_score

    def __get_player_pick(self,sheet,row,player_column,game):
        team1_row = row
        team2_row = row + 1
        CELL_EMPTY = 0
        team1_picked = sheet.cell_type(team1_row,player_column) != CELL_EMPTY
        team2_picked = sheet.cell_type(team2_row,player_column) != CELL_EMPTY

        if team1_picked:
            return game.team1
        if team2_picked:
            return game.team2
        import pdb; pdb.set_trace()
        raise AssertionError,"Neither team was picked (and player did not default week)"

    def __get_result(self,game,pick):
        if pick == "":
            return "loss"
        if game.winner == pick:
            return "win"
        return "loss"

    def __create_player_default(self,player_name):
        results = []
        for game in self.__games:
            d = Data()
            d.player_pick = ""
            d.result = "loss"
            d.team1 = game.team1
            d.team2 = game.team2
            d.team1_score = game.team1_score
            d.team2_score = game.team2_score
            d.game_state = "final"
            d.favored = game.favored
            d.favored_spread = game.favored_spread
            d.winning_team = game.game_winner
            d.game_spread = game.game_spread
            d.game_quarter = None
            d.game_time_left = None
            d.game_date = None
            d.game_number = game.number
            d.team1_tiebreak = None
            d.team2_tiebreak = None
            results.append(d)
        self.__data[player_name] = results

    def __import_games(self,sheet):
        game_col = 1
        first_game_row = 2
        winner_col = 4
        score_col = 3
        favorite_col = 2

        self.__games = []
        row = first_game_row
        for game_number in range(1,11):
            team1_row = row
            team2_row = row+1

            g = Game()
            g.number = game_number
            g.team1 = str(sheet.cell(team1_row,game_col).value)
            g.team2 = str(sheet.cell(team2_row,game_col).value)
            g.team1_score = int(float(str(sheet.cell(team1_row,score_col).value)))
            g.team2_score = int(float(str(sheet.cell(team2_row,score_col).value)))

            team1_winner = int(float(str(sheet.cell(team1_row,winner_col).value))) == 1
            team2_winner = int(float(str(sheet.cell(team2_row,winner_col).value))) == 1

            assert team1_winner or team2_winner, "Expected a game winner"

            g.winner = g.team1 if team1_winner else g.team2

            team1_spread = str(sheet.cell(team1_row,favorite_col).value)
            team2_spread = str(sheet.cell(team2_row,favorite_col).value)
            favored,spread = self.__calculate_spread(g,team1_spread,team2_spread)

            g.favored = favored
            g.favored_spread = spread

            if g.team1_score > g.team2_score:
                g.game_winner = g.team1
            else:
                g.game_winner = g.team2

            g.game_spread = abs(g.team1_score-g.team2_score) 

            self.__games.append(g)

            row += 2

    def __calculate_spread(self,game,team1_spread,team2_spread):
        assert self.__spread_errors(team1_spread,team2_spread) == False

        if team1_spread == '':
            favored = game.team2
            spread = float(team2_spread)
        elif team2_spread == '':
            favored = game.team1
            spread = float(team1_spread)
        return favored,spread

    def __spread_errors(self,team1_spread,team2_spread):
        if team1_spread == '' and team2_spread == '':
            return True
        if team1_spread == '':
            try:
                f = float(team2_spread)
                return False
            except ValueError:
                return True
        if team2_spread == '':
            try:
                f = float(team1_spread)
                return False
            except ValueError:
                return True
        return True


    def __import_players(self):
        first_player_row = 7
        player_col = 1

        sheet = self.__get_sheet("Standings")

        players = []
        for row in range(first_player_row,sheet.nrows):
            player_name = str(sheet.cell(row,player_col).value)
            players.append(player_name)
        self.players = players

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


if __name__ == "__main__":
    excel_file = 'pool_2013_standings.xlsm'
    week_number = int(sys.argv[1])
    test_data = TestDataImport(excel_file,week_number)
    test_data.print_code()
