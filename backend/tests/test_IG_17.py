import json
import requests
from conftest import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urllib.parse import urlparse
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
    applicant_element = role_listings[0].find_element(By.ID, 'numberApplicants')
    applicant_element.click()
    
    time.sleep(10)
    
    current_url = driver.current_url
    parsed_url = urlparse(current_url)
    path_segments = parsed_url.path.split('/')
    rolelisting_id = path_segments[-1]
    
    # add application
    response = requests.delete(f'{backend_base_url_production}/deleteapplications/140008/{rolelisting_id}')
    
    application_data = {
        "staff_ID": 140008,
        "rolelisting_ID": rolelisting_id,
        "application_date": "2023-10-13",
        "percentage_match": 38.9
    }
    
    response = requests.post(f'{backend_base_url_production}/addapplication', json=application_data)
    
    time.sleep(10)
    
    application_element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//li[contains(@class, 'applicants-panel')]"))
    )

    application_element.click()
    
    time.sleep(10)
    
    name_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "name"))
    )
    assert name_element.text
    
    id_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "id"))
    )
    assert id_element.text
    
    percentageMatch_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "percentageMatch"))
    )
    assert percentageMatch_element.text
    
    email_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "email"))
    )
    assert email_element.text
    
    hiring_department_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "hiring-department"))
    )
    assert hiring_department_element.text
    
    country_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "country"))
    )
    assert country_element.text
    
    response = requests.delete(f'{backend_base_url_production}/deleteapplications/140008/{rolelisting_id}')

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

def test_get_staff_details():
    response = requests.get(f'{backend_base_url_production}/staff/140008')
    response_content = json.loads(response.content)
    
    assert "code" in response_content
    assert "data" in response_content
    assert "message" not in response_content

def test_get_staff_skills():
    response = requests.get(f'{backend_base_url_production}/get_staff_skill/140008')
    response_content = json.loads(response.content)
    
    assert "code" in response_content
    assert "data" in response_content
    assert "message" not in response_content
    
    assert len(response_content["data"]) > 0
    
def test_get_role_skill():
    response = requests.get(f'{backend_base_url_production}/get_role_skill/developer')
    response_content = json.loads(response.content)

    assert "code" in response_content
    assert "data" in response_content
    assert "message" not in response_content
    
    assert len(response_content["data"]) >= 0  