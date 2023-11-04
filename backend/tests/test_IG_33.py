import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import *
from datetime import datetime
import requests
import json

@pytest.fixture
def url():
    return f'{frontend_base_url}'

##################### FRONTEND TESTING #####################

"""
    Check if applicant number is shown on each rolelisting panel
        else, the page should display 'No listings available!'
"""
def test_rolelisting_applications(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)

    hr_login(driver)

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "manage"))
    )

    manage_link = driver.find_element(By.ID, "manageRoute")
    manage_link.click()
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".rolelisting-panel"))
    )

    if len(driver.find_elements(By.CSS_SELECTOR, ".rolelisting-panel")) > 0:
        rolelistings = driver.find_elements(By.CSS_SELECTOR, ".rolelisting-panel")
        for listing in rolelistings:
            assert listing.find_element(By.CSS_SELECTOR, ".role-applicants").is_displayed()
    else:
        assert driver.find_element(By.XPATH, "//div[contains(text(), 'No listings available!')]").is_displayed()