# IG_21      Staff can view their own skills profile
import json
import pytest
import requests

from conftest import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def url():
    return f'{frontend_base_url}/'

##################### FRONTEND TESTING #####################

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


##################### BACKEND TESTING #####################


"""
    Check if skills data is returned
"""
def test_user_skills():
    staff_skills_response = requests.get(f'{backend_base_url_production}/get_staff_skill/140002')
    assert staff_skills_response.status_code == 200
    staff_skills = json.loads(staff_skills_response.content)["data"]
    correct_staff_skills = ['Accounting and Tax Systems', 'Business Environment Analysis', 'Customer Relationship Management', 'Professional and Business Ethics']
    assert staff_skills == correct_staff_skills