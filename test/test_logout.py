from fastapi.testclient import TestClient
import main
import pytest
import sys
import os
import json


client = TestClient(main.app)


def test_logout():
    response = client.put('/logout')

    assert response.status_code == 200
    assert response.json() == "logout successfully"

    response = client.put('/logout')

    assert response.status_code == 400
    assert response.json()['detail'] == "Login First"



