import requests
import json
from unittest import TestCase
from .config import *


class TestPCAPI(TestCase):
    """Test listing a single character and editing a single character"""
    headers = {"Content-Type": "application/json"}
    POST_URL = BASE_URL + '/api/pcs'

    @classmethod
    def setUpClass(cls):
        post_data = json.dumps(admin_login)
        response = requests.post(LOGIN_URL, post_data, headers=cls.headers)
        cls.headers["auth"] = response.json()["auth"]
        cls.post_data = {"name": "Serra",
                         "description": "Serra is a wolf shifter who flies a helicopter with a massive fuck-off gun.",
                         "karma": 15,
                         "nuyen": 20000}

        response = requests.post(cls.POST_URL, json.dumps(cls.post_data), headers=cls.headers)
        cls.URL = BASE_URL + response.json()["URI"]

    def test_no_char(self):
        # Strip out the last element of the URL and replace it with 0, as this will never exist
        nochar = "/".join(self.URL.split("/")[:-1] + ["0"])

        response = requests.get(nochar, headers=self.headers)
        self.assertEqual(response.status_code, 404)
        response = requests.put(nochar, json.dumps({}), headers=self.headers)
        self.assertEqual(response.status_code, 404)
        response = requests.delete(nochar, headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_get(self):
        response = requests.get(self.URL, headers=self.headers)
        char = response.json().keys()

        self.assertEqual(response.status_code, 200)
        self.assertIn("name", char)
        self.assertIn("description", char)
        self.assertIn("URI", char)
        self.assertIn("status", char)
        self.assertIn("karma", char)
        self.assertIn("nuyen", char)

    def test_put(self):
        post_data = {"name": "Serra Skruti"}
        response = requests.put(self.URL, json.dumps(post_data), headers=self.headers)
        message = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("URI", message.keys())
        self.assertEqual(BASE_URL + message["URI"], self.URL)

    def test_players_cant_edit_others_characters(self):
        newchar = BASE_URL + requests.post(self.POST_URL, json.dumps(self.post_data),
                                           headers=self.headers).json()["URI"]
        headers = {"Content-Type": "application/json"}
        headers['auth'] = requests.post(LOGIN_URL, json.dumps(player_login), headers=headers).json()['auth']

        response = requests.put(newchar, json.dumps({"status": "Dead"}), headers=headers)
        self.assertEqual(response.status_code, 403)

    def test_players_cant_delete_others_characters(self):
        newchar = BASE_URL + requests.post(self.POST_URL, json.dumps(self.post_data),
                                           headers=self.headers).json()["URI"]
        headers = {"Content-Type": "application/json"}
        headers['auth'] = requests.post(LOGIN_URL, json.dumps(player_login), headers=headers).json()['auth']

        response = requests.delete(newchar, headers=headers)
        self.assertEqual(response.status_code, 403)

    def test_delete(self):
        newchar = requests.post(self.POST_URL, json.dumps(self.post_data), headers=self.headers).json()
        response = requests.delete(BASE_URL + newchar["URI"], headers=self.headers)
        message = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("message", message.keys())
        self.assertEqual(message["message"], "Success")
