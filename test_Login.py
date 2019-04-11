from BaseSettings import BaseSettings
from BaseSettings import Response
from test_Registration import TestRegistration
import requests


class TestLogin (BaseSettings):

    #storing token is needed for testing its uniqueness
    token: str

    # Function for requesting login with provided email and password
    def login(email: str, password: str) -> Response:
        login_response = Response
        login = requests.post(BaseSettings.endpoint + "login",
                                     json={"email": "{}".format(email), "password": "{}".format(password)})
        login_response.code = login.status_code
        login_response.json = login.json()
        return login_response

    def test_Login(self):
        login_user_number = "loginuser" + str(BaseSettings.users + 1)
        TestRegistration.register_Request("{}@test.test".format(login_user_number), "Password1")
        login = TestLogin.login("{}@test.test".format(login_user_number), "Password1")
        assert (login.code == 200), "Response code is {}, instead of 200".format(login.code)
        assert (isinstance(login.json["token"], str)), "Token is not a string"
        assert (login.json["token"] != ""), "Token is empty"

        # storing token is needed for further testing of its uniqueness
        TestLogin.token = login.json["token"]


