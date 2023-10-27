import json
import requests

from conftest import *
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def url():
    return f'{frontend_base_url}/'

##################### FRONTEND TESTING ####################
"""
    Check if user can submit application for a role listing successfully
"""
def test_successful_application_selenium(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)

    user_login(driver)

    role_listing_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "rolelisting-1")))
    role_listing_button.click()

    requests.delete(f'{backend_base_url_production}/deleteapplications/140002/1')
    
    apply_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "applyButton")))
    apply_button.click()
    submit_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "submitButton")))
    submit_button.click()
    success_message = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "successMessage")))
    
    requests.delete(f'{backend_base_url_production}/deleteapplications/140002/1')
    assert success_message.is_displayed()

"""
    Check if user can submit application for a role listing unsuccessfully
"""
def test_unsuccessful_application_selenium(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)

    user_login(driver)

    role_listing_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "rolelisting-2")))
    role_listing_button.click()
    
    apply_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "applyButton")))
    apply_button.click()
    submit_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "submitButton")))
    submit_button.click()
    error_message = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "unsuccessfulMessage")))
    
    assert error_message.is_displayed()
    
##################### BACKEND TESTING #####################

def test_create_application():
    
    response = requests.delete(f'{backend_base_url}/deleteapplications/140008/1')
    
    application_data = {
        "staff_ID": 140008,
        "rolelisting_ID": 1,
        "application_date": "2023-10-13",
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
    
    response = requests.delete(f'{backend_base_url}/deleteapplications/140008/1')

    assert response.status_code == 200
        
        
def test_duplicate_application():
    
    application_data = {
        "staff_ID": 140002,
        "rolelisting_ID": 1,
        "application_date": "2023-10-12",
        "percentage_match": 38.9
    }
    response = requests.post(f'{backend_base_url}/addapplication', json=application_data)
    
    response_duplicate = requests.post(f'{backend_base_url}/addapplication', json=application_data)

    assert response_duplicate.status_code == 400

    response_duplicate_data = json.loads(response_duplicate.content)

    assert "code" in response_duplicate_data
    assert "data" in response_duplicate_data
    assert "message" in response_duplicate_data
    assert response_duplicate_data["message"] == 'Application exists.'