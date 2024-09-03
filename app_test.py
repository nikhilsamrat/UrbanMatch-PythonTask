from fastapi.testclient import TestClient
from schemas import UserCreate
from main import app

client = TestClient(app)


def test_create_users():
    user = {
        "name": "alice",
        "age": 10,
        "gender": "female",
        "email": "alice@gmail.com",
        "city": "bangalore",
        "interests": ["coding"],
    }
    response = client.post("/users/", json=user)
    print(response.json())
    assert response.status_code == 200

    user = {
        "name": "bob",
        "age": 10,
        "gender": "male",
        "email": "bob@gmail.com",
        "city": "bangalore",
        "interests": ["coding"],
    }
    response = client.post("/users/", json=user)
    print(response.json())
    assert response.status_code == 200

    user = {
        "name": "max",
        "age": 10,
        "gender": "male",
        "email": "max@gmail.com",
        "city": "bangalore",
        "interests": ["coding"],
    }
    response = client.post("/users/", json=user)
    print(response.json())
    assert response.status_code == 200

    user = {
        "name": "min",
        "age": 10,
        "gender": "male",
        "email": "min@gmail.com",
        "city": "bangalore",
        "interests": ["coding"],
    }
    response = client.post("/users/", json=user)
    print(response.json())
    assert response.status_code == 200


def test_read_users():
    response = client.get("/users/")
    print(response.json())
    assert response.status_code == 200


def test_delete_min():
    response = client.get("/delete/4")
    print(response.json())
    assert response.status_code == 200


def test_update_max():
    user = {"id": 3, "age": 15}
    response = client.post("/update/", json=user)
    print(response.json())
    assert response.status_code == 200


def test_match_bob():
    response = client.get("/match/2")
    print(response.json())
    assert response.status_code == 200
