import webapp2
from load import *

class LoadEveryThingPage(webapp2.RequestHandler):
    def get(self):
        code = "<html><body>"
        code += "<form action='loadall' method='post'>"
        code += "Load the Entire Database&nbsp;"
        code += "<input type='submit' value='Submit'>"
        code += "</form>"
        code += "</body></html>"
        self.response.write(code)

    def post(self):
        load = LoadDatabase()
        load.load_all()
        self.response.write("<html><body>%s</body></html>" % ("Load All Complete"))
