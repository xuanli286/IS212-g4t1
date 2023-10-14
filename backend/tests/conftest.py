import pytest
from selenium import webdriver

backend_base_url = "http://13.212.177.124:5001"
backend_base_url_production = "http://13.212.177.124:5000" # ONLY USE FOR GET REQUEST
frontend_base_url = "http://localhost:8080"

@pytest.fixture
def chrome_driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()
    return driver

