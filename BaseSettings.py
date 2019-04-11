from unittest import TestCase
import json
import requests


class BaseSettings(TestCase):

    # Used for every test class
    def setup_class(self):
        print("----test started----")

    def teardown_class(self):
        print("----test is over----")

    # Used for every test method in class
    def setUp(self):
        print('----current test: ' + self._testMethodName + " started----")

    def tearDown(self):
        print('----current test: ' + self._testMethodName + " is over----")

    # Function, that will store JSONs
    def get_JSON(self, endpoint, filename):
        jsondata = requests.get(endpoint).json()
        with open(filename + '.txt', 'w') as json_file:
            json.dump(jsondata, json_file)



