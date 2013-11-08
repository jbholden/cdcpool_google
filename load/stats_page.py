import webapp2
from models.games import *
from models.players import *
from models.teams import *
from models.weeks import *
from models.picks import *
from lookups import *

class DatabaseStats(webapp2.RequestHandler):
    def __count_instances(self,name,data):
        s = ''
        if not(data):
            return '%s loaded=0<br>' % (name)
        else:
            return '%s loaded=%d<br>' % (name,data.count())

    def get(self):
        code = '<html><body>'
        code += self.__count_instances('Players',Player.all())
        code += self.__count_instances('Teams',Team.all())
        code += self.__count_instances('Games',Game.all())
        code += self.__count_instances('Weeks',Week.all())
        code += self.__count_instances('Picks',Pick.all())
        code += self.__count_instances('Lookups',Lookup.all())
        code += '</body></html>'
        self.response.write(code)
