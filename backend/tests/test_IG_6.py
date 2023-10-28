import json
import requests
from conftest import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import Select

##################### FRONTEND TESTING ####################
@pytest.fixture
def url():
    return f'{frontend_base_url}/addrolelisting'

"""
    Check that the earliest date clickable for Application Opening field is today's date
"""
def test_clickable_application_opening_selenium(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    application_opening_input = driver.find_element(By.ID, "applicationOpening")
    current_date = datetime.now().date()
    min_opening_date = application_opening_input.get_attribute("min")
    min_opening_date = datetime.strptime(min_opening_date, "%Y-%m-%d").date()
    assert min_opening_date >= current_date
    assert application_opening_input.is_enabled()


"""
    Check that the earliest date clickable for Application Deadline field is 
        either 1 day after Application Opening
        or 1 day after today's date, 
    whichever is larger
"""
def test_clickable_application_deadline_selenium(chrome_driver, url): 
    driver = chrome_driver
    driver.get(url)
    application_deadline_input = driver.find_element(By.ID, "applicationDeadline")
    application_opening_input = driver.find_element(By.ID, "applicationOpening")
    application_opening_date = application_opening_input.get_attribute("value")
    min_opening_date = datetime.strptime(application_opening_date, "%Y-%m-%d").date()
    current_date = datetime.now().date()
    min_closing_date = application_deadline_input.get_attribute("min")
    min_closing_date = datetime.strptime(min_closing_date, "%Y-%m-%d").date()
    correct_min_closing = max(min_opening_date + timedelta(days=1), current_date + timedelta(days=1))
    assert min_closing_date == correct_min_closing


"""
    Check that 
        if a user keys into Application Opening field a value that is earlier than today's date,
        its value will be automatically set to today's date
"""
def test_user_input_application_opening_selenium(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    application_opening_input = driver.find_element(By.ID, "applicationOpening")
    application_opening_input.clear()
    application_opening_input.send_keys('10-01-2022')
    application_opening_date = application_opening_input.get_attribute("value")
    application_opening_date = datetime.strptime(application_opening_date, "%Y-%m-%d").date()
    current_date = datetime.now().date()
    assert application_opening_date == current_date


"""
    Check that 
        if a user keys into Application Deadline field a value that is NOT
            either 1 day after Application Opening
            or 1 day after today's date, 
        whichever is larger,
        its value will be automatically set to the correct/valid input
"""
def test_user_input_application_deadline_selenium(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    application_deadline_input = driver.find_element(By.ID, "applicationDeadline")
    application_deadline_input.clear()
    application_deadline_input.send_keys('10-01-2022')
    application_deadline_date = application_deadline_input.get_attribute("value")
    application_deadline_date = datetime.strptime(application_deadline_date, "%Y-%m-%d").date()
    application_opening_input = driver.find_element(By.ID, "applicationOpening")
    application_opening_date = application_opening_input.get_attribute("value")
    application_opening_date = datetime.strptime(application_opening_date, "%Y-%m-%d").date()
    current_date = datetime.now().date()
    correct_application_closing = max(application_opening_date + timedelta(days=1), current_date + timedelta(days=1))
    assert application_deadline_date == correct_application_closing



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
    
    response = requests.post(f'{backend_base_url}/addrolelisting', json=rolelisting_data)
    
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


