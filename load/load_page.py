import webapp2
from load import *

class LoadAllPage(webapp2.RequestHandler):
    def code(self):
        c = "<html><body>"
        c += "1.&nbsp;<a href='/a/load_players?batch_size=100'>Load Players</a><br>"
        c += "2.&nbsp; <a href='/a/load_teams?batch_size=100'>Load Teams</a><br>"
        c += "3.&nbsp;<a href='/a/load_games?batch_size=100'>Load Games</a><br>"
        c += "4.&nbsp;<a href='/a/load_weeks?batch_size=100'>Load Weeks</a><br>"
        c += "5.&nbsp;<a href='/a/load_picks?batch_size=100'>Load Picks</a><br>"
        c += "6.&nbsp;<a href='/a/delete_lookups'>Delete Lookups (cleanup)</a><br><br>"
        c += "Fix or start over:<br><br>"
        c += "<a href='/a/delete'>Delete All</a><br>"
        c += "<a href='/a/delete_players'>Delete Players</a><br>"
        c += "<a href='/a/delete_teams'>Delete Teams</a><br>"
        c += "<a href='/a/delete_games'>Delete Games</a><br>"
        c += "<a href='/a/delete_weeks'>Delete Weeks</a><br>"
        c += "<a href='/a/delete_picks'>Delete Picks</a><br>"
        c += "</body></html>"
        return c

    def get(self):
        self.response.write(self.code())

class LoadPlayersPage(webapp2.RequestHandler):
    def __load_all(self):
        load = LoadDatabase()
        done = load.load_players()
        return done

    def __load_batch(self,index,batch):
        start_index = 0 if not(index) else int(index)
        batch_size = 0 if not(batch) else int(batch)
        end_index = start_index + batch_size

        load = LoadDatabase()
        done = load.load_players(start_index,batch_size)
        return done,end_index

    def get(self):
        index = self.request.get('index')
        batch = self.request.get('batch_size')
        load_all = not(index) and not(batch)

        if load_all:
            finished = self.__load_all()
        else:
            finished,end_index = self.__load_batch(index,batch)

        if finished:
            self.response.write('Finished loading players.')
        else:
            batch_size = 0 if not(batch) else int(batch)
            code = "<form type='post'>"
            code += "<input type='hidden' name='index' value='%s'>" % (end_index)
            code += "<input type='hidden' name='batch_size' value='%s'>" % (batch_size)
            code += "Load Next Batch&nbsp;"
            code += "<input type='submit' value='next'>"
            code += "</form>"
            self.response.write(code)

    def post(self):
        self.response.write('Redirecting...')
        index = self.request.get("index")
        batch_size = self.request.get("batch_size")
        self.redirect('/a/load_players?index=%s&batch_size=%s' % (index,batch_size))


class LoadTeamsPage(webapp2.RequestHandler):
    def __load_all(self):
        load = LoadDatabase()
        done = load.load_teams()
        return done

    def __load_batch(self,index,batch):
        start_index = 0 if not(index) else int(index)
        batch_size = 0 if not(batch) else int(batch)
        end_index = start_index + batch_size

        load = LoadDatabase()
        done = load.load_teams(start_index,batch_size)
        return done,end_index

    def get(self):
        index = self.request.get('index')
        batch = self.request.get('batch_size')
        load_all = not(index) and not(batch)

        if load_all:
            finished = self.__load_all()
        else:
            finished,end_index = self.__load_batch(index,batch)

        if finished:
            self.response.write('Finished loading teams.')
        else:
            batch_size = 0 if not(batch) else int(batch)
            code = "<form type='post'>"
            code += "<input type='hidden' name='index' value='%s'>" % (end_index)
            code += "<input type='hidden' name='batch_size' value='%s'>" % (batch_size)
            code += "Load Next Batch&nbsp;"
            code += "<input type='submit' value='next'>"
            code += "</form>"
            self.response.write(code)

    def post(self):
        self.response.write('Redirecting...')
        index = self.request.get("index")
        batch_size = self.request.get("batch_size")
        self.redirect('/a/load_teams?index=%s&batch_size=%s' % (index,batch_size))

class LoadGamesPage(webapp2.RequestHandler):
    def __load_all(self):
        load = LoadDatabase()
        done = load.load_games()
        return done

    def __load_batch(self,index,batch):
        start_index = 0 if not(index) else int(index)
        batch_size = 0 if not(batch) else int(batch)
        end_index = start_index + batch_size

        load = LoadDatabase()
        done = load.load_games(start_index,batch_size)
        return done,end_index

    def get(self):
        index = self.request.get('index')
        batch = self.request.get('batch_size')
        load_all = not(index) and not(batch)

        if load_all:
            finished = self.__load_all()
        else:
            finished,end_index = self.__load_batch(index,batch)

        if finished:
            self.response.write('Finished loading games.')
        else:
            batch_size = 0 if not(batch) else int(batch)
            code = "<form type='post'>"
            code += "<input type='hidden' name='index' value='%s'>" % (end_index)
            code += "<input type='hidden' name='batch_size' value='%s'>" % (batch_size)
            code += "Load Next Batch&nbsp;"
            code += "<input type='submit' value='next'>"
            code += "</form>"
            self.response.write(code)

    def post(self):
        self.response.write('Redirecting...')
        index = self.request.get("index")
        batch_size = self.request.get("batch_size")
        self.redirect('/a/load_games?index=%s&batch_size=%s' % (index,batch_size))


class LoadPicksPage(webapp2.RequestHandler):
    def __load_all(self):
        load = LoadDatabase()
        done = load.load_picks()
        return done

    def __load_batch(self,index,batch):
        start_index = 0 if not(index) else int(index)
        batch_size = 0 if not(batch) else int(batch)
        end_index = start_index + batch_size

        load = LoadDatabase()
        done = load.load_picks(start_index,batch_size)
        return done,end_index

    def get(self):
        index = self.request.get('index')
        batch = self.request.get('batch_size')
        load_all = not(index) and not(batch)

        if load_all:
            finished = self.__load_all()
        else:
            finished,end_index = self.__load_batch(index,batch)

        if finished:
            self.response.write('Finished loading picks.')
        else:
            batch_size = 0 if not(batch) else int(batch)
            code = "<form type='post'>"
            code += "<input type='hidden' name='index' value='%s'>" % (end_index)
            code += "<input type='hidden' name='batch_size' value='%s'>" % (batch_size)
            code += "Load Next Batch&nbsp;"
            code += "<input type='submit' value='next'>"
            code += "</form>"
            self.response.write(code)

    def post(self):
        self.response.write('Redirecting...')
        index = self.request.get("index")
        batch_size = self.request.get("batch_size")
        self.redirect('/a/load_picks?index=%s&batch_size=%s' % (index,batch_size))


class LoadWeeksPage(webapp2.RequestHandler):
    def __load_all(self):
        load = LoadDatabase()
        done = load.load_weeks()
        return done

    def __load_batch(self,index,batch):
        start_index = 0 if not(index) else int(index)
        batch_size = 0 if not(batch) else int(batch)
        end_index = start_index + batch_size

        load = LoadDatabase()
        done = load.load_weeks(start_index,batch_size)
        return done,end_index

    def get(self):
        index = self.request.get('index')
        batch = self.request.get('batch_size')
        load_all = not(index) and not(batch)

        if load_all:
            finished = self.__load_all()
        else:
            finished,end_index = self.__load_batch(index,batch)

        if finished:
            self.response.write('Finished loading weeks.')
        else:
            batch_size = 0 if not(batch) else int(batch)
            code = "<form type='post'>"
            code += "<input type='hidden' name='index' value='%s'>" % (end_index)
            code += "<input type='hidden' name='batch_size' value='%s'>" % (batch_size)
            code += "Load Next Batch&nbsp;"
            code += "<input type='submit' value='next'>"
            code += "</form>"
            self.response.write(code)

    def post(self):
        self.response.write('Redirecting...')
        index = self.request.get("index")
        batch_size = self.request.get("batch_size")
        self.redirect('/a/load_weeks?index=%s&batch_size=%s' % (index,batch_size))
