import json
import pytest

from g4t1_test import *
from conftest import client, app
from sqlalchemy.exc import IntegrityError


def test_create_application(client):
    application_data = {
        "staff_ID": 1031,
        "rolelisting_ID": 1,
        "application_date": "2023-10-12",
        "percentage_match": 38.9
    }

    with app.app_context():

        response = client.post("/addapplication", json=application_data)

        assert response.status_code == 201

        response_data = json.loads(response.data)

        assert "code" in response_data
        assert "data" in response_data
        assert "message" not in response_data

        created_application = Application.query.filter(
            response_data["data"]["staff_ID"] == 1031,
            response_data["data"]["rolelisting_ID"] == 1
        ).first()
        assert created_application is not None
        
        
def test_duplicate_application(client):
    
    application_data = {
        "staff_ID": 1032,
        "rolelisting_ID": 1,
        "application_date": "2023-10-12",
        "percentage_match": 38.9
    }

    with app.app_context():

        client.post("/addapplication", json=application_data)

        response_duplicate = client.post("/addapplication", json=application_data)

        assert response_duplicate.status_code == 400

        response_duplicate_data = json.loads(response_duplicate.data)

        assert "code" in response_duplicate_data
        assert "data" in response_duplicate_data
        assert "message" in response_duplicate_data

        assert response_duplicate_data["message"] == 'Application exists.'
