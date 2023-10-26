import json
import requests
from conftest import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

##################### FRONTEND TESTING ####################
@pytest.fixture
def url():
    return f'{frontend_base_url}/'

def test_search_selenium(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)

    user_login(driver)

    search_input = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "role-search")))
    search_input.send_keys("Developer")

    search_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "search-button")))
    search_button.click()

    # have to check on this
    search_result = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "rolelisting-1")))

    assert search_result.is_displayed()
