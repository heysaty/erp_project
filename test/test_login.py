from fastapi.testclient import TestClient
import main
import pytest
import sys
import os
import json
from jwttoken import verify_token

# from routes import login
#
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

client = TestClient(main.app)


def test_login():
    data = {
        "email": "bruce@wayne.com",
        "password": "batman"
    }
    response = client.post("/login", json.dumps(data))



    assert response.status_code == 200
    assert response.json()['access_token'] is not None
    assert response.json()['token_type'] == "bearer"
