import json
import pytest
from g4t1_test import RoleListing
from conftest import client, app

def test_create_rolelisting(client):
    rolelisting_data = {
        "role_name": "Software Engineer",
        "application_opening": "2023-09-21",
        "application_deadline": "2023-12-31",
        "dept": "Engineering Operation",
        "country": "Hong Kong",
        "manager_ID": "1033",
    }

    response = client.post("/addrolelisting", json=rolelisting_data)

    assert response.status_code == 201

    response_data = json.loads(response.data)

    assert "code" in response_data
    assert "data" in response_data
    assert "message" not in response_data

    with app.app_context():
        created_role_listing = RoleListing.query.filter(
            RoleListing.role_name == "Software Engineer",
            RoleListing.application_opening == "2023-09-21",
            RoleListing.application_deadline == "2023-12-31"
        ).first()
        assert created_role_listing is not None
        
        
def test_duplicate_rolelisting(client):
    
    rolelisting_data = {
        "role_name": "Software Engineer",
        "application_opening": "2023-09-15",
        "application_deadline": "2023-12-31",
        "dept": "Engineering Operation",
        "country": "Hong Kong",
        "manager_ID": "1033"
    }
    
    response = client.post("/addrolelisting", json=rolelisting_data)

    response_duplicate = client.post("/addrolelisting", json=rolelisting_data)

    assert response_duplicate.status_code == 400

    response_duplicate_data = json.loads(response_duplicate.data)

    assert "code" in response_duplicate_data
    assert "data" in response_duplicate_data
    assert "message" in response_duplicate_data
    assert response_duplicate_data["message"] == 'Role Listing exists.'

