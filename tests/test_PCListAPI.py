import requests, json
from unittest import TestCase
from tests.config import *


class TestPCListAPI(TestCase):
    """Test creation of characters and listing all characters"""
    URL = CREATE_PC_URL
    headers = {"Content-Type": "application/json"}

    @classmethod
    def setUpClass(cls):
        response = requests.post(LOGIN_URL, json.dumps(admin_login), headers=cls.headers)
        cls.headers["auth"] = response.json()["auth"]

    def delete_all_chars(self):
        response = requests.get(self.URL, headers=self.headers)
        for item in response.json():
            requests.delete(BASE_URL + item["URI"], headers=self.headers)

    def test_get_empty(self):
        self.delete_all_chars()
        response = requests.get(self.URL, headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    def test_post_working(self):
        post_data = json.dumps(WORKING_PC)
        response = requests.post(self.URL, post_data, headers=self.headers)
        char = response.json().keys()

        self.assertEqual(response.status_code, 201)
        self.assertIn("URI", char)
        self.assertNotIn("name", char)
        self.assertNotIn("description", char)
        self.assertNotIn("karma", char)
        self.assertNotIn("nuyen", char)

    def test_post_status(self):
        post_data = json.dumps({"name": "Rook",
                                "description": "A genderless physical adept who was corrupted by Nyarlathotep.",
                                "status": "AWOL",
                                "karma": 20,
                                "nuyen": 100000})
        r = requests.post(self.URL, post_data, headers=self.headers).json()
        URL = BASE_URL + r["URI"]
        response = requests.get(URL, headers=self.headers)
        self.assertEqual("AWOL", response.json()["status"])

    def test_post_missing_info(self):
        post_data = json.dumps({})
        response = requests.post(self.URL, post_data, headers=self.headers)
        errors = response.json()["message"].keys()

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", errors)
        self.assertIn("description", errors)
        self.assertIn("karma", errors)
        self.assertIn("nuyen", errors)

    def test_get_character(self):
        post_data = json.dumps(WORKING_PC)
        requests.post(self.URL, post_data, headers=self.headers)
        response = requests.get(self.URL, headers=self.headers)
        response_json = response.json()
        char = response_json[-1].keys()

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(len(response_json), 0)
        self.assertIn("URI", char)
        self.assertIn("name", char)
        self.assertNotIn("description", char)
        self.assertNotIn("karma", char)
        self.assertNotIn("nuyen", char)

    def test_player_character_count(self):
        self.delete_all_chars()
        headers = {"Content-Type": "application/json"}
        headers["auth"] = requests.post(LOGIN_URL, json.dumps(player_login), headers=headers).json()['auth']

        char = {"name": "something", "description": "pie", "karma": 5, "nuyen": 3}
        charURL = BASE_URL + requests.post(self.URL, json.dumps(char), headers=headers).json()['URI']
        response = requests.post(self.URL, json.dumps(char), headers=headers)
        self.assertEqual(response.status_code, 403)

        requests.put(charURL, json.dumps({"status": "Dead"}), headers=headers)
        response = requests.post(self.URL, json.dumps(char), headers=headers)
        self.assertEqual(response.status_code, 201)

    def test_players_cant_see_characters_they_dont_know(self):
        pass
        # headers = {"Content-Type": "application/json"}
        # headers["auth"] = requests.post(LOGIN_URL, json.dumps(player_login), headers=self.headers).json()['auth']
        #
        # char = {"name": "something", "description": "pie", "pc": False}
        # response = requests.post(self.URL, json.dumps(char), headers=headers)
        # self.assertEqual(response.status_code, 403)
