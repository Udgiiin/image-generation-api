from fastapi.testclient import TestClient
from app.main import app
from app.core.security import decode_jwt_token
import json
import string
import random
client = TestClient(app)


class FakeUser:
    def __init__(self):
        self.password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        self.username = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        self.id = None
        self.token = None

    def to_body(self, fake_password=None):
        return json.dumps({
            "username": self.username,
            "password": fake_password if fake_password else self.password,
            "id": self.id
        })
    
    def to_header(self, fake_token=None):
        return {
            "authorization": fake_token if fake_token else self.token
        }

user_fake = FakeUser()

def test_add_user():
    response = client.post("/api/v1/user/create", data=user_fake.to_body())
    assert response.status_code == 200
    user_fake.id = response.json()['id']

def test_add_duplicate_user():
    response = client.post("/api/v1/user/create", data=user_fake.to_body())
    assert response.status_code == 409
    assert response.json() == {
        "detail": "username is exists"
    }


def test_login_user():
    response = client.post("/api/v1/user/auth", data=user_fake.to_body())
    assert response.status_code == 200
    assert user_fake.id == decode_jwt_token(response.json()['access_token'])['sub']
    user_fake.token = response.json()['access_token']


def test_login_with_fake_password():
    response = client.post("/api/v1/user/auth", data=user_fake.to_body("loremipsum"))
    assert response.status_code == 406
    assert response.json() == {
        "detail": "wrong password"
    }


def test_get_image_api_without_token():
    response = client.post("/api/v1/image/generate/asdfasdfasd", data=user_fake.to_body())
    assert response.status_code == 405
    

def test_get_image_api():
    response = client.get("/api/v1/image/generate/asdfasdfasd", data=user_fake.to_body(), headers=user_fake.to_header())
    assert response.status_code == 200


def test_get_image_api_with_fake_token():
    response = client.get("/api/v1/image/generate/fasdfasd", data=user_fake.to_body(),
                          headers=user_fake.to_header("loremipsum"))
    assert response.status_code == 403