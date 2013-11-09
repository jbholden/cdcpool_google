from weeks import *

class LoadWeeks:

    def __init__(self,player_lookup,game_lookup):
        self.__player_lookup = player_lookup
        self.__game_lookup = game_lookup

    def add_week(self,number,year,winner,games):
        w = Week(number=number,year=year)
        w.winner = self.__player_lookup[winner]
        w.games = [self.__game_lookup[id] for id in games ]
        return w.put()

    def load(self):
        lookup = dict()
        lookup[1] = self.add_week(1,2012,36,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        lookup[2] = self.add_week(2,2012,43,[11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
        lookup[3] = self.add_week(3,2012,21,[21, 22, 23, 24, 25, 26, 27, 28, 29, 30])
        lookup[4] = self.add_week(4,2012,1,[31, 32, 33, 34, 35, 36, 37, 38, 39, 40])
        lookup[5] = self.add_week(5,2012,2,[41, 42, 43, 44, 45, 46, 47, 48, 49, 50])
        lookup[6] = self.add_week(6,2012,47,[51, 52, 53, 54, 55, 56, 57, 58, 59, 60])
        lookup[7] = self.add_week(7,2012,30,[61, 62, 63, 64, 65, 66, 67, 68, 69, 70])
        lookup[8] = self.add_week(8,2012,43,[71, 72, 73, 74, 75, 76, 77, 78, 79, 80])
        lookup[9] = self.add_week(9,2012,4,[81, 82, 83, 84, 85, 86, 87, 88, 89, 90])
        lookup[10] = self.add_week(10,2012,1,[91, 92, 93, 94, 95, 96, 97, 98, 99, 100])
        lookup[11] = self.add_week(11,2012,2,[101, 102, 103, 104, 105, 106, 107, 108, 109, 110])
        lookup[12] = self.add_week(12,2012,5,[111, 112, 113, 114, 115, 116, 117, 118, 119, 120])
        lookup[13] = self.add_week(13,2012,37,[121, 122, 123, 124, 125, 126, 127, 128, 129, 130])
        lookup[14] = self.add_week(1,2013,78,[131, 132, 133, 134, 135, 136, 137, 138, 139, 140])
        lookup[15] = self.add_week(2,2013,75,[141, 142, 143, 144, 145, 146, 147, 148, 149, 150])
        lookup[16] = self.add_week(3,2013,63,[151, 152, 153, 154, 155, 156, 157, 158, 159, 160])
        lookup[17] = self.add_week(4,2013,56,[161, 162, 163, 164, 165, 166, 167, 168, 169, 170])
        lookup[18] = self.add_week(5,2013,61,[171, 172, 173, 174, 175, 176, 177, 178, 179, 180])
        lookup[19] = self.add_week(6,2013,61,[181, 182, 183, 184, 185, 186, 187, 188, 189, 190])
        lookup[20] = self.add_week(7,2013,77,[191, 192, 193, 194, 195, 196, 197, 198, 199, 200])
        lookup[21] = self.add_week(8,2013,75,[201, 202, 203, 204, 205, 206, 207, 208, 209, 210])
        return lookup


