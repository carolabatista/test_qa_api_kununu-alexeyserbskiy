from unittest import TestCase
import json


class BaseSettings(TestCase):

    endpoint = "https://reqres.in/api/"

    #Amount of users, created during a tests run
    users = 0

    # Used for every test class
    def setup_class(self):
        print("----Test suite started----")

    def teardown_class(self):
        print("----Test suite is over----")

    # Used for every test method in class
    def setUp(self):
        print("----Current testcase: " + self._testMethodName + " started----")

    def tearDown(self):
        print("----Current testcase: " + self._testMethodName + " is over----")


class Response:
    def __init__(self):
        self.code: str
        self.json: json








