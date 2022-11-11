from fastapi.testclient import TestClient
import main
import pytest
import sys
import os
import json

# from routes import login
#
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

client = TestClient(main.app)


def test_signup():
    data = {
        "email": "test@test.com",
        "password": "test",
        "first_name": "test",
        "last_name": "test",
        "role": "employee"
    }
    response = client.post("/signup", json.dumps(data))

    assert response.status_code == 401
    assert response.json()['detail'] == 'Login First'

    data = {
        "email": "bruce@wayne.com",
        "password": "batman"
    }
    client.post("/login", json.dumps(data))
    # assert res.status_code==200

    data = {
        "email": "test@test.com",
        "password": "test",
        "first_name": "test",
        "last_name": "test",
        "role": "employee"
    }
    response = client.post("/signup", json.dumps(data))

    assert response.status_code == 409
    assert response.json()['detail'] == "user already exists"

    client.put('/logout')

    data = {
        "email": "satyam@gkmit.co",
        "password": "satyam"
    }
    client.post("/login", json.dumps(data))
    # assert res.status_code==200

    data = {
        "email": "te@test.com",
        "password": "test",
        "first_name": "test",
        "last_name": "test",
        "role": "employee"
    }
    response = client.post("/signup", json.dumps(data))

    assert response.status_code == 401
    assert response.json()['detail'] == 'Only Admin can create user'


def test_logout():
    response = client.put('/logout')

    assert response.status_code == 200
    assert response.json() == "logout successfully"
