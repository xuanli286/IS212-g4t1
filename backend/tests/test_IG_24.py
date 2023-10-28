import json
import requests
from conftest import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

##################### FRONTEND TESTING ####################
@pytest.fixture
def url():
    return f'{frontend_base_url}/'

"""
    Check if user can log in successfully
"""
def test_login_selenium(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    
    staff_id = driver.find_element(By.ID, "staffId")
    staff_id.send_keys("130001")
    
    password = driver.find_element(By.ID, "password")
    password.send_keys("john@123")
    
    login_button = driver.find_element(By.ID, "login")
    login_button.click()
    
    success_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "title")))
    
    assert success_element, "Login was not successful"

"""
    Check if the correct error message is display if user input wrong log in details
"""
def test_invalid_login_selenium(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    
    staff_id = driver.find_element(By.ID, "staffId")
    staff_id.send_keys("130001")
    
    password = driver.find_element(By.ID, "password")
    password.send_keys("john@12345678")
    
    login_button = driver.find_element(By.ID, "login")
    login_button.click()
    
    error_message_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "errorMessage")))
    
    assert error_message_element.is_displayed(), "Error message is not displayed"

##################### BACKEND TESTING #####################

def test_get_staff():
    
    response = requests.get(f'{backend_base_url}/staff')

    assert response.status_code == 200
    
    response_data = json.loads(response.content)
    assert "code" in response_data
    assert "data" in response_data
    
    staff_list = response_data["data"]["staff"]
    
    assert len(staff_list) !=0



