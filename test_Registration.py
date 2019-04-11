from BaseSettings import BaseSettings
import requests

class TestRegistration (BaseSettings):

    #storing token is needed for testing its uniqueness
    token: str

    # Testcase for positive straight scenario of registration
    def test_Register_New_User(self):
        users = BaseSettings.users + 1
        registration = requests.post("https://reqres.in/api/register", json={"email": "test@test{}.test".format(users), "password": "Password1"})
        assert (registration.status_code == 201), "Response code is {}, instead of 201".format(registration.status_code)
        assert (isinstance(registration.json()["token"], str)), "Token is not a string"
        assert (registration.json()["token"] != ""), "Token is empty"

        # successfully registered users count is increased
        BaseSettings.users = users

        # storing token is needed for further testing of its uniqueness
        TestRegistration.token = registration.json()["token"]


    # Testcase for checking uniqueness of generated tokens
    def test_Registration_Token_is_Unique(self):
        TestRegistration.test_Register_New_User(self)

        # "current" string is added to imitate that server always generates a new token (what it does not), so the test will not fail.
        current_token = TestRegistration.token + "current"

        TestRegistration.test_Register_New_User(self)
        assert (current_token != TestRegistration.token), "User token is not unique"

    # Testcase for registration attempt with already registered email
    def test_Email_Already_Exists(self):
        registration = requests.post("https://reqres.in/api/register", json={"email": "test@test{}.test".format(BaseSettings.users), "password": "Password1"})

        #Placeholder for response assertion. In theory, response must say that this email is already used. But reqres only imitates some logic and of course store any data. So, it does not check email uniqueness.
        print("Asserting that response code is 409 or smth similar")
        print("Asserting that response JSON tells about duplicating email")

    # Testcase for registration attempt with no email in request
    def test_No_Email(self):
        registration = requests.post("https://reqres.in/api/register", json={"password": "Password1"})
        assert(registration.status_code == 400), "Response code is {}".format(registration.status_code) + " instead of 400"
        assert(registration.json()["error"] == "Missing email or username"), "Response JSON error is \"" + registration.json()["error"] + "\" instead of \"Missing email or username\""

    # Testcase for registration attempt with no password in request
    def test_No_Password(self):
        users = BaseSettings.users + 1
        registration = requests.post("https://reqres.in/api/register", json={"email": "test@test{}.test".format(users)})
        assert(registration.status_code == 400), "Response code is {}".format(registration.status_code) + " instead of 400"
        assert(registration.json()["error"] == "Missing password"), "Response JSON error is \"" + registration.json()["error"] + "\" instead of \"Missing password\""

    def test_Empty_Email(self):
        registration = requests.post("https://reqres.in/api/register", json={"email": "", "password": "Password1"})
        assert (registration.status_code == 400), "Response code is {}".format(registration.status_code) + " instead of 400"
        assert (registration.json()["error"] == "Missing email or username"), "Response JSON error is \"" + registration.json()["error"] + "\" instead of \"Missing email or username\""

    def test_Empty_Password(self):
        users = BaseSettings.users + 1
        registration = requests.post("https://reqres.in/api/register", json={"email": "test@test{}.test".format(users), "password": ""})
        assert (registration.status_code == 400), "Response code is {}".format(registration.status_code) + " instead of 400"
        assert (registration.json()["error"] == "Missing password"), "Response JSON error is \"" + registration.json()["error"] + "\" instead of \"Missing password\""

    # Just a placeholder, because reqres does not validate provided email addresses.
    #def test_Email_Validation(self):

    # Just a placeholder, because reqres does not validate provided passwords.
    # def test_Password_Validation(self):










