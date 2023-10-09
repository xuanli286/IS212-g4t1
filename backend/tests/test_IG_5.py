import pytest
from selenium.webdriver.common.by import By
from conftest import *

@pytest.fixture
def url():
    return f'{frontend_base_url}/rolelistingmanagement'

def test_add_rolelisting_button(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    assert driver.find_element(By.CSS_SELECTOR, "#addRoleListingButton").is_displayed()

def test_pill_color(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    if len(driver.find_elements(By.CSS_SELECTOR, ".rolelisting-panel")) > 0:
        rolelistings = driver.find_elements(By.CSS_SELECTOR, ".rolelisting-panel")
        for listing in rolelistings:
            if listing.find_element(By.CSS_SELECTOR, ".role-status"):
                statusPill = listing.find_element(By.CSS_SELECTOR, ".role-status")
                if statusPill.text == "Open":
                    assert "bg-green" in statusPill.get_attribute("class")
                elif statusPill.text == "Closed":
                    assert "bg-red" in statusPill.get_attribute("class")

def test_rolelisting_items(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    if len(driver.find_elements(By.CSS_SELECTOR, ".rolelisting-panel")) > 0:
        rolelistings = driver.find_elements(By.CSS_SELECTOR, ".rolelisting-panel")
        for listing in rolelistings:
            assert listing.find_element(By.XPATH, "//div[@label='role-title']").is_displayed()
            assert listing.find_element(By.XPATH, "//div[@label='role-manager']").is_displayed()
            assert listing.find_element(By.XPATH, "//div[@label='role-applicants']").is_displayed()
            assert listing.find_element(By.XPATH, "//div[@label='role-deadline']").is_displayed()
            assert listing.find_element(By.XPATH, "//div[@label='role-department']").is_displayed()
    else:
        assert driver.find_element(By.XPATH, "//div[contains(text(), 'No listings available!')]").is_displayed()