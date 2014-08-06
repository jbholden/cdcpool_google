import unittest
from google.appengine.ext import db
import logging
import datetime
from models.root import *

# TODO:  handle teams changing conferences

class TestTeams(unittest.TestCase):

    def test_all_teams_query(self):
        teams_query = db.GqlQuery('select * from Team where ANCESTOR IS :ancestor',ancestor=root_teams())
        self.assertIsNotNone(teams_query)
        teams = list(teams_query)
        self.assertEquals(len(teams),128)
        for team in teams:
            self.__check_team_state(team)

    def test_team_name_query(self):
        self.__test_team_name_query("Georgia Tech")
        self.__test_team_name_query("Virginia Tech")
        self.__test_team_name_query("Syracuse")

    def test_team_conference_query(self):
        self.__test_team_conference_query("Atlantic Coast",14)
        self.__test_team_conference_query("Pacific 12",12)
        self.__test_team_conference_query("Southeastern",14)
        self.__test_team_conference_query("Mountain West",12)
        self.__test_team_conference_query("Big 12",10)
        self.__test_team_conference_query("Big Ten",12)
        self.__test_team_conference_query("American Athletic",10)
        self.__test_team_conference_query("Conference USA",15)
        self.__test_team_conference_query("Independents",7)
        self.__test_team_conference_query("Mid American",13)
        self.__test_team_conference_query("Sun Belt",8)

    def test_invalid_team_name_query(self):
        self.__test_invalid_team_name_query(team="invalid")
        self.__test_invalid_team_name_query(team=None)

    def __test_team_name_query(self,team):
        teams_query = db.GqlQuery('select * from Team where name=:name and ANCESTOR IS :ancestor',name=team,ancestor=root_teams())
        self.assertIsNotNone(teams_query)
        teams = list(teams_query)
        self.assertEquals(len(teams),1)
        self.__check_team_state(teams[0])

    def __test_team_conference_query(self,conference,num_teams):
        teams_query = db.GqlQuery('select * from Team where conference=:conference and ANCESTOR IS :ancestor',conference=conference,ancestor=root_teams())
        self.assertIsNotNone(teams_query)
        teams = list(teams_query)
        self.assertEquals(len(teams),num_teams)
        for team in teams:
            self.__check_team_state(team)

    def __test_invalid_team_name_query(self,team):
        teams_query = db.GqlQuery('select * from Team where name=:name and ANCESTOR IS :ancestor',name=team,ancestor=root_teams())
        self.assertIsNotNone(teams_query)
        teams = list(teams_query)
        self.assertEqual(len(teams),0)

    def __check_team_state(self,team):
        self.assertIsNotNone(team.name)
        self.assertIsNotNone(team.conference)

