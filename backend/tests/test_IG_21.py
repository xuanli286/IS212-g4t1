# IG_21      Staff can view their own skills profile
import pytest

from conftest import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def url():
    return f'{frontend_base_url}/'


"""
    Check if all user details are present
    (Staff ID, First Name, Last Name, Department, Country, Email, Skills)
"""
def test_user_details_selenium(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    user_login(driver)
    dropdown_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "dropdown")))
    dropdown_element.click()
    skillprofile_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "skillprofile")))
    skillprofile_element.click()
    fields = ["country", "dept", "email", "skill"]
    for field in fields:
        fieldDisplayed = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, field)))
        assert fieldDisplayed.is_displayed()