import requests, json
from unittest import TestCase
from tests.config import *


class TestContactAPI(TestCase):
    """Test editing and viewing a contact"""
    headers = {"Content-Type": "application/json"}
    CREATE_URL = BASE_URL + "/api/contacts"

    @classmethod
    def setUpClass(cls):
        response = requests.post(LOGIN_URL, json.dumps(admin_login), headers=cls.headers)
        cls.headers["auth"] = response.json()["auth"]

        # Create an NPC and a PC, record their IDs
        cls.NPC = requests.post(CREATE_NPC_URL, json.dumps(WORKING_NPC), headers=cls.headers)\
            .json()['URI'].split('/')[-1]
        cls.PC = requests.post(CREATE_PC_URL, json.dumps(WORKING_PC), headers=cls.headers).json()['URI'].split('/')[-1]

        # Create a contact linking the two
        post_data = json.dumps({"character": cls.PC, "contact": cls.NPC, "security": "GM", "loyalty": 3, "chips": 0})
        cls.URL = BASE_URL + requests.post(cls.CREATE_URL, post_data, headers=cls.headers).json()['URI']

    def test_invalid_contact(self):
        invalid_contact = "/".join(self.URL.split("/")[:-1] + ["0"])
        self.assertEqual(requests.put(invalid_contact, json.dumps({}), headers=self.headers).status_code, 404)
        self.assertEqual(requests.delete(invalid_contact, headers=self.headers).status_code, 404)

    def test_put(self):
        post_data = json.dumps({"chips": -3})
        response = requests.put(self.URL, post_data, headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertIn("URI", response.json().keys())

    def test_get(self):
        response = requests.get(BASE_URL + "/api/pc/" + str(self.PC), headers=self.headers)
        contact = response.json()['contacts'][0]

        self.assertEqual(response.status_code, 200)
        self.assertIn("name", contact)
        self.assertIn("connection", contact)
        self.assertIn("loyalty", contact)
        self.assertIn("chips", contact)
        self.assertIn("URI", contact)

    def test_players_cant_edit_contacts(self):
        post_data = json.dumps({"chips": 3})
        headers = {"Content-Type": "application/json"}
        headers['auth'] = requests.post(LOGIN_URL, json.dumps(player_login), headers=self.headers).json()['auth']
        response = requests.put(self.URL, post_data, headers=headers)
        message = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertIn("message", message.keys())


    def test_delete(self):
        new_url = BASE_URL + requests.post(self.CREATE_URL,
                    json.dumps({"character": self.PC, "contact": self.NPC, "security": "GM", "loyalty": 3, "chips": 0}),
                    headers=self.headers).json()['URI']
        response = requests.delete(new_url, headers=self.headers)
        message = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("message", message.keys())
        self.assertEqual(message["message"], "Success")
