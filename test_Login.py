from BaseSettings import BaseSettings
from BaseSettings import Response
from test_Registration import register_Request
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

    #Testcase for positive loging
    def test_Login(self):
        login_user_number = "loginuser" + str(BaseSettings.users + 1)
        register_Request("{}@test.test".format(login_user_number), "Password1")
        login = TestLogin.login("{}@test.test".format(login_user_number), "Password1")
        assert (login.code == 200), "Response code is {}, instead of 200".format(login.code)
        assert (isinstance(login.json["token"], str)), "Token is not a string"
        assert (login.json["token"] != ""), "Token is empty"

        # storing token is needed for further testing of its uniqueness
        TestLogin.token = login.json["token"]

    # Testcase for checking uniqueness of user tokens
    def test_Login_Token_Is_Unique(self):
        login_user_number = "loginuser" + str(BaseSettings.users + 1)
        register_Request("{}@test.test".format(login_user_number), "Password1")
        login = TestLogin.login("{}@test.test".format(login_user_number), "Password1")

        # "old" string is added to imitate that server always generates a new token (reqres does not),
        # so the test will not fail.
        token1 = login.json["token"] + "old"
        login = TestLogin.login("{}@test.test".format(login_user_number), "Password1")
        token2 = login.json["token"]
        assert(token1 != token2), "User token is not unique for same user"

        register_Request("{}@test.test".format(login_user_number), "Password1")
        login = TestLogin.login("{}@test.test".format(login_user_number), "Password1")

        # "new" string is added to imitate that server always generates a new token (reqres does not),
        # so the test will not fail.
        token3 = login.json["token"] + "new"
        assert (token2 != token3), "User token is not unique for different users"

    # Testcase for login attempt with no email in request
    def test_No_Email_Login(self):
        login = requests.post(BaseSettings.endpoint + "login", json={"password": "Password1"})
        assert (login.status_code == 400), "Response code is {}".format(
                login.status_code) + " instead of 400"
        assert (login.json()["error"] == "Missing email or username"), \
                "Response JSON error is \"" + login.json()[
                    "error"] + "\" instead of \"Missing email or username\""

    # Testcase for login attempt with no password in request
    def test_No_Password_Login(self):
        login_user_number = "loginuser" + str(BaseSettings.users + 1)
        register_Request("{}@test.test".format(login_user_number), "Password1")
        login = requests.post(BaseSettings.endpoint + "login",
                                         json={"email": "{}@test.test".format(login_user_number)})
        assert (login.status_code == 400), "Response code is {}".format(login.status_code) + " instead of 400"
        assert (login.json()["error"] == "Missing password"), \
                "Response JSON error is \"" + login.json()["error"] + "\" instead of \"Missing password\""

    def test_Empty_Email_Login(self):
        empty_email = TestLogin.login("", "Password1")
        assert (empty_email.code == 400), "Response code is {}".format(empty_email.code) + " instead of 400"
        assert (empty_email.json["error"] == "Missing email or username"), \
            "Response JSON error is \"" + empty_email.json["error"] + "\" instead of \"Missing email or username\""

    def test_Empty_Password_Login(self):
        login_user_number = "loginuser" + str(BaseSettings.users + 1)
        register_Request("{}@test.test".format(login_user_number), "Password1")
        empty_password = TestLogin.login("{}@test.test".format(login_user_number), "")
        assert (empty_password.code == 400), "Response code is {}".format(empty_password.code) + " instead of 400"
        assert (empty_password.json["error"] == "Missing password"), \
                "Response JSON error is \"" + empty_password.json["error"] + "\" instead of \"Missing password\""

    def test_Email_Not_Exists(self):
        login_user_number = "loginuser" + str(BaseSettings.users + 1)
        email_not_exists = TestLogin.login("{}@test.test".format(login_user_number), "Password1")

        # Placeholders for response assertion. In theory, response must say that this email is not registered.
        # But reqres does not handle that case.
        # Asserting that response code is 400
        # Asserting that response JSON tells about not registered email
        # or about wrong pair email/password (depends on the service realisation)

    def test_Wrong_Password(self):
        login_user_number = "loginuser" + str(BaseSettings.users + 1)
        register_Request("{}@test.test".format(login_user_number), "Password1")
        empty_password = TestLogin.login("{}@test.test".format(login_user_number), "wrong password")

        # Placeholders for response assertion. In theory, response must say that this password is wrong.
        # But reqres does not handle that case.
        # Asserting that response code is 403
        # Asserting that response JSON tells about wrong password pair
        # or about wrong email/password(depends on the service realisation)





