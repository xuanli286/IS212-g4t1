import json
import requests
import pytest
from conftest import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

##################### FRONTEND TESTING ####################

@pytest.fixture
def url():
    return f'{frontend_base_url}'

"""
    Check that candidate's details are shown correctly
"""
def test_candidates_details(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    
    hr_login(driver)
    
    candidate_route_button = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "candidateRoute"))
    )
    candidate_route_button.click()
    
    time.sleep(10)
    
    candidate = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, '130001'))
    )
    candidate.click()
    
    time.sleep(10)
    
    name = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'name'))
    )
    assert name.text.strip() != ""
    
    department = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'department'))
    )
    assert department.text.strip() != ""
    
    email = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'email'))
    )
    assert email.text.strip() != ""
    
    staffID = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'staffID'))
    )
    assert staffID.text.strip() != ""
    
    country = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'country'))
    )
    assert country.text.strip() != ""
    
    try:
        ul_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "staff-skills"))
        )

        li_elements = ul_element.find_elements(By.TAG_NAME, "li")   

        assert len(li_elements) > 0  
    except:
        error_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "no-skills"))
        )
        assert error_element.text.strip() != ""
        
    

##################### BACKEND TESTING #####################
def test_get_staff():
    
    response = requests.get(f'{backend_base_url}/staff/130001')

    assert response.status_code == 200
    
    response_data = json.loads(response.content)
    assert "code" in response_data
    assert "data" in response_data
    assert "message" not in response_data

def test_get_staff_skills():
    response = requests.get(f'{backend_base_url_production}/get_staff_skill/140008')
    response_content = json.loads(response.content)
    
    assert "code" in response_content
    assert "data" in response_content
    assert "message" not in response_content
    
    assert len(response_content["data"]) > 0
        
        