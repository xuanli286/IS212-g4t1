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
    
    results = []

    role_listings = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//li[contains(@class, "rolelisting-panel")]'))
    )
    for listing in role_listings:
        role_title = listing.find_element(By.CLASS_NAME, 'role-title').text
        results.append(role_title == "Developer")
    assert all(results)

##################### BACKEND TESTING ####################

def test_get_open_rolelisting():
    
    response = requests.get(f'{backend_base_url_production}/openrolelisting')
    response_content = json.loads(response.content)

    assert "code" in response_content
    assert "data" in response_content
    assert "message" not in response_content
    
    assert len(response_content["data"]) >= 0
    
def test_get_role_skill():
    response = requests.get(f'{backend_base_url_production}/get_role_skill/developer')
    response_content = json.loads(response.content)

    assert "code" in response_content
    assert "data" in response_content
    assert "message" not in response_content
    
    assert len(response_content["data"]) >= 0

