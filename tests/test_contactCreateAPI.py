import requests, json
from unittest import TestCase
from tests.config import *


class TestContactCreateAPI(TestCase):
    """Test creating a contact"""
    headers = {"Content-Type": "application/json"}
    URL = BASE_URL + "/api/contacts"

    @classmethod
    def setUpClass(cls):
        response = requests.post(LOGIN_URL, json.dumps(admin_login), headers=cls.headers)
        cls.headers["auth"] = response.json()["auth"]

        # Create an NPC and a PC, record their IDs
        response = requests.post(CREATE_NPC_URL, json.dumps(WORKING_NPC), headers=cls.headers)
        cls.NPC = response.json()['URI'].split('/')[-1]
        response = requests.post(CREATE_PC_URL, json.dumps(WORKING_PC), headers=cls.headers)
        cls.PC = response.json()['URI'].split('/')[-1]

    def test_invalid_pc(self):
        post_data = json.dumps({"character": 0, "contact": self.NPC, "security": "GM", "loyalty": 3, "chips": 0})
        response = requests.post(self.URL, post_data, headers=self.headers)

        self.assertEqual(response.status_code, 404)
        self.assertIn(" PC", response.json()['message'])

    def test_invalid_npc(self):
        post_data = json.dumps({"character": self.PC, "contact": 0, "security": "GM", "loyalty": 3, "chips": 0})
        response = requests.post(self.URL, post_data, headers=self.headers)

        self.assertEqual(response.status_code, 404)
        self.assertIn(" NPC", response.json()['message'])

    def test_missing_info(self):
        post_data = json.dumps({})
        response = requests.post(self.URL, post_data, headers=self.headers)
        errors = response.json()["message"].keys()

        self.assertEqual(response.status_code, 400)
        self.assertIn("character", errors)
        self.assertIn("contact", errors)
        self.assertIn("security", errors)
        self.assertIn("loyalty", errors)
        self.assertIn("chips", errors)

    def test_post(self):
        post_data = json.dumps({"character": self.PC, "contact": self.NPC, "security": "GM", "loyalty": 3, "chips": 0})
        response = requests.post(self.URL, post_data, headers=self.headers)

        self.assertEqual(response.status_code, 201)
        self.assertIn("URI", response.json().keys())
