import requests
import json
from unittest import TestCase
from .config import *


class TestCharacterListAPI(TestCase):
    """Test creation of characters and listing all characters"""
    URL = BASE_URL + "/api/characters"
    headers = {"Content-Type": "application/json"}

    @classmethod
    def setUpClass(cls):
        post_data = json.dumps(admin_login)
        response = requests.post(LOGIN_URL, post_data, headers=cls.headers)
        cls.headers["auth"] = response.json()["auth"]

    def test_get_empty(self):
        response = requests.get(self.URL, headers=self.headers)
        for item in response.json():
            requests.delete(BASE_URL + item["URI"], headers=self.headers)

        response = requests.get(self.URL, headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    def test_post_working(self):
        post_data = json.dumps({"name": "Serra",
                                "description": "Serra is a wolf shifter who flies a helicopter with a massive fuck-off \
                                gun.",
                                "pc": True})
        response = requests.post(self.URL, post_data, headers=self.headers)
        char = response.json().keys()

        self.assertEqual(response.status_code, 201)
        self.assertIn("URI", char)
        self.assertNotIn("name", char)
        self.assertNotIn("description", char)
        self.assertNotIn("pc", char)

    def test_post_status(self):
        post_data = json.dumps({"name": "Rook",
                                "description": "A genderless physical adept who was corrupted by Nyarlathotep.",
                                "pc": True,
                                "status": "AWOL"})
        URL = BASE_URL + requests.post(self.URL, post_data, headers=self.headers).json()["URI"]
        response = requests.get(URL, headers=self.headers)
        self.assertEqual("AWOL", response.json()["status"])

    def test_post_missing_info(self):
        post_data = json.dumps({})
        response = requests.post(self.URL, post_data, headers=self.headers)
        errors = response.json()["message"].keys()

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", errors)
        self.assertIn("description", errors)
        self.assertIn("pc", errors)

    def test_get_characters(self):
        post_data = json.dumps({"name": "Serra",
                                "description": "Serra is a wolf shifter who flies a helicopter with a massive fuck-off \
                                gun.",
                                "pc": True})
        requests.post(self.URL, post_data, headers=self.headers)
        response = requests.get(self.URL, headers=self.headers)
        response_json = response.json()
        char = response_json[-1].keys()

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(len(response_json), 0)
        self.assertIn("URI", char)
        self.assertIn("name", char)
        self.assertNotIn("description", char)
        self.assertNotIn("pc", char)
