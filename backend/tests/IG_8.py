# IG_8      HR staff can update a role listing
import json
import pytest

from g4t1_test import *
from sqlalchemy.exc import IntegrityError

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_invalid_role(client):
    invalid_data = {
        "role_name": "Consult",
        "application_opening": "2023-10-01",
        "application_deadline": "2023-10-15",
        "manager_ID": 1033,
        "dept": "Finance",
        "country": "Hong Kong",
    }
    with app.app_context():
        with pytest.raises(IntegrityError):
            latest_rolelisting_ID = str(RoleListing.query.order_by(RoleListing.rolelisting_ID.desc()).first().rolelisting_ID)
            client.put('/updaterolelisting/'+latest_rolelisting_ID, json=invalid_data)

def test_update_role_listing(client):
    updated_data = {
        "role_name": "Consultant",
        "application_opening": "2023-10-01",
        "application_deadline": "2023-10-15",
        "manager_ID": 1033,
        "dept": "Finance",
        "country": "Hong Kong",
    }
    with app.app_context():
        latest_rolelisting_ID = str(RoleListing.query.order_by(RoleListing.rolelisting_ID.desc()).first().rolelisting_ID)
        response = client.put('/updaterolelisting/'+latest_rolelisting_ID, json=updated_data)
        assert response.status_code == 200
        updated_role_listing = json.loads(response.data)["data"][latest_rolelisting_ID]
        assert updated_role_listing["role_name"] == "Consultant"
        assert updated_role_listing["application_opening"] == "2023-10-01"
        assert updated_role_listing["application_deadline"] == "2023-10-15"
        assert updated_role_listing["dept"] == "Finance"
        assert updated_role_listing["country"] == "Hong Kong"

def test_update_duplicate_role_listing(client):
    duplicate_update_data = {
        "role_name": "Consultant",
        "application_opening": "2023-10-01",
        "application_deadline": "2023-10-15",
        "manager_ID": 1033,
        "dept": "Finance",
        "country": "Hong Kong",
    }
    with app.app_context():
        latest_rolelisting_ID = str(RoleListing.query.order_by(RoleListing.rolelisting_ID.desc()).first().rolelisting_ID)
        response = client.put('/updaterolelisting/'+latest_rolelisting_ID, json=duplicate_update_data)
        assert response.status_code == 400