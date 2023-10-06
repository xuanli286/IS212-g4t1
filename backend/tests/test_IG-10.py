# IG_10     Staff can view a specific role listing
import json
import pytest

from g4t1_test import *
from conftest import client, app
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def chrome_driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.fixture
def url():
    return "http://localhost:8080/viewspecificrolelisting/1"

rolelisting_ID = "1"

"""
    Check if unique Role Title, Role Description, Hiring Department, Required Skills Set, Application Deadline, 
    Reporting Manager, and the Geographic Location of the role are displayed for staff to view
"""
def test_all_visible_fields_selenium(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    fields = ["role-name", "role-description", "hiring-department", "required-skills", "application-deadline", "manager", "country"]
    for field in fields:
        fieldDisplayed = driver.find_element(By.ID, field)
        assert fieldDisplayed.is_displayed()


"""
    Check navigation back to the list of open role listings
"""
def test_back_button_selenium(chrome_driver, url):
    driver = chrome_driver
    previous_url = "http://localhost:8080/viewrolelistings"
    driver.get(previous_url)
    driver.get(url)
    back_btn = driver.find_element(By.ID, "back")
    back_btn.click()
    url_after_click = driver.current_url
    assert url_after_click == previous_url


"""
    Check for button to apply role
"""
def test_apply_role_button(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    apply_btn = driver.find_element(By.ID, "apply")
    assert apply_btn.is_displayed()


"""
    Check if role listing is currently open
"""
def test_application_deadline(client):
    with app.app_context():
        response = client.get('/rolelisting/' + rolelisting_ID)
        assert response.status_code == 200
        data = json.loads(response.data)["data"][rolelisting_ID]
        assert datetime.fromisoformat(data["application_deadline"]) >= datetime.now()


"""
    Check if values of role listing returned tallies with that stored in test database
"""
def test_all_available_fields(client):
    rolelisting_ID = "1"
    with app.app_context():
        # Fields: Role Title, Hiring Department, Application Deadline, Geographic Location of the role
        rolelisting_response = client.get('/rolelisting/' + rolelisting_ID)
        assert rolelisting_response.status_code == 200
        rolelisting_data = json.loads(rolelisting_response.data)["data"][rolelisting_ID]
        role_name = rolelisting_data["role_name"]
        assert role_name == "Software Engineer"
        assert rolelisting_data["dept"] == "Engineering Operation"
        assert rolelisting_data["application_deadline"] == "2023-12-31"
        assert rolelisting_data["country"] == "Hong Kong"
        manager_ID = str(rolelisting_data["manager_ID"])
        assert manager_ID == "1033"
        # Field: Reporting Manager
        staff_response = client.get('/staff/' + manager_ID)
        assert staff_response.status_code == 200
        staff_data = json.loads(staff_response.data)["data"][manager_ID]
        assert staff_data["staff_FName"] == "Philip"
        assert staff_data["staff_LName"] == "Lee"
        # Field: Role Description
        role_description_response = client.get('/get_all_role')
        assert role_description_response.status_code == 200
        role_description_data = json.loads(role_description_response.data)["data"]
        for idx in range(len(role_description_data)):
            if role_description_data[idx] == role_name:
                assert(role_description_data[idx][role_name] == "As a Software Engineer, you will be responsible for designing, developing, and maintaining software applications. You will collaborate with cross-functional teams to understand requirements, write code, and perform testing to ensure the software meets quality standards. Strong programming skills and problem-solving abilities are essential for success in this role.")
        # Field: Required Skills
        role_skill_response = client.get('/get_role_skill/' + role_name)
        assert role_skill_response.status_code == 200
        role_skill_data = json.loads(role_skill_response.data)["data"]
        assert(role_skill_data == ["Communication Skills", "Data Structures", "Problem Solving", "Version Control", "Web Development"])