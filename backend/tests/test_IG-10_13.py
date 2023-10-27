# IG_10     Staff can view a specific role listing
# IG_13     Staff can view role-skill match
import json
import pytest
import requests
import time

from conftest import *
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def url():
    return f'{frontend_base_url}/'

rolelisting_ID = "4"

"""
    Check if unique Role Title, Role Description, Hiring Department, Required Skills Set, Application Deadline, 
    Reporting Manager, and the Geographic Location of the role are displayed for staff to view
"""
def test_all_visible_fields_selenium(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    user_login(driver)
    rolelistings = driver.find_elements(By.CSS_SELECTOR, ".rolelisting-panel")
    for listing in rolelistings:
        listing.click()
        fields = ["role-name", "role-description", "hiring-department", "required-skills", "application-deadline", "manager", "country"]
        for field in fields:
            fieldDisplayed = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, field)))
            assert fieldDisplayed.is_displayed()
        break

"""
    Check navigation back to the list of open role listings
"""
def test_back_button_selenium(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    user_login(driver)
    rolelistings = driver.find_elements(By.CSS_SELECTOR, ".rolelisting-panel")
    for listing in rolelistings:
        listing.click()
        previous_url = f"{frontend_base_url}/home"
        back_btn = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "back")))
        back_btn.click()
        url_after_click = driver.current_url
        assert url_after_click == previous_url
        break


"""
    Check for button to apply role
"""
def test_apply_role_button(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    user_login(driver)
    rolelistings = driver.find_elements(By.CSS_SELECTOR, ".rolelisting-panel")
    for listing in rolelistings:
        listing.click()
        apply_btn = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "applyButton")))
        assert apply_btn.is_displayed()
        break


"""
    Check if 
        percentage match between my skills and the skills required for the role
        list of matched and missing skills
    are displayed
"""
def test_percentage_match_selenium(chrome_driver, url): 
    driver = chrome_driver
    driver.get(url)
    user_login(driver)
    rolelistings = driver.find_elements(By.CSS_SELECTOR, ".rolelisting-panel")
    for listing in rolelistings:
        listing.click()
        fields = ["percentage", "matched-skills", "missing-skills"]
        for field in fields:
            fieldDisplayed = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, field)))
            assert fieldDisplayed.is_displayed()
        break


"""
    Check if role listing is currently open
"""
def test_application_deadline():
    response = requests.get(f'{backend_base_url_production}/rolelisting/{rolelisting_ID}')
    assert response.status_code == 200
    data = json.loads(response.content)["data"][rolelisting_ID]
    assert datetime.fromisoformat(data["application_deadline"]) >= datetime.now()


"""
    Check if values of role listing returned tallies with that stored in test database
"""
def test_all_available_fields():
    rolelisting_data = {
        "role_name": "Account Manager",
        "application_opening": "2023-09-21",
        "application_deadline": "2024-12-31",
        "dept": "Consultancy",
        "country": "Vietnam",
        "manager_ID": 140003
    }
    add_response = requests.post(f'{backend_base_url}/addrolelisting', json=rolelisting_data)
    assert add_response.status_code == 201
    for key in json.loads(add_response.content)['data'].keys():
        new_role_listing_id = key
    # Fields: Role Title, Hiring Department, Application Deadline, Geographic Location of the role
    rolelisting_response = requests.get(f'{backend_base_url}/rolelisting/{new_role_listing_id}')
    assert rolelisting_response.status_code == 200
    rolelisting_data = json.loads(rolelisting_response.content)["data"][new_role_listing_id]
    role_name = rolelisting_data["role_name"]
    assert role_name == "Account Manager"
    assert rolelisting_data["dept"] == "Consultancy"
    assert rolelisting_data["application_deadline"] == "2024-12-31"
    assert rolelisting_data["country"] == "Vietnam"
    manager_ID = str(rolelisting_data["manager_ID"])
    assert manager_ID == "140003"
    # Field: Reporting Manager
    staff_response = requests.get(f'{backend_base_url_production}/staff/{manager_ID}')
    assert staff_response.status_code == 200
    staff_data = json.loads(staff_response.content)["data"][manager_ID]
    assert staff_data["staff_FName"] == "Janice"
    assert staff_data["staff_LName"] == "Chan"
    # Field: Role Description
    role_description_response = requests.get(f'{backend_base_url_production}/get_all_role')
    assert role_description_response.status_code == 200
    role_description_data = json.loads(role_description_response.content)["data"]
    for idx in range(len(role_description_data)):
        if role_description_data[idx] == role_name:
            assert(role_description_data[idx][role_name] == "The Account Manager acts as a key point of contact between an organisation and its clients. He/She possesses thorough product knowledge and oversees product and/or service sales. He works with customers to identify their wants and prepares reports by collecting, analysing, and summarising sales information. He contacts existing customers to discuss and give recommendations on how specific products or services can meet their needs. He maintains customer relationships to strategically place new products and drive sales for long-term growth. He works in a fast-paced and dynamic environment, and travels frequently to clients' premises for meetings. He is familiar with client relationship management and sales tools. He is knowledgeable of the organisation's products and services, as well as trends, developments and challenges of the industry domain. The Sales Account Manager is a resourceful, people-focused and persistent individual, who takes rejection as a personal challenge to succeed when given opportunity. He appreciates the value of long lasting relationships and prioritises efforts to build trust with existing and potential customers. He exhibits good listening skills and is able to establish rapport with customers and team members alike easily.")
    # Field: Required Skills
    role_skill_response = requests.get(f'{backend_base_url_production}/get_role_skill/{role_name}')
    assert role_skill_response.status_code == 200
    role_skill_data = json.loads(role_skill_response.content)["data"]
    assert(role_skill_data == ["Account Management", "Budgeting", "Business Development", "Business Needs Analysis", "Business Negotiation", "Collaboration", "Communication", "Data Analytics", "Pricing Strategy", "Problem Solving", "Product Management", "Sales Strategy", "Stakeholder Management"])
    delete_response = requests.delete(f'{backend_base_url}/deleterolelisting/{new_role_listing_id}')
    assert delete_response.status_code == 200