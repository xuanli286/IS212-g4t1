import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

@pytest.fixture
def chrome_driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.fixture
def url():
    return "http://localhost:8080/rolelistingmanagement"

def test_add_rolelisting_button(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    assert driver.find_element(By.CSS_SELECTOR, "#addRoleListingButton").is_displayed()

def test_open_pill_color(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    openPill = driver.find_element(By.XPATH, "//*[contains(text(), 'Open')]/..")    
    assert "bg-green" in openPill.get_attribute("class")

def test_closed_pill_color(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    closedPill = driver.find_element(By.XPATH, "//*[contains(text(), 'Closed')]/..")    
    assert "bg-red" in closedPill.get_attribute("class")

def test_rolelistings(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    rolelistings = driver.find_elements(By.CSS_SELECTOR, ".rolelisting-panel")
    for listing in rolelistings:
        assert listing.is_displayed()

def test_rolelisting_items(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    rolelistings = driver.find_elements(By.CSS_SELECTOR, ".rolelisting-panel")
    for listing in rolelistings:
        assert listing.find_element(By.XPATH, "//div[@label='role-title']").is_displayed()
        assert listing.find_element(By.XPATH, "//div[@label='role-manager']").is_displayed()
        assert listing.find_element(By.XPATH, "//div[@label='role-applicants']").is_displayed()
        assert listing.find_element(By.XPATH, "//div[@label='role-deadline']").is_displayed()
        assert listing.find_element(By.XPATH, "//div[@label='role-department']").is_displayed()