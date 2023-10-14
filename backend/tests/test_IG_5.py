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
    return f'{frontend_base_url}/rolelistingmanagement'

##################### FRONTEND TESTING #####################

"""
    Check if add rolelisting button is displayed and clickable to the correct page
"""
def test_add_rolelisting_button(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    driver.maximize_window()
    driver.find_element(By.CSS_SELECTOR, "#addRoleListingButton").click()
    assert "/addrolelisting" in driver.current_url

"""
    Check if Open/Closed pill are the correct colors
"""
def test_pill_color(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    if len(driver.find_elements(By.CSS_SELECTOR, ".rolelisting-panel")) > 0:
        rolelistings = driver.find_elements(By.CSS_SELECTOR, ".rolelisting-panel")
        for listing in rolelistings:
            if listing.find_element(By.CSS_SELECTOR, ".role-status"):
                status_pill = listing.find_element(By.CSS_SELECTOR, ".role-status")
                if status_pill.text == "Open":
                    assert "bg-green" in status_pill.get_attribute("class")
                elif status_pill.text == "Closed":
                    assert "bg-red" in status_pill.get_attribute("class")

"""
    Check if all items on each rolelisting panel are displayed,
        if no rolelistings are available, the page should display 'No listings available!'
"""
def test_rolelisting_items(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".rolelisting-panel"))
    )

    if len(driver.find_elements(By.CSS_SELECTOR, ".rolelisting-panel")) > 0:
        rolelistings = driver.find_elements(By.CSS_SELECTOR, ".rolelisting-panel")
        for listing in rolelistings:
            assert listing.find_element(By.CSS_SELECTOR, ".role-title").is_displayed()
            assert listing.find_element(By.CSS_SELECTOR, ".role-manager").is_displayed()
            assert listing.find_element(By.CSS_SELECTOR, ".role-deadline").is_displayed()
            assert listing.find_element(By.CSS_SELECTOR, ".role-department").is_displayed()
            assert listing.find_element(By.CSS_SELECTOR, ".role-country").is_displayed()
    else:
        assert driver.find_element(By.XPATH, "//div[contains(text(), 'No listings available!')]").is_displayed()

"""
    Check if the status of the role listing shows:
        'Closed' if the deadline has passed
        'Open' if the deadline has not passed
"""
def test_date_and_pill(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    if len(driver.find_elements(By.CSS_SELECTOR, ".rolelisting-panel")) > 0:
        rolelistings = driver.find_elements(By.CSS_SELECTOR, ".rolelisting-panel")
        current_date = datetime.now()
        for listing in rolelistings:
            status_pill = listing.find_element(By.CSS_SELECTOR, ".role-status")
            date_string = listing.find_element(By.CSS_SELECTOR, ".role-deadline").text.split("by ")[1]
            date_format = "%d %B %Y"
            deadline = datetime.strptime(date_string, date_format)
            if deadline < current_date:
                assert "Closed" in status_pill.text 
            else:
                assert "Open" in status_pill.text

##################### BACKEND TESTING #####################

"""
    Check if number of rolelistings shown on frontend is equivalent to
    the number of rolelistings actually on backend
"""
def test_rolelisting_tally(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".rolelisting-panel"))
    )
    num_frontend = len(driver.find_elements(By.CSS_SELECTOR, ".rolelisting-panel"))

    closed_role_listings_response = requests.get(f'{backend_base_url_production}/closerolelisting')
    closed_role_listings = json.loads(closed_role_listings_response.content)
    if closed_role_listings['code'] == 404:
        closed_role_listings = []
    else:
        closed_role_listings = closed_role_listings['data']['rolelisting']

    open_role_listings_response = requests.get(f'{backend_base_url_production}/openrolelisting')
    open_role_listings = json.loads(open_role_listings_response.content)
    if open_role_listings['code'] == 404:
        open_role_listings = []
    else:
        open_role_listings = open_role_listings['data']['rolelisting']

    num_backend = len(closed_role_listings) + len(open_role_listings)

    assert num_frontend == num_backend
