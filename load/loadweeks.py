from models.weeks import *

from lookups import *
import datetime
from google.appengine.ext import db

class LoadWeeks:

    def __init__(self):
        self.load()

    def num_transactions(self):
        return len(self.transactions)

    def run_transactions(self,txn_range):
        last_index = self.num_transactions() - 1
        for i in txn_range:
            if i > last_index:
                break
            d = self.transactions[i]
            self.add_week(d)

    def __lookup_winner(self,name,recno):
        if not(name) or not(recno):
            return None
        q = db.GqlQuery('SELECT * FROM Lookup WHERE name=:name and recno=:recno',name=name,recno=recno)
        assert q
        result = list(q)
        assert len(result) == 1
        return db.get(db.Key(result[0].instance_key))

    def __lookup_game(self,name,recno):
        if not(name) or not(recno):
            return None
        q = db.GqlQuery('SELECT * FROM Lookup WHERE name=:name and recno=:recno',name=name,recno=recno)
        assert q
        result = list(q)
        assert len(result) == 1
        return db.Key(result[0].instance_key)

    def add_week(self,week):
        w = Week(number=week['number'],year=week['year'])
        w.winner = self.__lookup_winner('player',week['winner'])
        w.games = [self.__lookup_game('game',id) for id in week['games'] ]
        w.lock_picks = datetime.datetime.now()
        w.lock_scores = datetime.datetime.now()
        key = w.put()
        l = Lookup(name='week',recno=week['recno'],instance_key=str(key))
        l.put()

    def load(self):
        self.transactions = []
        self.transactions.append({'recno':1,'number':1,'year':2012,'winner':36,'games':[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
        self.transactions.append({'recno':2,'number':2,'year':2012,'winner':43,'games':[11, 12, 13, 14, 15, 16, 17, 18, 19, 20]})
        self.transactions.append({'recno':3,'number':3,'year':2012,'winner':21,'games':[21, 22, 23, 24, 25, 26, 27, 28, 29, 30]})
        self.transactions.append({'recno':4,'number':4,'year':2012,'winner':1,'games':[31, 32, 33, 34, 35, 36, 37, 38, 39, 40]})
        self.transactions.append({'recno':5,'number':5,'year':2012,'winner':2,'games':[41, 42, 43, 44, 45, 46, 47, 48, 49, 50]})
        self.transactions.append({'recno':6,'number':6,'year':2012,'winner':47,'games':[51, 52, 53, 54, 55, 56, 57, 58, 59, 60]})
        self.transactions.append({'recno':7,'number':7,'year':2012,'winner':30,'games':[61, 62, 63, 64, 65, 66, 67, 68, 69, 70]})
        self.transactions.append({'recno':8,'number':8,'year':2012,'winner':43,'games':[71, 72, 73, 74, 75, 76, 77, 78, 79, 80]})
        self.transactions.append({'recno':9,'number':9,'year':2012,'winner':4,'games':[81, 82, 83, 84, 85, 86, 87, 88, 89, 90]})
        self.transactions.append({'recno':10,'number':10,'year':2012,'winner':1,'games':[91, 92, 93, 94, 95, 96, 97, 98, 99, 100]})
        self.transactions.append({'recno':11,'number':11,'year':2012,'winner':2,'games':[101, 102, 103, 104, 105, 106, 107, 108, 109, 110]})
        self.transactions.append({'recno':12,'number':12,'year':2012,'winner':5,'games':[111, 112, 113, 114, 115, 116, 117, 118, 119, 120]})
        self.transactions.append({'recno':13,'number':13,'year':2012,'winner':37,'games':[121, 122, 123, 124, 125, 126, 127, 128, 129, 130]})
        self.transactions.append({'recno':14,'number':1,'year':2013,'winner':95,'games':[131, 132, 133, 134, 135, 136, 137, 138, 139, 140]})
        self.transactions.append({'recno':15,'number':2,'year':2013,'winner':58,'games':[141, 142, 143, 144, 145, 146, 147, 148, 149, 150]})
        self.transactions.append({'recno':16,'number':3,'year':2013,'winner':56,'games':[151, 152, 153, 154, 155, 156, 157, 158, 159, 160]})
        self.transactions.append({'recno':17,'number':4,'year':2013,'winner':69,'games':[161, 162, 163, 164, 165, 166, 167, 168, 169, 170]})
        self.transactions.append({'recno':18,'number':5,'year':2013,'winner':74,'games':[171, 172, 173, 174, 175, 176, 177, 178, 179, 180]})
        self.transactions.append({'recno':19,'number':6,'year':2013,'winner':74,'games':[181, 182, 183, 184, 185, 186, 187, 188, 189, 190]})
        self.transactions.append({'recno':20,'number':7,'year':2013,'winner':86,'games':[191, 192, 193, 194, 195, 196, 197, 198, 199, 200]})
        self.transactions.append({'recno':21,'number':8,'year':2013,'winner':58,'games':[201, 202, 203, 204, 205, 206, 207, 208, 209, 210]})
        self.transactions.append({'recno':22,'number':9,'year':2013,'winner':75,'games':[211, 212, 213, 214, 215, 216, 217, 218, 219, 220]})
        self.transactions.append({'recno':23,'number':10,'year':2013,'winner':62,'games':[221, 222, 223, 224, 225, 226, 227, 228, 229, 230]})
        self.transactions.append({'recno':24,'number':11,'year':2013,'winner':76,'games':[231, 232, 233, 234, 235, 236, 237, 238, 239, 240]})
        self.transactions.append({'recno':25,'number':12,'year':2013,'winner':81,'games':[241, 242, 243, 244, 245, 246, 247, 248, 249, 250]})

