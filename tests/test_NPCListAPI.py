import requests, json
from unittest import TestCase
from tests.config import *


class TestNPCListAPI(TestCase):
    """Test the list of NPCs - where it differs from the list of PCs"""
    headers = {"Content-Type": "application/json"}
    URL = CREATE_NPC_URL

    @classmethod
    def setUpClass(cls):
        response = requests.post(LOGIN_URL, json.dumps(admin_login), headers=cls.headers)
        cls.headers["auth"] = response.json()["auth"]

    def test_invalid_sec(self):
        post_data = {"name": "someone",
                     "description": "something",
                     "status": "Active",
                     "security": "not_a_level",
                     "connection": 5}
        response = requests.post(self.URL, json.dumps(post_data), headers=self.headers)
        self.assertEqual(response.status_code, 400)

    def test_post_not_allowed(self):
        headers = {"Content-Type": "application/json"}
        headers["auth"] = requests.post(LOGIN_URL, json.dumps(player_login), headers=headers).json()['auth']
        response = requests.post(self.URL, json.dumps(WORKING_NPC), headers=headers)
        self.assertEqual(response.status_code, 403)
