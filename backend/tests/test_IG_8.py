# IG_8   HR staff can update a role listing
import json
import pytest
import datetime

from g4t1_test import *
from conftest import client, app
from sqlalchemy.exc import IntegrityError
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def chrome_driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.fixture
def url():
    return "http://localhost:8080/editrolelisting/1"


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


"""
    Check that success modal pops up upon valid input data (i.e. no duplicate role listing)
"""
def test_valid_update_role_listing_selenium(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    # "role_name": "Consultant"
    title_select = driver.find_element(By.ID, "title")
    title_select.click()
    title_option_to_select = driver.find_element(By.XPATH, '//option[text()="Consultant"]')
    title_option_to_select.click()
    # "application_opening": today's date
    current_date = datetime.now().date()
    current_date_formatted = current_date.strftime("%m-%d-%Y")
    application_opening_input = driver.find_element(By.ID, "applicationOpening")
    application_opening_input.clear()
    application_opening_input.send_keys(current_date_formatted)
    # "application_deadline": 1 day after today's date/application_opening
    application_deadline = current_date + timedelta(days=1)
    application_deadline_formatted = application_deadline.strftime("%m-%d-%Y")
    application_deadline_input = driver.find_element(By.ID, 'applicationDeadline')
    application_deadline_input.clear()
    application_deadline_input.send_keys(application_deadline_formatted)
    # "manager_ID": 1030
    manager_select = driver.find_element(By.ID, "manager")
    manager_select.click()
    manager_option_to_select = driver.find_element(By.XPATH, '//option[text()="Derek Tan (1030)"]')
    manager_option_to_select.click()
    # "dept": "Finance"
    department_select = driver.find_element(By.ID, "department")
    department_select.click()
    department_option_to_select = driver.find_element(By.XPATH, '//option[text()="Finance"]')
    department_option_to_select.click()
    # "country": "Hong Kong"
    country_select = driver.find_element(By.ID, "country")
    country_select.click()
    country_option_to_select = driver.find_element(By.XPATH, '//option[text()="Hong Kong"]')
    country_option_to_select.click()
    # Save
    save_button = driver.find_element(By.XPATH, '//button[text()="Save Edit"]')
    save_button.click()
    success_message = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//p[text()="Role listing has been updated successfully."]')))
    assert success_message.is_displayed()


"""
    Check that error modal pops up upon invalid input data (i.e. duplicate role listing)
"""
def test_invalid_update_role_listing_selenium(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    # "role_name": "Consultant"
    title_select = driver.find_element(By.ID, "title")
    title_select.click()
    title_option_to_select = driver.find_element(By.XPATH, '//option[text()="Consultant"]')
    title_option_to_select.click()
    # "application_opening": today's date
    current_date = datetime.now().date()
    current_date_formatted = current_date.strftime("%m-%d-%Y")
    application_opening_input = driver.find_element(By.ID, "applicationOpening")
    application_opening_input.clear()
    application_opening_input.send_keys(current_date_formatted)
    # "application_deadline": 1 day after today's date/application_opening
    application_deadline = current_date + timedelta(days=1)
    application_deadline_formatted = application_deadline.strftime("%m-%d-%Y")
    application_deadline_input = driver.find_element(By.ID, 'applicationDeadline')
    application_deadline_input.clear()
    application_deadline_input.send_keys(application_deadline_formatted)
    # "manager_ID": 1030
    manager_select = driver.find_element(By.ID, "manager")
    manager_select.click()
    manager_option_to_select = driver.find_element(By.XPATH, '//option[text()="Derek Tan (1030)"]')
    manager_option_to_select.click()
    # "dept": "Finance"
    department_select = driver.find_element(By.ID, "department")
    department_select.click()
    department_option_to_select = driver.find_element(By.XPATH, '//option[text()="Finance"]')
    department_option_to_select.click()
    # "country": "Hong Kong"
    country_select = driver.find_element(By.ID, "country")
    country_select.click()
    country_option_to_select = driver.find_element(By.XPATH, '//option[text()="Hong Kong"]')
    country_option_to_select.click()
    # Save
    save_button = driver.find_element(By.XPATH, '//button[text()="Save Edit"]')
    save_button.click()
    success_message = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//p[text()="Role Listing exists."]')))
    assert success_message.is_displayed()


##################### BACKEND TESTING #####################

# def test_update_role_listing(client):
#     updated_data = {
#         "role_name": "Consultant",
#         "application_opening": "2023-10-01",
#         "application_deadline": "2023-10-15",
#         "manager_ID": 1030,
#         "dept": "Finance",
#         "country": "Hong Kong",
#     }
#     with app.app_context():
#         latest_rolelisting_ID = str(RoleListing.query.order_by(RoleListing.rolelisting_ID.desc()).first().rolelisting_ID)
#         response = client.put('/updaterolelisting/'+latest_rolelisting_ID, json=updated_data)
#         assert response.status_code == 200
#         updated_role_listing = json.loads(response.data)["data"][latest_rolelisting_ID]
#         assert updated_role_listing["role_name"] == "Consultant"
#         assert updated_role_listing["application_opening"] == "2023-10-01"
#         assert updated_role_listing["application_deadline"] == "2023-10-15"
#         assert updated_role_listing["dept"] == "Finance"
#         assert updated_role_listing["country"] == "Hong Kong"

# def test_update_duplicate_role_listing(client):
#     duplicate_update_data = {
#         "role_name": "Consultant",
#         "application_opening": "2023-10-01",
#         "application_deadline": "2023-10-15",
#         "manager_ID": 1030,
#         "dept": "Finance",
#         "country": "Hong Kong",
#     }
#     with app.app_context():
#         latest_rolelisting_ID = str(RoleListing.query.order_by(RoleListing.rolelisting_ID.desc()).first().rolelisting_ID)
#         response = client.put('/updaterolelisting/'+latest_rolelisting_ID, json=duplicate_update_data)
#         assert response.status_code == 400