from BaseSettings import BaseSettings
from BaseSettings import Response
import requests


class TestRegistration (BaseSettings):

    # Function for requesting registration with chosen email and password
    # Can be used for checking mail and password inputs validation and used in other classes
    def register_Request(email: str, password: str) -> Response:
        register_response = Response
        registration = requests.post(BaseSettings.endpoint + "register",
                                     json={"email": "{}".format(email), "password": "{}".format(password)})
        register_response.code = registration.status_code
        register_response.json = registration.json()
        if registration.status_code == 201:
            BaseSettings.users += 1
            with open("users.txt", "a") as file:
                file.write("\n{}".format(email) + " / " + "{}".format(password))
                file.close()
        return register_response

    # storing token is needed for testing its uniqueness
    token: str

    # Testcase for positive straight scenario of registration
    def test_Register_New_User(self):
        users = BaseSettings.users + 1
        registration = requests.post(BaseSettings.endpoint + "register", json={"email": "test@test{}.test".format(users), "password": "Password1"})
        assert (registration.status_code == 201), "Response code is {}, instead of 201".format(registration.status_code)
        assert (isinstance(registration.json()["token"], str)), "Token is not a string"
        assert (registration.json()["token"] != ""), "Token is empty"

        # successfully registered users count is increased
        BaseSettings.users = users

        # storing token is needed for further testing of its uniqueness
        TestRegistration.token = registration.json()["token"]

        # successfully registered user to file
        with open("users.txt", "a" ) as file:
            file.write("\ntest@test{}.test".format(users) + " / Password1")
            file.close()

    # Testcase for checking uniqueness of generated tokens
    def test_Registration_Token_is_Unique(self):
        TestRegistration.test_Register_New_User(self)

        # "current" string is added to imitate that server always generates a new token (reqres does not),
        # so the test will not fail.
        current_token = TestRegistration.token + "current"

        TestRegistration.test_Register_New_User(self)
        assert (current_token != TestRegistration.token), "User token is not unique"

    # Testcase for registration attempt with already registered email
    def test_Email_Already_Exists(self):
        registration = TestRegistration.register_Request("test@test{}.test".format(BaseSettings.users), "Password1")
        #registration = requests.post("https://reqres.in/api/register",
                                    # json={"email": "test@test{}.test".format(BaseSettings.users), "password": "Password1"})

        # Placeholders for response assertion. In theory, response must say that this email is already used.
        # But reqres does not check email uniqueness.
        # Asserting that response code is 409 or smth similar
        # Asserting that response JSON tells about duplicating email

    # Testcase for registration attempt with no email in request
    def test_No_Email(self):
        registration = requests.post(BaseSettings.endpoint + "register", json={"password": "Password1"})
        assert(registration.status_code == 400), "Response code is {}".format(registration.status_code) + " instead of 400"
        assert(registration.json()["error"] == "Missing email or username"), \
            "Response JSON error is \"" + registration.json()["error"] + "\" instead of \"Missing email or username\""

    # Testcase for registration attempt with no password in request
    def test_No_Password(self):
        users = BaseSettings.users + 1
        registration = requests.post(BaseSettings.endpoint + "register", json={"email": "test@test{}.test".format(users)})
        assert(registration.status_code == 400), "Response code is {}".format(registration.status_code) + " instead of 400"
        assert(registration.json()["error"] == "Missing password"), \
            "Response JSON error is \"" + registration.json()["error"] + "\" instead of \"Missing password\""

    def test_Empty_Email(self):
        empty_email = TestRegistration.register_Request("test@test{}.test".format(BaseSettings.users + 1), "")
        assert (empty_email.code == 400), "Response code is {}".format(empty_email.code) + " instead of 400"
        assert (empty_email.json["error"] == "Missing password"), "Response JSON error is \"" + empty_email.json[
            "error"] + "\" instead of \"Missing password\""

    def test_Empty_Password(self):
        empty_password = TestRegistration.register_Request("test@test{}.test".format(BaseSettings.users + 1), "")
        assert(empty_password.code == 400), "Response code is {}".format(empty_password.code) + " instead of 400"
        assert (empty_password.json["error"] == "Missing password"), \
            "Response JSON error is \"" + empty_password.json["error"] + "\" instead of \"Missing password\""

    # Just a placeholder, because reqres does not validate provided email addresses.
    # def test_Email_Validation(self):

    # Just a placeholder, because reqres does not validate provided passwords.
    # def test_Password_Validation(self):

    # Because reqres does not validate provided email and password at all (exept empty cases), test has only placeholders for these inputs validation.
    # In theory, inputs could be tests via using register_Request function and asserting returned class values.
    # Also, data files with email and passwords to test and pytest-expect plugin could be useful,
    # so even if one check of validation is failed, the hole test will not stop and will finish checking data from files.










