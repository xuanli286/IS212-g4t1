import json
import requests

from conftest import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

@pytest.fixture
def url():
    return f'{frontend_base_url}/'

##################### FRONTEND TESTING #####################

"""
    Check if HR has access to both View and Manage Role Listing
"""
def test_hr_manage_role_listing_selenium(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    hr_login(driver)
    view = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "View")]')))
    assert view.is_displayed()
    manage = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "Manage")]')))
    assert manage.is_displayed()

"""
    Check if Staff has access to ONLY View Role Listing
"""
def test_user_view_role_listing_selenium(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    user_login(driver)
    view = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "viewRoute")))
    assert view.is_displayed()
    
    try:
        manage = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "manageRoute")))
        assert False
    except:
        assert True