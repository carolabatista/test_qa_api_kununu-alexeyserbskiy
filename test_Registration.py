from BaseSettings import BaseSettings
import requests

class TestRegistration (BaseSettings):

    #storing token is needed for testing its uniqueness
    token: str

    # Testcase for positive straight scenario of registration
    def test_Register_New_User(self):
        users = BaseSettings.users + 1
        BaseSettings.users = users
        registration = requests.post("https://reqres.in/api/register", json={"email": "test@test{}.test".format(users), "password": "Password1"})
        assert (registration.status_code == 201), "Response code is {}, instead of 201".format(registration.status_code)
        assert (isinstance(registration.json()["token"], str)), "Token is not a string"
        assert (registration.json()["token"] != ""), "Token is empty"

        # storing token is needed for further testing of its uniqueness
        TestRegistration.token = registration.json()["token"]


    # Testcase for checking uniqueness of generated tokens
    def test_Registration_Token_is_Unique(self):
        TestRegistration.test_Register_New_User(self)

        # "current" string is added to imitate that server always generates a new token (what it does not), so the test will not fail.
        current_token = TestRegistration.token + "current"

        TestRegistration.test_Register_New_User(self)
        assert (current_token != TestRegistration.token)






