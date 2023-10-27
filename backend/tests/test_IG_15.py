import json
import requests
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
    Check that all applicants are shown for a specific rolelisting
"""
def test_show_applicants(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    
    hr_login(driver)
    
    manage_route_button = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.ID, "manageRoute"))
    )
    manage_route_button.click()
    
    time.sleep(10)
    
    role_listings = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//li[contains(@class, "rolelisting-panel")]'))
    )
    applicant_element = role_listings[1].find_element(By.ID, 'numberApplicants')
    applicant_element.click()
    
    time.sleep(10)
    
    try:
        applications_panel = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'applicants-panel'))
        )
        assert applications_panel
        
    except TimeoutException:
        no_matching_application_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//li[@class="py-5 text-center message"]'))
        )
        assert no_matching_application_element.is_displayed()

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
        
        