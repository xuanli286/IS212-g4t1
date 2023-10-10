# import pytest
from selenium import webdriver
import chromedriver_autoinstaller
from pyvirtualdisplay import Display
import pytest

backend_base_url = "http://13.212.177.124:5001"
frontend_base_url = "http://localhost:8080"

@pytest.fixture
def chrome_driver():
    # Set up a virtual display (for headless mode)
    display = Display(visible=0, size=(800, 800))
    display.start()
    
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

