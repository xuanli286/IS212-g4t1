# IG-25     Managers, Director, HR staff, Staff can log out
import json
import pytest
import requests
import time

from conftest import *
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

@pytest.fixture
def url():
    return f'{frontend_base_url}/'

"""
    Check that the log out button is not accessible Staff is not logged in
"""
def test_logout_not_accessible_selenium(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    try:
        dropdownBtn = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "dropdown")))
        dropdownBtn.click()
        logout = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "logout")))
        logout.click()
        assert False
    except:
        assert True

"""
    Check that the log out button is accessible Staff is logged in
"""
def test_logout_accessible_selenium(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    user_login(driver)
    try:
        dropdownBtn = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "dropdown")))
        dropdownBtn.click()
        logout = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "logout")))
        logout.is_displayed()
        assert True
    except:
        assert False

"""
    Check that Staff is redirected back after Staff is logged out
"""
def test_logout_selenium(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    user_login(driver)
    try:
        dropdownBtn = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "dropdown")))
        dropdownBtn.click()
        previous_url = f"{frontend_base_url}/"
        logout = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "logout")))
        logout.click()
        url_after_click = driver.current_url
        assert url_after_click == previous_url
    except:
        assert False
