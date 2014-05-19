import unittest
import socket
import logging
from google.appengine.api import urlfetch
from scripts.api.fbpool_api import *
from scripts.api.fbpool_api_exception import *

class TestTeam(unittest.TestCase):

    def setUp(self):
        hostname = socket.gethostname()
        urlfetch.set_default_fetch_deadline(60)
        url = "http://%s" % (hostname)
        self.fbpool = FBPoolAPI(url=url)

    def test_create_team(self):
        try:
            team = self.fbpool.createTeam("Team1","Conference1")
            self.fbpool.deleteTeamByID(team['id'])
        except FBAPIException as e:
            logging.info(e)
            self.assertTrue(False)
            return

        self.__verify_team(team,"Team1","Conference1")


    def test_delete_team(self):
        try:
            team = self.fbpool.createTeam("Team2","Conference1")
            self.fbpool.deleteTeam("Team2")
        except FBAPIException as e:
            self.assertTrue(False)
            return

        self.assertFalse(self.__does_team_exist("Team2"))


    def test_get_team(self):
        try:
            dummy_team = self.fbpool.createTeam("Team3","Conference1")
            team = self.fbpool.getTeam("Team3")
            self.fbpool.deleteTeamByID(dummy_team['id'])
        except FBAPIException as e:
            self.assertTrue(False)
            return

        self.assertIn('id',team)
        self.assertIn('key',team)
        self.assertIn('name',team)
        self.assertIn('conference',team)
        self.assertEquals(team['name'],"Team3")
        self.assertEquals(team['conference'],"Conference1")

    def test_delete_team_by_id(self):
        try:
            team = self.fbpool.createTeam("Team2","Conference1")
            self.fbpool.deleteTeamByID(team['id'])
        except FBAPIException as e:
            self.assertTrue(False)
            return

        self.assertFalse(self.__does_team_exist("Team2"))

    def test_delete_team_by_key(self):
        try:
            team = self.fbpool.createTeam("Team2","Conference1")
            self.fbpool.deleteTeamByKey(team['key'])
        except FBAPIException as e:
            self.assertTrue(False)
            return

        self.assertFalse(self.__does_team_exist("Team2"))

    def test_get_team_by_id(self):
        try:
            created_team = self.fbpool.createTeam("Team4","Conference1")
            team = self.fbpool.getTeamByID(created_team['id'])
            self.fbpool.deleteTeamByID(created_team['id'])
        except FBAPIException as e:
            self.assertTrue(False)
            return

        self.assertIn('id',team)
        self.assertIn('key',team)
        self.assertIn('name',team)
        self.assertIn('conference',team)
        self.assertEquals(team['name'],"Team4")
        self.assertEquals(team['conference'],"Conference1")

    def test_get_team_by_key(self):
        try:
            created_team = self.fbpool.createTeam("Team4","Conference1")
            team = self.fbpool.getTeamByKey(created_team['key'])
            self.fbpool.deleteTeamByID(created_team['id'])
        except FBAPIException as e:
            self.assertTrue(False)
            return

        self.assertIn('id',team)
        self.assertIn('key',team)
        self.assertIn('name',team)
        self.assertIn('conference',team)
        self.assertEquals(team['name'],"Team4")
        self.assertEquals(team['conference'],"Conference1")

    def test_get_teams(self):
        try:
            self.fbpool.deleteAllTeams()
            teams = self.fbpool.getAllTeams()
            self.assertEquals(len(teams),0)

            team1 = self.fbpool.createTeam("Team1","Conference1")
            team2 = self.fbpool.createTeam("Team2","Conference1")
            team3 = self.fbpool.createTeam("Team3","Conference1")
            team4 = self.fbpool.createTeam("Team4","Conference1")
            team5 = self.fbpool.createTeam("Team5","Conference1")

            teams = self.fbpool.getAllTeams()
            self.assertEquals(len(teams),5)

            teams_sorted = sorted(teams,key=lambda team:team['name'])

            self.__verify_team(teams_sorted[0],"Team1","Conference1")
            self.__verify_team(teams_sorted[1],"Team2","Conference1")
            self.__verify_team(teams_sorted[2],"Team3","Conference1")
            self.__verify_team(teams_sorted[3],"Team4","Conference1")
            self.__verify_team(teams_sorted[4],"Team5","Conference1")

            self.fbpool.deleteAllTeams()
        except FBAPIException as e:
            self.assertTrue(False)
            return

    def test_delete_all_teams(self):
        try:
            self.fbpool.deleteAllTeams()
            teams = self.fbpool.getAllTeams()
            self.assertEquals(len(teams),0)

            team1 = self.fbpool.createTeam("Team1","Conference1")
            team2 = self.fbpool.createTeam("Team2","Conference1")
            team3 = self.fbpool.createTeam("Team3","Conference1")
            team4 = self.fbpool.createTeam("Team4","Conference1")
            team5 = self.fbpool.createTeam("Team5","Conference1")

            teams = self.fbpool.getAllTeams()
            self.assertEquals(len(teams),5)

            self.fbpool.deleteAllTeams()
            teams = self.fbpool.getAllTeams()
            self.assertEquals(len(teams),0)
        except FBAPIException as e:
            self.assertTrue(False)
            return

    def test_create_team_that_already_exists(self):
        try:
            self.fbpool.deleteTeamIfExists("Team1")
            team = self.fbpool.createTeam("Team1","Conference1")
        except FBAPIException as e:
            self.assertTrue(False)
            return

        try:
            team2 = self.fbpool.createTeam("Team1","Conference1")
            self.assertTrue(False)
        except FBAPIException as e:
            self.assertEquals(e.http_code,409)
            self.assertEquals(e.errmsg,"team already exists")

        try:
            self.fbpool.deleteTeamByID(team['id'])
        except FBAPIException as e:
            self.assertTrue(False)
            return


    def test_create_multiple_teams(self):
        try:
            self.fbpool.deleteTeamIfExists("Team1")
            self.fbpool.deleteTeamIfExists("Team2")
            self.fbpool.deleteTeamIfExists("Team3")
            self.fbpool.deleteTeamIfExists("Team4")
            self.fbpool.addTeam("Team1","Conference1")
            self.fbpool.addTeam("Team2","Conference1")
            self.fbpool.addTeam("Team3","Conference1")
            self.fbpool.addTeam("Team4","Conference1")
            teams = self.fbpool.createTeams()

            teams_sorted = sorted(teams,key=lambda team:team['name'])

            self.__verify_team(teams_sorted[0],"Team1","Conference1")
            self.__verify_team(teams_sorted[1],"Team2","Conference1")
            self.__verify_team(teams_sorted[2],"Team3","Conference1")
            self.__verify_team(teams_sorted[3],"Team4","Conference1")

            for i in range(len(teams_sorted)):
                self.fbpool.deleteTeamByID(teams_sorted[i]['id'])

        except FBAPIException as e:
            self.assertTrue(False)
            return

    def test_create_multiple_teams_with_same_name(self):
        try:
            self.fbpool.deleteTeamIfExists("Team1")
            self.fbpool.deleteTeamIfExists("Team2")
            team1 = self.fbpool.createTeam("Team1","Conference1")
        except FBAPIException as e:
            self.assertTrue(False)
            return

        try:
            self.fbpool.addTeam("Team1","Conference1")
            self.fbpool.addTeam("Team2","Conference1")
            teams = self.fbpool.createTeams()
            self.assertTrue(False)
        except FBAPIException as e:
            self.assertEquals(e.http_code,409)
            self.assertEquals(e.errmsg,"team already exists")

        try:
            self.fbpool.deleteTeamIfExists("Team1")
        except FBAPIException as e:
            self.assertTrue(False)
            return

        self.assertFalse(self.__does_team_exist("Team2"))


    def __does_team_exist(self,name):
        try:
            team = self.fbpool.getTeam(name)
            return True
        except FBAPIException as e:
            return False
        raise AssertionError,"should not get here"

    def __verify_team(self,team,name,conference):
        self.assertIn('id',team)
        self.assertIn('key',team)
        self.assertIn('name',team)
        self.assertIn('conference',team)
        self.assertEquals(team.name,name)
        self.assertEquals(team.conference,conference)

