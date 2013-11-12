from models.players import *

from lookups import *

class LoadPlayers:

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
            self.add_player(recno=d['recno'],name=d['name'],year=d['year'])

    def __lookup_player(self,name):
        q = db.GqlQuery('SELECT * FROM Player WHERE name=:name',name=name)
        if not q:
            return None
        result = list(q)
        if len(result) < 1:
            return None
        assert len(result) == 1
        return q[0]

    def add_player(self,recno,name,year):
        existing_player = self.__lookup_player(name)
        if not existing_player:
            p = Player(name=name,years=[year])
            key = p.put()
            l = Lookup(name='player',recno=recno,instance_key=str(key))
            l.put()
        else:
            existing_player.years.append(year)
            key = existing_player.put()
            l = Lookup(name='player',recno=recno,instance_key=str(key))
            l.put()

    def load(self):
        self.transactions = []
        self.transactions.append({'recno':1,'name':'Jeffrey S.','year':2012})
        self.transactions.append({'recno':2,'name':'Adam S.','year':2012})
        self.transactions.append({'recno':3,'name':'David R.','year':2012})
        self.transactions.append({'recno':4,'name':'Thai N.','year':2012})
        self.transactions.append({'recno':5,'name':'Dale R.','year':2012})
        self.transactions.append({'recno':6,'name':'Amos C.','year':2012})
        self.transactions.append({'recno':7,'name':'Landon A.','year':2012})
        self.transactions.append({'recno':8,'name':'Scott D.','year':2012})
        self.transactions.append({'recno':9,'name':'Jerome B.','year':2012})
        self.transactions.append({'recno':10,'name':'Adam G.','year':2012})
        self.transactions.append({'recno':11,'name':'David B.','year':2012})
        self.transactions.append({'recno':12,'name':'Chris F.','year':2012})
        self.transactions.append({'recno':13,'name':'Dave L.','year':2012})
        self.transactions.append({'recno':14,'name':'Kevin F.','year':2012})
        self.transactions.append({'recno':15,'name':'Byron R.','year':2012})
        self.transactions.append({'recno':16,'name':'Kevin S.','year':2012})
        self.transactions.append({'recno':17,'name':'Chris C.','year':2012})
        self.transactions.append({'recno':18,'name':'Christopher E.','year':2012})
        self.transactions.append({'recno':19,'name':'Martin B.','year':2012})
        self.transactions.append({'recno':20,'name':'Simon C.','year':2012})
        self.transactions.append({'recno':21,'name':'Scott Fe.','year':2012})
        self.transactions.append({'recno':22,'name':'Charles N.','year':2012})
        self.transactions.append({'recno':23,'name':'Tim P.','year':2012})
        self.transactions.append({'recno':24,'name':'David S.','year':2012})
        self.transactions.append({'recno':25,'name':'Daniel D.','year':2012})
        self.transactions.append({'recno':26,'name':'LaMar P.','year':2012})
        self.transactions.append({'recno':27,'name':'Chip A.','year':2012})
        self.transactions.append({'recno':28,'name':'Brent H.','year':2012})
        self.transactions.append({'recno':29,'name':'Larry J.','year':2012})
        self.transactions.append({'recno':30,'name':'Matt H.','year':2012})
        self.transactions.append({'recno':31,'name':'Steve M.','year':2012})
        self.transactions.append({'recno':32,'name':'William M.','year':2012})
        self.transactions.append({'recno':33,'name':'Michael N.','year':2012})
        self.transactions.append({'recno':34,'name':'Todd W.','year':2012})
        self.transactions.append({'recno':35,'name':'Steve W.','year':2012})
        self.transactions.append({'recno':36,'name':'Carlos E.','year':2012})
        self.transactions.append({'recno':37,'name':'Leslie F.','year':2012})
        self.transactions.append({'recno':38,'name':'Robert J.','year':2012})
        self.transactions.append({'recno':39,'name':'Nick E.','year':2012})
        self.transactions.append({'recno':40,'name':'Brandon G.','year':2012})
        self.transactions.append({'recno':41,'name':'Jason H.','year':2012})
        self.transactions.append({'recno':42,'name':'Chris R.','year':2012})
        self.transactions.append({'recno':43,'name':'Brantley B.','year':2012})
        self.transactions.append({'recno':44,'name':'Douglas M.','year':2012})
        self.transactions.append({'recno':45,'name':'Kevin M.','year':2012})
        self.transactions.append({'recno':46,'name':'Moises P.','year':2012})
        self.transactions.append({'recno':47,'name':'Brooker S.','year':2012})
        self.transactions.append({'recno':48,'name':'Jarred W.','year':2012})
        self.transactions.append({'recno':49,'name':'Kenneth Y.','year':2012})
        self.transactions.append({'recno':50,'name':'Van S.','year':2012})
        self.transactions.append({'recno':51,'name':'Carl S.','year':2012})
        self.transactions.append({'recno':52,'name':'Greg I.','year':2012})
        self.transactions.append({'recno':53,'name':'Seth W.','year':2012})
        self.transactions.append({'recno':54,'name':'Rob N.','year':2012})
        self.transactions.append({'recno':55,'name':'Marwan K.','year':2012})
        self.transactions.append({'recno':56,'name':'Van S.','year':2013})
        self.transactions.append({'recno':57,'name':'Alexander M.','year':2013})
        self.transactions.append({'recno':58,'name':'Matt H.','year':2013})
        self.transactions.append({'recno':59,'name':'Amos C.','year':2013})
        self.transactions.append({'recno':60,'name':'Amber N.','year':2013})
        self.transactions.append({'recno':61,'name':'Michael N.','year':2013})
        self.transactions.append({'recno':62,'name':'Dale R.','year':2013})
        self.transactions.append({'recno':63,'name':'David B.','year':2013})
        self.transactions.append({'recno':64,'name':'Simon C.','year':2013})
        self.transactions.append({'recno':65,'name':'Scott Fe.','year':2013})
        self.transactions.append({'recno':66,'name':'Larry J.','year':2013})
        self.transactions.append({'recno':67,'name':'David S.','year':2013})
        self.transactions.append({'recno':68,'name':'Greg I.','year':2013})
        self.transactions.append({'recno':69,'name':'Jeffrey S.','year':2013})
        self.transactions.append({'recno':70,'name':'Steve W.','year':2013})
        self.transactions.append({'recno':71,'name':'Leslie F.','year':2013})
        self.transactions.append({'recno':72,'name':'Brandon G.','year':2013})
        self.transactions.append({'recno':73,'name':'Steve M.','year':2013})
        self.transactions.append({'recno':74,'name':'Thai N.','year':2013})
        self.transactions.append({'recno':75,'name':'Seth W.','year':2013})
        self.transactions.append({'recno':76,'name':'Christopher E.','year':2013})
        self.transactions.append({'recno':77,'name':'Chris F.','year':2013})
        self.transactions.append({'recno':78,'name':'Charles N.','year':2013})
        self.transactions.append({'recno':79,'name':'Byron R.','year':2013})
        self.transactions.append({'recno':80,'name':'Martin B.','year':2013})
        self.transactions.append({'recno':81,'name':'Kevin F.','year':2013})
        self.transactions.append({'recno':82,'name':'Brent H.','year':2013})
        self.transactions.append({'recno':83,'name':'Chip A.','year':2013})
        self.transactions.append({'recno':84,'name':'Daniel D.','year':2013})
        self.transactions.append({'recno':85,'name':'Nick E.','year':2013})
        self.transactions.append({'recno':86,'name':'Dave L.','year':2013})
        self.transactions.append({'recno':87,'name':'Chris R.','year':2013})
        self.transactions.append({'recno':88,'name':'Jarred W.','year':2013})
        self.transactions.append({'recno':89,'name':'Chris C.','year':2013})
        self.transactions.append({'recno':90,'name':'Kevin M.','year':2013})
        self.transactions.append({'recno':91,'name':'Aaron P.','year':2013})
        self.transactions.append({'recno':92,'name':'Carl S.','year':2013})
        self.transactions.append({'recno':93,'name':'Adam S.','year':2013})
        self.transactions.append({'recno':94,'name':'Robert J.','year':2013})
        self.transactions.append({'recno':95,'name':'William M.','year':2013})
        self.transactions.append({'recno':96,'name':'Adam G.','year':2013})
        self.transactions.append({'recno':97,'name':'Douglas M.','year':2013})
        self.transactions.append({'recno':98,'name':'LaMar P.','year':2013})
        self.transactions.append({'recno':99,'name':'Kevin S.','year':2013})
        self.transactions.append({'recno':100,'name':'Kenneth Y.','year':2013})
        self.transactions.append({'recno':101,'name':'Landon A.','year':2013})
        self.transactions.append({'recno':102,'name':'Scott Fr.','year':2013})
        self.transactions.append({'recno':103,'name':'Scott D.','year':2013})
        self.transactions.append({'recno':104,'name':'William C.','year':2013})
        self.transactions.append({'recno':105,'name':'Jeremy H.','year':2013})
        self.transactions.append({'recno':106,'name':'Tim P.','year':2013})
        self.transactions.append({'recno':107,'name':'Jerome B.','year':2013})
        self.transactions.append({'recno':108,'name':'David R.','year':2013})
        self.transactions.append({'recno':109,'name':'Moises P.','year':2013})
        self.transactions.append({'recno':110,'name':'Rob N.','year':2013})

