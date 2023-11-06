# IG_8      HR staff can update a role listing
import json
import pytest
import datetime
import requests

from conftest import *
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def url():
    return f'{frontend_base_url}/editrolelisting/1'


##################### FRONTEND TESTING #####################

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

def test_update_role_listing():
    rolelisting_data = {
        "role_name": "Account Manager",
        "application_opening": "2023-09-21",
        "application_deadline": "2023-12-31",
        "dept": "Consultancy",
        "country": "Hong Kong",
        "manager_ID": 140003
    }
    add_response = requests.post(f'{backend_base_url}/addrolelisting', json=rolelisting_data)
    assert add_response.status_code == 201
    for key in json.loads(add_response.content)['data'].keys():
        new_role_listing_id = key

    updated_data = {
        "role_name": "Account Manager",
        "application_opening": "2023-09-20",
        "application_deadline": "2023-12-30",
        "manager_ID": 140001,
        "dept": "Consultancy",
        "country": "Vietnam",
    }
    response = requests.put(f'{backend_base_url}/updaterolelisting/{new_role_listing_id}', json=updated_data)
    assert response.status_code == 200
    updated_role_listing = json.loads(response.content)["data"][new_role_listing_id]
    assert updated_role_listing["role_name"] == "Account Manager"
    assert updated_role_listing["application_opening"] == "2023-09-20"
    assert updated_role_listing["application_deadline"] == "2023-12-30"
    assert updated_role_listing["dept"] == "Consultancy"
    assert updated_role_listing["country"] == "Vietnam"
    actual_data = {
        "role_name": "Account Manager",
        "application_opening": "2023-09-21",
        "application_deadline": "2023-12-31",
        "manager_ID": 140001,
        "dept": "Consultancy",
        "country": "Hong Kong",
    }
    cleaned_response = requests.put(f'{backend_base_url}/updaterolelisting/{new_role_listing_id}', json=actual_data)
    assert cleaned_response.status_code == 200
    delete_response = requests.delete(f'{backend_base_url}/deleterolelisting/{new_role_listing_id}')
    assert delete_response.status_code == 200


def test_update_duplicate_role_listing():
    rolelisting_data = {
        "role_name": "Account Manager",
        "application_opening": "2023-09-21",
        "application_deadline": "2023-12-31",
        "dept": "Consultancy",
        "country": "Hong Kong",
        "manager_ID": 140001
    }
    add_response = requests.post(f'{backend_base_url}/addrolelisting', json=rolelisting_data)
    assert add_response.status_code == 201
    for key in json.loads(add_response.content)['data'].keys():
        new_role_listing_id = key
    duplicate_update_data = {
        "role_name": "Account Manager",
        "application_opening": "2023-09-21",
        "application_deadline": "2023-12-31",
        "manager_ID": 140001,
        "dept": "Consultancy",
        "country": "Hong Kong",
    }
    response = requests.put(f'{backend_base_url}/updaterolelisting/{new_role_listing_id}', json=duplicate_update_data)
    assert response.status_code == 400
    delete_response = requests.delete(f'{backend_base_url}/deleterolelisting/{new_role_listing_id}')
    assert delete_response.status_code == 200