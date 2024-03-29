import requests, json
from unittest import TestCase
from tests.config import *


class TestNPCAPI(TestCase):
    """Test the NPC endpoint - where it differs from the PC endpoint"""
    headers = {"Content-Type": "application/json"}
    player_headers = {"Content-Type": "application/json"}

    @classmethod
    def setUpClass(cls):
        response = requests.post(LOGIN_URL, json.dumps(admin_login), headers=cls.headers)
        cls.headers["auth"] = response.json()["auth"]
        cls.player_headers['auth'] = requests.post(LOGIN_URL, json.dumps(player_login), headers=cls.headers).json()['auth']

        response = requests.post(CREATE_NPC_URL, json.dumps(WORKING_NPC), headers=cls.headers)
        cls.URL = BASE_URL + response.json()["URI"]

    def test_invalid_security(self):
        post_data = {"security": "not_a_level"}
        response = requests.put(self.URL, json.dumps(post_data), headers=self.headers)
        self.assertEqual(response.status_code, 400)

    def test_get_not_allowed(self):
        response = requests.get(self.URL, headers=self.player_headers)
        self.assertEqual(response.status_code, 403)

    def test_put_not_allowed(self):
        response = requests.put(self.URL, json.dumps(WORKING_NPC), headers=self.player_headers)
        self.assertEqual(response.status_code, 403)

    def test_delete_not_allowed(self):
        response = requests.delete(self.URL, headers=self.player_headers)
        self.assertEqual(response.status_code, 403)
