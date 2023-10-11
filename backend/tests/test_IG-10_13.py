# IG_10     Staff can view a specific role listing
# IG_13     Staff can view role-skill match
import json
import pytest
import requests

from g4t1_test import *
from conftest import *
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
    return f'{frontend_base_url}/viewspecificrolelisting/1'

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
    previous_url = f"{frontend_base_url}/viewrolelistings"
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
    Check if 
        percentage match between my skills and the skills required for the role
        list of matched and missing skills
    are displayed
"""
def test_percentage_match_selenium(chrome_driver, url): 
    driver = chrome_driver
    driver.get(url)
    fields = ["percentage", "matched-skills", "missing-skills"]
    for field in fields:
        fieldDisplayed = driver.find_element(By.ID, field)
        assert fieldDisplayed.is_displayed()


"""
    Check if role listing is currently open
"""
def test_application_deadline():
    response = requests.get(f'{backend_base_url}/rolelisting/{rolelisting_ID}')
    assert response.status_code == 200
    data = json.loads(response.content)["data"][rolelisting_ID]
    assert datetime.fromisoformat(data["application_deadline"]) >= datetime.now()


"""
    Check if values of role listing returned tallies with that stored in test database
"""
def test_all_available_fields():
    rolelisting_ID = "1"
    # Fields: Role Title, Hiring Department, Application Deadline, Geographic Location of the role
    rolelisting_response = requests.get(f'{backend_base_url}/rolelisting/{rolelisting_ID}')
    assert rolelisting_response.status_code == 200
    rolelisting_data = json.loads(rolelisting_response.content)["data"][rolelisting_ID]
    role_name = rolelisting_data["role_name"]
    assert role_name == "Call Centre"
    assert rolelisting_data["dept"] == "Sales"
    assert rolelisting_data["application_deadline"] == "2024-10-28"
    assert rolelisting_data["country"] == "Vietnam"
    manager_ID = str(rolelisting_data["manager_ID"])
    assert manager_ID == "140003"
    # Field: Reporting Manager
    staff_response = requests.get(f'{backend_base_url}/staff/{manager_ID}')
    assert staff_response.status_code == 200
    staff_data = json.loads(staff_response.content)["data"][manager_ID]
    assert staff_data["staff_FName"] == "Janice"
    assert staff_data["staff_LName"] == "Chan"
    # Field: Role Description
    role_description_response = requests.get(f'{backend_base_url}/get_all_role')
    assert role_description_response.status_code == 200
    role_description_data = json.loads(role_description_response.content)["data"]
    for idx in range(len(role_description_data)):
        if role_description_data[idx] == role_name:
            assert(role_description_data[idx][role_name] == "Call Centre Executive is responsible for providing assistance to customers by addressing their queries and requests. He/She advises customers on appropriate products and services based on their needs. He is responsible for the preparation of customer documentation. In the case of complex customer requests, he escalates them to senior officers. He is able to abide by safety and/or security standards in the workplace. The Call Centre Executive  pays strong attention to details to verify and process documentation. He also shows initiative and quick decision-making skills to provide excellent personalised customer services and support. He is comfortable with various stakeholder interactions whilst working in shifts and possesses adequate computer literacy to process customer documentation.")
    # Field: Required Skills
    role_skill_response = requests.get(f'{backend_base_url}/get_role_skill/{role_name}')
    assert role_skill_response.status_code == 200
    role_skill_data = json.loads(role_skill_response.content)["data"]
    assert(role_skill_data == ["Call Centre Management", "Collaboration", "Communication", "Customer Relationship Management", "Digital Fluency", "Problem Solving", "Stakeholder Management", "Technology Application"])