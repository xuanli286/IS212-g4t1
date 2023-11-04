from selenium import webdriver
import chromedriver_autoinstaller
import pytest
from selenium.webdriver.common.by import By

backend_base_url = "http://18.143.92.81:5001"
backend_base_url_production = "http://18.143.92.81:5000" # ONLY USE FOR GET REQUEST or when need to show effect on frontend
frontend_base_url = "http://localhost:8080"

@pytest.fixture
def chrome_driver():
    
    # Install and configure Chrome WebDriver
    chromedriver_autoinstaller.install()
    chrome_options = webdriver.ChromeOptions()
    
    options = [
        "--window-size=1200,1200",
        "--ignore-certificate-errors",
        # "--headless",  # Enable headless mode
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage"
    ]

    for option in options:
        chrome_options.add_argument(option)
        
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    
    driver.quit()


# selenium login steps for User
def user_login(driver):
    staff_id = driver.find_element(By.ID, "staffId")
    staff_id.send_keys("140002")

    password = driver.find_element(By.ID, "password")
    password.send_keys("susan@123")

    login_button = driver.find_element(By.ID, "login")
    login_button.click()

# selenium login steps for Manager
def manager_login(driver):
    staff_id = driver.find_element(By.ID, "staffId")
    staff_id.send_keys("140008")

    password = driver.find_element(By.ID, "password")
    password.send_keys("jaclyn@123")

    login_button = driver.find_element(By.ID, "login")
    login_button.click()

# selenium login steps for HR
def hr_login(driver):
    staff_id = driver.find_element(By.ID, "staffId")
    staff_id.send_keys("160008")

    password = driver.find_element(By.ID, "password")
    password.send_keys("sally@123")

    login_button = driver.find_element(By.ID, "login")
    login_button.click()

