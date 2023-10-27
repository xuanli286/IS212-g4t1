import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import *
from datetime import datetime
import requests
import json

@pytest.fixture
def url():
    return f'{frontend_base_url}/'

##################### FRONTEND TESTING #####################


##################### BACKEND TESTING #####################

def test_get_all_skill():
    
    response = requests.get(f'{backend_base_url_production}/get_all_skill')
    response_content = json.loads(response.content)

    assert "code" in response_content
    assert "data" in response_content
    assert "message" not in response_content
    
    assert len(response_content["data"]) == 81
    
def test_get_country():
    
    response = requests.get(f'{backend_base_url_production}/get_dept_country/country')
    response_content = json.loads(response.content)

    assert "code" in response_content
    assert "data" in response_content
    assert "message" not in response_content
    
    assert len(response_content["data"]) == 5
    
def test_get_dept():
    
    response = requests.get(f'{backend_base_url_production}/get_dept_country/dept')
    response_content = json.loads(response.content)

    assert "code" in response_content
    assert "data" in response_content
    assert "message" not in response_content
    
    assert len(response_content["data"]) == 9
    
def test_get_open_rolelisting():
    
    response = requests.get(f'{backend_base_url_production}/openrolelisting')
    response_content = json.loads(response.content)

    assert "code" in response_content
    assert "data" in response_content
    assert "message" not in response_content
    
    assert len(response_content["data"]) >= 0
    
def test_get_close_rolelisting():
    
    response = requests.get(f'{backend_base_url_production}/closerolelisting')
    response_content = json.loads(response.content)

    assert "code" in response_content
    assert "data" in response_content
    assert "message" not in response_content
    
    assert len(response_content["data"]) >= 0
