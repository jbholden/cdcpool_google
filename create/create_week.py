import webapp2
import unittest
from pages.handler import *

class CreateWeekPage(Handler):

  def code(self):
    c  = '<html><head>'
    c += '</head><body>'
    c += '<h1>Placeholder - POST create_week</h1>'
    c += '</body></html>'
    return c

  def post(self):
    self.response.write(self.code())

  def get(self):
    self.render("create_week_commish.html")
    return

