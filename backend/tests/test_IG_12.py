import json
import requests
from conftest import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

##################### FRONTEND TESTING ####################
@pytest.fixture
def url():
    return frontend_base_url

def test_search_title(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)

    user_login(driver)

    search_input = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "role-search")))
    search_input.send_keys("Developer")

    search_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "search-button")))
    search_button.click()
    
    time.sleep(10)
    
    results = []
    
    try:
        role_listings = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//li[contains(@class, "rolelisting-panel")]'))
        )
        for listing in role_listings:
            role_title = listing.find_element(By.CLASS_NAME, 'role-title').text
            results.append(role_title == "Developer")

    except TimeoutException:
        no_matching_roles_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//li[@class="py-5 text-center message"]'))
        )
        assert no_matching_roles_element.is_displayed()

    if results[0]:
        assert all(results)

def test_search_country(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)

    user_login(driver)

    search_input = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "role-search")))
    search_input.send_keys("Singapore")

    search_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "search-button")))
    search_button.click()
    
    time.sleep(10)
    
    results = []
    
    try:
        role_listings = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//li[contains(@class, "rolelisting-panel")]'))
        )
        for listing in role_listings:
            role_title = listing.find_element(By.CLASS_NAME, 'role-title').text
            results.append(role_title == "Developer")

    except TimeoutException:
        no_matching_roles_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//li[@class="py-5 text-center message"]'))
        )
        assert no_matching_roles_element.is_displayed()

    if results[0]:
        assert all(results)

    
def test_search_department(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)

    user_login(driver)

    search_input = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "role-search")))
    search_input.send_keys("Sales")

    search_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "search-button")))
    search_button.click()
    
    time.sleep(30)
    
    results = []
    
    try:
        role_listings = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//li[contains(@class, "rolelisting-panel")]'))
        )
        for listing in role_listings:
            role_title = listing.find_element(By.CLASS_NAME, 'role-title').text
            results.append(role_title == "Developer")           

    except TimeoutException:
        no_matching_roles_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//li[@class="py-5 text-center message"]'))
        )
        assert no_matching_roles_element.is_displayed()

    if results[0]:
        assert all(results)
    
def test_search_skills(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)

    user_login(driver)

    search_input = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "role-search")))
    search_input.send_keys("Developer")

    search_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "search-button")))
    search_button.click()
    
    time.sleep(10)
    
    results = []
    
    try:
        role_listings = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//li[contains(@class, "rolelisting-panel")]'))
        )
        for listing in role_listings:
            role_title = listing.find_element(By.CLASS_NAME, 'role-title').text
            results.append(role_title == "Developer")

    except TimeoutException:
        no_matching_roles_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//li[@class="py-5 text-center message"]'))
        )
        assert no_matching_roles_element.is_displayed()

    if results[0]:
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

