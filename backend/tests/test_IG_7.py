import json
import pytest
import requests
import time

from conftest import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def url():
    return f'{frontend_base_url}/'


##################### FRONTEND TESTING #####################

"""
    Check if unique Role Title, Role Description, Hiring Department, Required Skills Set, Application Deadline, 
    Reporting Manager, and the Geographic Location of the role are displayed for HR to view
"""
def test_all_visible_fields_selenium(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    hr_login(driver)

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.ID, "manageRoute"))
    )

    manage_link = driver.find_element(By.ID, "manageRoute")
    manage_link.click()

    time.sleep(10)

    rolelistings = driver.find_elements(By.CSS_SELECTOR, ".rolelisting-panel")
    for listing in rolelistings:
        listing.click()

        time.sleep(10)

        fields = ["role-name", "role-description", "hiring-department", "required-skills", "application-deadline", "manager", "country"]
        for field in fields:
            fieldDisplayed = driver.find_element(By.ID, field)
            assert fieldDisplayed.is_displayed()
        break

"""
    Check navigation back to the list of open role listings
"""
def test_back_button_selenium(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    hr_login(driver)

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.ID, "manageRoute"))
    )

    manage_link = driver.find_element(By.ID, "manageRoute")
    manage_link.click()

    time.sleep(10)

    rolelistings = driver.find_elements(By.CSS_SELECTOR, ".rolelisting-panel")
    for listing in rolelistings:
        listing.click()
        previous_url = f"{frontend_base_url}/rolelistingmanagement"
        time.sleep(10)
        back_btn = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "back")))
        back_btn.click()
        url_after_click = driver.current_url
        assert url_after_click == previous_url
        break


##################### BACKEND TESTING #####################

"""
    Check get specific rolelisting
"""

def test_get_rolelisting():
    
    response = requests.get(f'{backend_base_url_production}/rolelisting/1')

    assert response.status_code == 200
    
    response_data = json.loads(response.content)
    
    assert "code" in response_data
    assert "data" in response_data
    assert "message" not in response_data
