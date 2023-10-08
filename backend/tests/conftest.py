import pytest
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
from pyvirtualdisplay import Display

backend_base_url = "http://13.212.177.124:5000"        
frontend_base_url = "http://localhost:8080"

@pytest.fixture
def chrome_driver():
    # driver = webdriver.Chrome()
    # yield driver
    # driver.quit()
    display = Display(visible=0, size=(800, 800))  
    display.start()
    
    chromedriver_autoinstaller.install()
    chrome_options = webdriver.ChromeOptions()    
    options = [
    "--window-size=1200,1200",
        "--ignore-certificate-errors"
    
        #"--headless",
        #"--disable-gpu",
        #"--window-size=1920,1200",
        #"--ignore-certificate-errors",
        #"--disable-extensions",
        #"--no-sandbox",
        #"--disable-dev-shm-usage",
        #'--remote-debugging-port=9222'
    ]

    for option in options:
        chrome_options.add_argument(option)
        
    driver = webdriver.Chrome(options = chrome_options)
    return driver