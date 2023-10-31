import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from conftest import *
import requests
import json
import math
import time

@pytest.fixture
def url():
    return frontend_base_url

##################### FRONTEND TESTING #####################

"""
    Check that rolelisting, country, department & skill filter works and 
    only candidates that match the selected filters are returned 
"""

def test_successful_filter(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    driver.maximize_window()

    rolelisting_data = {
        "role_name": "Developer",
        "application_opening": "2023-10-30",
        "application_deadline": "2024-10-08",
        "dept": "Sales",
        "country": "Malaysia",
        "manager_ID": 140008
    }

    response = requests.post(f'{backend_base_url_production}/addrolelisting', json=rolelisting_data)

    assert response.status_code == 201

    response_data = json.loads(response.content)
    rolelisting_id = list(response_data["data"].keys())[0]

    manager_login(driver)

    wait = WebDriverWait(driver, 30)

    wait.until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "candidates"))
    )

    candidate_link = driver.find_element(By.CLASS_NAME, "candidates")
    candidate_link.click()

    """
    Check filter by rolelisting
    """

    time.sleep(100)

    """
    Check filter by country
    """

    wait.until(
        EC.presence_of_all_elements_located((By.ID, "country"))
    )

    dropdown = driver.find_element(By.ID, "country")

    select = Select(dropdown)
    select.select_by_visible_text("Malaysia")

    wait.until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'staff_country'))
    )
    
    staff_country = driver.find_element(By.CLASS_NAME, "staff_country").text

    assert staff_country == "Malaysia"

    """
    Check filter by rolelisting
    """

    wait.until(
        EC.presence_of_all_elements_located((By.ID, "rolelisting"))
    )

    dropdown = driver.find_element(By.ID, "rolelisting")

    select = Select(dropdown)
    select.select_by_visible_text("Account Manager")

    
    WebDriverWait(driver, 60).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'percentageMatch'))
    )

    
    staff_percentageMatch = driver.find_element(By.CLASS_NAME, "percentageMatch")

    assert staff_percentageMatch.is_displayed()


    """
    Check filter by department
    """

    wait.until(
        EC.presence_of_all_elements_located((By.ID, "department"))
    )

    dropdown = driver.find_element(By.ID, "department")

    select = Select(dropdown)
    select.select_by_visible_text("Sales")


    wait.until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'staff_dept'))
    )
    
    staff_dept = driver.find_element(By.CLASS_NAME, "staff_dept").text

    assert staff_dept == "Sales"

    """
    Check filter by skill
    """

    wait.until(
        EC.presence_of_all_elements_located((By.ID, "Collaboration"))
    )

    skill_checkbox = driver.find_element(By.ID, "Collaboration")
    skill_checkbox.click()

    WebDriverWait(driver, 60).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'percentageMatch'))
    )
    
    staff_percentageMatch = driver.find_element(By.CLASS_NAME, "percentageMatch")

    assert staff_percentageMatch.is_displayed()

    # delete rolelisting

    response = requests.delete(f'{backend_base_url_production}/deleterolelisting/{rolelisting_id}')

    assert response.status_code == 200

    driver.close()


"""
    Check that error message is displayed when there are no matching candidates
"""

def test_unsuccessful_filter(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    driver.maximize_window()

    manager_login(driver)

    wait = WebDriverWait(driver, 10)

    wait.until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "candidates"))
    )

    candidate_link = driver.find_element(By.CLASS_NAME, "candidates")
    candidate_link.click()

    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.ID, "country"))
    )

    dropdown = driver.find_element(By.ID, "country")


    select = Select(dropdown)
    select.select_by_visible_text("Indonesia")

    wait.until(
        EC.presence_of_all_elements_located((By.ID, "department"))
    )

    dropdown = driver.find_element(By.ID, "department")

    select = Select(dropdown)
    select.select_by_visible_text("Finance")


    wait.until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "noMatch"))
    )

    noMatch = driver.find_element(By.CLASS_NAME, "noMatch")

    assert noMatch.is_displayed()
    driver.close()


#################### BACKEND TESTING #####################

"""
    Check get all staff
"""

def test_get_all_staff():
    
    response = requests.get(f'{backend_base_url_production}/staff')

    assert response.status_code == 200

    response_data = json.loads(response.content)
    assert "code" in response_data
    assert "data" in response_data
    assert "message" not in response_data
    assert len(response_data["data"]["staff"]) == 555

"""
    Check get skills of specific staff
"""

def test_get_staff_skill():
    
    response = requests.get(f'{backend_base_url_production}/get_staff_skill/140001')

    assert response.status_code == 200

    response_data = json.loads(response.content)
    assert "code" in response_data
    assert "data" in response_data
    assert "message" not in response_data
    assert len(response_data["data"]) > 0

"""
    Check get skills of specific role
"""

def test_get_role_skill():
    
    response = requests.get(f'{backend_base_url_production}/get_role_skill/Developer')

    assert response.status_code == 200

    response_data = json.loads(response.content)
    assert "code" in response_data
    assert "data" in response_data
    assert "message" not in response_data
    assert len(response_data["data"]) > 0


"""
    Check get rolelisting by manager ID
"""

def test_get_rolelisting_by_managerID():

    rolelisting_data = {
        "role_name": "Account Manager",
        "application_opening": "2023-09-21",
        "application_deadline": "2023-12-31",
        "dept": "Consultancy",
        "country": "Singapore",
        "manager_ID": 151440
    }

    response = requests.post(f'{backend_base_url_production}/addrolelisting', json=rolelisting_data)

    assert response.status_code == 201

    response_data = json.loads(response.content)
    rolelisting_id = list(response_data["data"].keys())[0]
    
    response = requests.get(f'{backend_base_url_production}/openrolelisting?manager_ID=151440')

    assert response.status_code == 200

    response_data = json.loads(response.content)
    assert "code" in response_data
    assert "data" in response_data
    assert "message" not in response_data
    assert len(response_data["data"]) > 0

    # delete rolelisting

    response = requests.delete(f'{backend_base_url_production}/deleterolelisting/{rolelisting_id}')

    assert response.status_code == 200
