import requests
import json
from unittest import TestCase
from .config import BASE_URL


class TestLoginAPI(TestCase):
    """Test login functionality, including missing information and wrong credentials."""
    URL = BASE_URL + "api/login"
    headers = {"Content-Type": "application/json"}

    def test_correct_post(self):
        post_data = json.dumps({"email": "sanchitsharma1@gmail.com", "password": "password"})
        response = requests.post(self.URL, post_data, headers=self.headers)
        assert response.status_code == 200
        assert "auth" in response.json().keys()

    def test_no_email(self):
        post_data = json.dumps({"password": "password"})
        response = requests.post(self.URL, post_data, headers=self.headers)
        assert response.status_code == 400
        assert "email" in response.json()["message"].keys()

    def test_no_password(self):
        post_data = json.dumps({"email": "sanchitsharma1@gmail.com"})
        response = requests.post(self.URL, post_data, headers=self.headers)
        assert response.status_code == 400
        assert "password" in response.json()["message"].keys()

    def test_empty_post(self):
        post_data = json.dumps({})
        response = requests.post(self.URL, post_data, headers=self.headers)
        assert response.status_code == 400
        assert "email" in response.json()["message"].keys()
        assert "password" in response.json()["message"].keys()

    def test_wrong_user(self):
        post_data = json.dumps({"email": "example@example.com", "password": "password"})
        response = requests.post(self.URL, post_data, headers=self.headers)
        assert response.status_code == 403
        assert response.json()["message"] == "User not found"

    def test_wrong_passworD(self):
        post_data = json.dumps({"email": "sanchitsharma1@gmail.com", "password": "wrongpassword"})
        response = requests.post(self.URL, post_data, headers=self.headers)
        assert response.status_code == 403
        assert response.json()["message"] == "Wrong password"
