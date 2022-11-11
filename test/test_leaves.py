from fastapi.testclient import TestClient
import main
import pytest
import sys
import os
import json


client = TestClient(main.app)



def test_postleaves():
    data = {
        "leave_date": "2023-10-01",
        "leave_type": "fullday"
    }
    response = client.post("/leaves", json.dumps(data))

    assert response.status_code == 401
    assert response.json() is not None

    data = {
        "email": "bruce@wayne.com",
        "password": "batman"
    }
    client.post("/login", json.dumps(data))

    data = {
        "leave_date": "2023-10-01",
        "leave_type": "fullday"
    }
    response = client.post("/leaves", json.dumps(data))

    assert response.status_code == 201
    assert response.json()['date'] == '2023-10-01'
    assert response.json()['leave_type'] == "fullday"
    assert response.json()['leave_status'] == "Pending"

    client.put('/logout')





def test_getleaves():

    response = client.get("/leaves")
    database= {
                            "leave_type": "fullday",
                            "id": 1,
                            "leave_status": "Approved",
                            "date": "2022-11-10",
                            "user_id": 1
                        }
    assert response.status_code == 401
    assert response.json() is not None


    data = {
        "email": "bruce@wayne.com",
        "password": "batman"
    }
    client.post("/login", json.dumps(data))

    response = client.get("/leaves")

    assert response.status_code == 200
    assert response.json() is not None

    client.put('/logout')

    # assert response.json()[0] == database


def test_approveleave():

    response = client.put("/leaves/approve/1" )

    assert response.status_code ==401
    assert response.json() is not None
    assert response.json()['detail'] == 'Login First'

    data = {
        "email": "bruce@wayne.com",
        "password": "batman"
    }
    client.post("/login", json.dumps(data))

    response = client.put("/leaves/approve/1")

    assert response.status_code ==201
    assert response.json() is not None
    assert response.json()['detail'] == "leave approved"



    client.put('/logout')

    data = {
        "email": "satyam@gkmit.co",
        "password": "satyam"
    }
    client.post("/login", json.dumps(data))

    response = client.put("/leaves/approve/1")

    assert response.status_code == 401
    assert response.json() is not None
    assert response.json()['detail'] == 'Only Admin can approve'

    client.put('/logout')





def test_rejectleave():
    response = client.put("/leaves/reject/1")

    assert response.status_code == 401
    assert response.json() is not None
    assert response.json()['detail'] == 'Login First'

    data = {
        "email": "bruce@wayne.com",
        "password": "batman"
    }
    client.post("/login", json.dumps(data))

    response = client.put("/leaves/reject/1")

    assert response.status_code == 201
    assert response.json() is not None
    assert response.json()['detail'] == "leave Rejected"

    client.put('/logout')

    data = {
        "email": "satyam@gkmit.co",
        "password": "satyam"
    }
    client.post("/login", json.dumps(data))

    response = client.put("/leaves/reject/1")

    assert response.status_code == 401
    assert response.json() is not None
    assert response.json()['detail'] == 'Only Admin can approve'

    client.put('/logout')


