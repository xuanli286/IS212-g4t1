import json
import requests
from conftest import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


##################### FRONTEND TESTING ####################

@pytest.fixture
def url():
    return f'{frontend_base_url}/addrolelisting'




##################### BACKEND TESTING #####################

def test_get_applications():
    
    response = requests.get(f'{backend_base_url}/applications/1')

    assert response.status_code == 200 or response.status_code == 404
    response_data = json.loads(response.content)
    
    if (response.status_code == 200):
        assert "code" in response_data
        assert "data" in response_data
        
        application_list = response_data["data"]
        
        assert len(application_list) !=0
        
    elif (response.status_code == 404):
        assert "code" in response_data
        assert "message" in response_data
        
        assert response_data["message"] == "There are no applicants for the role."

def test_get_rolelisting():
    
        response = requests.get(f'{backend_base_url}/rolelisting/1')

        assert response.status_code == 200
        
        response_data = json.loads(response.content)
        
        assert "code" in response_data
        assert "data" in response_data
        
        