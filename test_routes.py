from fastapi.testclient import TestClient
from main import app
import pytest
import sys
import os
import json

from routes import login

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

client = TestClient(app)


def test_login():
    data = {
        "email": "bruce@wayne.com",
        "password": "batman"
    }
    response = client.post("/login", json.dumps(data))

    # response_again=client.post("/login", json.dumps(data))

    assert response.status_code == 200
    assert response.json()['access_token'] is not None
    assert response.json()['token_type'] == "bearer"

    # assert  response_again.status_code==400


def test_postleaves():
    data = {
        "leave_date": "2023-10-01",
        "leave_type": "fullday"
    }
    response = client.post("/leaves", json.dumps(data))

    assert response.status_code == 201
    assert response.json()['date'] == '2023-10-01'
    assert response.json()['leave_type'] == "fullday"
    assert response.json()['leave_status'] == "Pending"



def test_getleaves():
    response = client.get("/leaves")
    database= {
                            "leave_type": "fullday",
                            "id": 1,
                            "leave_status": "Approved",
                            "date": "2022-11-10",
                            "user_id": 1
                        }
    assert response.status_code == 200
    assert response.json() is not None
    # assert response.json()[0] == database


def test_approveleave():

    response = client.put("/leaves/approve/1" )

    assert response.status_code ==201
    assert response.json() is not None
    assert response.json()['detail'] == "leave approved"


def test_rejectleave():
    response = client.put("/leaves/reject/1")

    assert response.status_code == 201
    assert response.json() is not None
    assert response.json()['detail'] == "leave Rejected"

def test_signup():
    data= {
              "email": "test@test.com",
              "password": "test",
              "first_name": "test",
              "last_name": "test",
              "role": "employee"
            }
    response = client.post("/signup", json.dumps(data))

    assert response.status_code==409
    assert response.json()['detail']== "user already exists"

def test_logout():
    response = client.put('/logout')

    assert response.status_code == 200
    assert response.json() == "logout successfully"

