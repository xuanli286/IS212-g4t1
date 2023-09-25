import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def chrome_driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.mark.parametrize("url, element_selector", [
    ("http://localhost:8080/rolelistingmanagement", "#roleListings"),
    # Add more test cases as needed
])
def test_check_rolelistings_ui(chrome_driver, url, element_selector):
    driver = chrome_driver
    
    driver.get(url)
    element = driver.find_element(By.CSS_SELECTOR, element_selector)
    
    assert element.is_displayed()