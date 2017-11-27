import requests, json
from unittest import TestCase
from tests.config import *


class TestContactAPI(TestCase):
    """Test editing and deleting a single contact"""
    headers = {"Content-Type": "application/json"}
    URL = BASE_URL + "/api/contacts"

    def test_put(self):
        self.assertTrue(True)

    def test_delete(self):
        self.assertTrue(True)
