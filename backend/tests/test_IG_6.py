import json
import requests
from conftest import *

##################### FRONTEND TESTING ####################


##################### BACKEND TESTING #####################

def test_create_rolelisting():
    rolelisting_data = {
            "role_name": "Account Manager",
            "application_opening": "2023-09-21",
            "application_deadline": "2023-12-31",
            "dept": "Consultancy",
            "country": "Hong Kong",
            "manager_ID": 140003
        }

    response = requests.post(f'{backend_base_url}/addrolelisting', json=rolelisting_data)

    assert response.status_code == 201

    response_data = json.loads(response.content)
    assert "code" in response_data
    assert "data" in response_data
    assert "message" not in response_data
    
    for key, item_data in response_data['data'].items():
        rolelisting_id = key
        retrieved_data = item_data
        
    response = requests.get(f'{backend_base_url}/rolelisting/{rolelisting_id}')
    
    assert response.status_code == 200
    
    assert retrieved_data["role_name"] == rolelisting_data["role_name"]
    assert retrieved_data["application_opening"] == rolelisting_data["application_opening"]
    assert retrieved_data["application_deadline"] == rolelisting_data["application_deadline"]
    assert retrieved_data["dept"] == rolelisting_data["dept"]
    assert retrieved_data["country"] == rolelisting_data["country"]
    assert retrieved_data["manager_ID"] == rolelisting_data["manager_ID"]
    
    response = requests.delete(f'{backend_base_url}/deleterolelisting/{rolelisting_id}')

    assert response.status_code == 200
        
        
def test_duplicate_rolelisting():
    
    rolelisting_data = {
        "role_name": "Call Centre",
        "application_opening": "2023-09-15",
        "application_deadline": "2023-10-28",
        "manager_ID": 140003,
        "dept": "Sales",
        "country": "Vietnam",
    }
    
    response_duplicate = requests.post(f'{backend_base_url}/addrolelisting', json=rolelisting_data)

    assert response_duplicate.status_code == 400

    response_duplicate_data = json.loads(response_duplicate.content)

    assert "code" in response_duplicate_data
    assert "data" in response_duplicate_data
    assert "message" in response_duplicate_data
    assert response_duplicate_data["message"] == 'Role Listing exists.'

def test_get_dept():
    
    response = requests.get(f'{backend_base_url}/get_dept_country/dept')

    assert response.status_code == 200
    
    response_data = json.loads(response.content)
    assert "code" in response_data
    assert "data" in response_data
    
    dept_list = response_data["data"]
    
    assert len(dept_list) !=0
    

def test_get_country():
    
    response = requests.get(f'{backend_base_url}/get_dept_country/country')

    assert response.status_code == 200
    
    response_data = json.loads(response.content)
    assert "code" in response_data
    assert "data" in response_data
    
    country_list = response_data["data"]
    
    assert len(country_list) !=0


