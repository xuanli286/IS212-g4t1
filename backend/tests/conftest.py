import pytest
from selenium import webdriver

backend_base_url = "http://13.229.118.77:5000"        
frontend_base_url = "http://localhost:8080"

@pytest.fixture
def chrome_driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()
    return driver

