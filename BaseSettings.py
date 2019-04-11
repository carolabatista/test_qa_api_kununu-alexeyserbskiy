from unittest import TestCase
import json
import requests


class BaseSettings(TestCase):

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

    # Function, that will store JSONs
    def write_JSON(self, endpoint, filename):
        jsondata = requests.get(endpoint).json()
        with open(filename + ".txt", "w") as json_file:
            json.dump(jsondata, json_file)






