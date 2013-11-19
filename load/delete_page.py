import webapp2
from load import *

class DeleteDatabase(webapp2.RequestHandler):

    def get(self):
        code = "<html><body>"
        code += "<form action='delete' method='post'>"
        code += "Delete the Database&nbsp;"
        code += "<input type='submit' value='Submit'>"
        code += "</form>"
        code += "</body></html>"
        self.response.write(code)

    def post(self):
        load = LoadDatabase()
        load.delete_all()
        self.response.write('Database deleted.')

class DeletePlayers(webapp2.RequestHandler):
    def get(self):
        code = "<html><body>"
        code += "<form action='delete_players' method='post'>"
        code += "Delete the Players&nbsp;"
        code += "<input type='submit' value='Submit'>"
        code += "</form>"
        code += "</body></html>"
        self.response.write(code)

    def post(self):
        load = LoadDatabase()
        load.delete_players()
        self.response.write('Players deleted from database.')

class DeleteTeams(webapp2.RequestHandler):
    def get(self):
        code = "<html><body>"
        code += "<form action='delete_teams' method='post'>"
        code += "Delete the Teams&nbsp;"
        code += "<input type='submit' value='Submit'>"
        code += "</form>"
        code += "</body></html>"
        self.response.write(code)

    def post(self):
        load = LoadDatabase()
        load.delete_teams()
        self.response.write('Teams deleted from database.')

class DeleteGames(webapp2.RequestHandler):
    def get(self):
        code = "<html><body>"
        code += "<form action='delete_games' method='post'>"
        code += "Delete the Games&nbsp;"
        code += "<input type='submit' value='Submit'>"
        code += "</form>"
        code += "</body></html>"
        self.response.write(code)

    def post(self):
        load = LoadDatabase()
        load.delete_games()
        self.response.write('Games deleted from database.')

class DeleteWeeks(webapp2.RequestHandler):
    def get(self):
        code = "<html><body>"
        code += "<form action='delete_weeks' method='post'>"
        code += "Delete the Weeks&nbsp;"
        code += "<input type='submit' value='Submit'>"
        code += "</form>"
        code += "</body></html>"
        self.response.write(code)

    def post(self):
        load = LoadDatabase()
        load.delete_weeks()
        self.response.write('Weeks deleted from database.')

class DeletePicks(webapp2.RequestHandler):
    def get(self):
        code = "<html><body>"
        code += "<form action='delete_picks' method='post'>"
        code += "Delete the Picks&nbsp;"
        code += "<input type='submit' value='Submit'>"
        code += "</form>"
        code += "</body></html>"
        self.response.write(code)

    def post(self):
        load = LoadDatabase()
        load.delete_picks()
        self.response.write('Picks deleted from database.')

class DeleteLookups(webapp2.RequestHandler):
    def get(self):
        code = "<html><body>"
        code += "<form action='delete_lookups' method='post'>"
        code += "Delete the Lookups&nbsp;"
        code += "<input type='submit' value='Submit'>"
        code += "</form>"
        code += "</body></html>"
        self.response.write(code)

    def post(self):
        load = LoadDatabase()
        load.delete_lookups()
        self.response.write('Lookups deleted from database.')
