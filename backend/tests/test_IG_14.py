import json
import requests

from conftest import *

def test_create_application():
    application_data = {
        "staff_ID": 140003,
        "rolelisting_ID": 1,
        "application_date": "2023-10-12",
        "percentage_match": 38.9
    }

    response = requests.post(f'{backend_base_url}/addapplication', json=application_data)

    assert response.status_code == 201

    response_data = json.loads(response.content)
    assert "code" in response_data
    assert "data" in response_data
    assert "message" not in response_data
    
    response = requests.get(f'{backend_base_url}/applications/1')    
    
    assert response.status_code == 200
    
    response = requests.delete(f'{backend_base_url}/deleteapplications/140003/1')

    assert response.status_code == 200
        
        
def test_duplicate_application():
    
    application_data = {
        "staff_ID": 140002,
        "rolelisting_ID": 1,
        "application_date": "2023-10-12",
        "percentage_match": 38.9
    }
    
    response_duplicate = requests.post(f'{backend_base_url}/addapplication', json=application_data)

    assert response_duplicate.status_code == 400

    response_duplicate_data = json.loads(response_duplicate.content)

    assert "code" in response_duplicate_data
    assert "data" in response_duplicate_data
    assert "message" in response_duplicate_data
    assert response_duplicate_data["message"] == 'Application exists.'