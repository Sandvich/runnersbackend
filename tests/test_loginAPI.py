import requests, json
from unittest import TestCase
from tests.config import *


class TestLoginAPI(TestCase):
    """Test login functionality, including missing information and wrong credentials."""
    URL = LOGIN_URL
    headers = {"Content-Type": "application/json"}

    def test_correct_post(self):
        post_data = json.dumps(admin_login)
        response = requests.post(self.URL, post_data, headers=self.headers)
        message = response.json().keys()

        self.assertEqual(response.status_code, 200)
        self.assertIn("auth", message)

    def test_no_email(self):
        post_data = json.dumps({"password": "password"})
        response = requests.post(self.URL, post_data, headers=self.headers)
        errors = response.json()["message"].keys()

        self.assertEqual(response.status_code, 400)
        self.assertIn("email", errors)

    def test_no_password(self):
        post_data = json.dumps({"email": "sanchitsharma1@gmail.com"})
        response = requests.post(self.URL, post_data, headers=self.headers)
        errors = response.json()["message"].keys()

        self.assertEqual(response.status_code, 400)
        self.assertIn("password", errors)

    def test_empty_post(self):
        post_data = json.dumps({})
        response = requests.post(self.URL, post_data, headers=self.headers)
        errors = response.json()["message"].keys()

        self.assertEqual(response.status_code, 400)
        self.assertIn("email", errors)
        self.assertIn("password", errors)

    def test_wrong_user(self):
        post_data = json.dumps({"email": "example@example.com", "password": "password"})
        response = requests.post(self.URL, post_data, headers=self.headers)
        message = response.json()['message']

        self.assertEqual(response.status_code, 403)
        self.assertEqual(message, "User not found")

    def test_wrong_passworD(self):
        post_data = json.dumps({"email": "sanchitsharma1@gmail.com", "password": "wrongpassword"})
        response = requests.post(self.URL, post_data, headers=self.headers)
        message = response.json()['message']

        self.assertEqual(response.status_code, 403)
        self.assertEqual(message, "Wrong password")
