from BaseSettings import BaseSettings
import requests

class TestRegistration (BaseSettings):

    def test_Register_new_user (self):
        r = requests.post("https://reqres.in/api/register", json={"email": "test@test.test", "password": "p"})
        assert (r.status_code == 201), "Response code is not 201"
        print(r.json())
        assert (isinstance(r.json()["token"], str)), "Token is not string"
        assert (r.json()["token"] != ""), "Token is empty"



