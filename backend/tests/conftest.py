from selenium import webdriver
import chromedriver_autoinstaller
import pytest

backend_base_url = "http://18.143.92.81:5001"
backend_base_url_production = "http://18.143.92.81:5000" # ONLY USE FOR GET REQUEST
frontend_base_url = "http://localhost:8080"

@pytest.fixture
def chrome_driver():
    
    # Install and configure Chrome WebDriver
    chromedriver_autoinstaller.install()
    chrome_options = webdriver.ChromeOptions()
    
    options = [
        "--window-size=1200,1200",
        "--ignore-certificate-errors",
        "--headless",  # Enable headless mode
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage"
    ]

    for option in options:
        chrome_options.add_argument(option)
        
    # Create and return the WebDriver instance
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    
    # Clean up resources by quitting the WebDriver
    driver.quit()

