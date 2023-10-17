import json
import requests

from conftest import *
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def url():
    return f'{frontend_base_url}'

##################### FRONTEND TESTING ####################
def test_successful_application_selenium(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)

    staff_id = driver.find_element(By.ID, "staffID")
    staff_id.send_keys("140002")

    password = driver.find_element(By.ID, "password")
    password.send_keys("susan@123")

    login_button = driver.find_element(By.ID, "login")
    login_button.click()

    role_listing_button = driver.find_element(By.ID, "rolelisting-1")
    role_listing_button.click()

    requests.delete(f'{backend_base_url}/deleteapplications/140002/1')
    apply_button = driver.find_element(By.ID, "applyButton")
    apply_button.click()
    submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "submitButton")))
    submit_button.click()
    success_message = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "successMessage")))
    assert success_message.is_displayed()


##################### BACKEND TESTING #####################

def test_create_application():
    application_data = {
        "staff_ID": 140003,
        "rolelisting_ID": 15,
        "application_date": "2023-10-12",
        "percentage_match": 38.9
    }

    response = requests.post(f'{backend_base_url}/addapplication', json=application_data)

    assert response.status_code == 201

    response_data = json.loads(response.content)
    assert "code" in response_data
    assert "data" in response_data
    assert "message" not in response_data
    
    response = requests.get(f'{backend_base_url}/applications/15')    
    
    assert response.status_code == 200
    
    response = requests.delete(f'{backend_base_url}/deleteapplications/140003/15')

    assert response.status_code == 200
        
        
def test_duplicate_application():
    
    application_data = {
        "staff_ID": 140002,
        "rolelisting_ID": 15,
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