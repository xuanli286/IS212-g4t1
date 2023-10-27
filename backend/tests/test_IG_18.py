import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from conftest import *
import requests
import json
import math

@pytest.fixture
def url():
    return f'{frontend_base_url}/candidates'

##################### FRONTEND TESTING #####################

"""
    Check that left buttons should be disabled and input value should be 1 when on first page
"""

def test_min_page(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    driver.maximize_window()

    min_button = driver.find_element(By.CLASS_NAME, 'min_button')
    back_button = driver.find_element(By.CLASS_NAME, 'back_button')
    input_search = driver.find_element(By.CLASS_NAME, 'input-search')

    assert int(input_search.get_attribute('value')) == 1
    assert not min_button.is_enabled()
    assert not back_button.is_enabled()

    driver.close()


"""
    Check that right buttons should be disabled and input value should match output returned by backend on first page
"""

def test_max_page(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    driver.maximize_window()

    total_response = requests.get(f"{backend_base_url_production}/staff")
    total_data = json.loads(total_response.content)
    total = len(total_data['data']['staff'])

    if total == 0:
        total = 1

    max_page = math.ceil(total/20)

    wait = WebDriverWait(driver, 30)

    max_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'max_button')))
    max_button.click()

    right_button = driver.find_element(By.CLASS_NAME, 'right_button')
    max_page_on_fe = driver.find_element(By.CLASS_NAME, 'max_page').text
    input_search = driver.find_element(By.CLASS_NAME, 'input-search')

    assert int(input_search.get_attribute('value')) == max_page
    assert int(max_page_on_fe) == max_page 
    assert not max_button.is_enabled()
    assert not right_button.is_enabled()

    driver.close()

"""
    Check that user with Manager access can access Candidates on nav bar 
    and  be directed to candidates page when clicked

"""

def test_mgr_access_candidate_page(chrome_driver):

    driver = chrome_driver
    driver.get(frontend_base_url)
    driver.maximize_window()

    manager_login(driver)

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "candidates"))
    )

    candidate_link = driver.find_element(By.CLASS_NAME, "candidates")
    candidate_link.click()

    assert candidate_link.is_displayed()
    assert candidate_link.text == "Candidates"
    assert '/candidates' in driver.current_url
    driver.close()
    

"""
    Check that user with HR access can access Candidates on nav bar 
    and  be directed to candidates page when clicked

"""

def test_hr_access_candidate_page(chrome_driver):

    driver = chrome_driver
    driver.get(frontend_base_url)
    driver.maximize_window()

    hr_login(driver)

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "candidates"))
    )

    candidate_link = driver.find_element(By.CLASS_NAME, "candidates")
    candidate_link.click()

    assert candidate_link.is_displayed()
    assert candidate_link.text == "Candidates"
    assert '/candidates' in driver.current_url
    driver.close()


"""
    Check that user with staff access cannot see Candidates on nav bar

"""

def test_user_access_candidate_page(chrome_driver):

    driver = chrome_driver
    driver.get(frontend_base_url)
    driver.maximize_window()

    user_login(driver)

    try:
        # Check if the "candidates" element is visible
        driver.find_element(By.CLASS_NAME, "candidates")

    except NoSuchElementException:
        pass


"""
    Check if number of staffs shown on frontend is equivalent to
    the number of staffs actually on backend
"""

def test_staff_tally(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    driver.maximize_window()

    total_response = requests.get(f"{backend_base_url_production}/staff")
    total_data = json.loads(total_response.content)
    total = len(total_data['data']['staff'])

    if total == 0:
        total = 1

    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, 'records'), str(total))
    )

    frontend_text = driver.find_element(By.CLASS_NAME, 'records').text

    frontend_total = frontend_text.split()[-2]

    assert int(frontend_total) == total


"""
    Check that staff details are displayed
"""

def test_staff_details(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    driver.maximize_window()

    wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed
    staff_name = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'staff_name')))
    staff_ID = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'staff_ID')))
    staff_email = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'staff_email')))
    staff_dept = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'staff_dept')))
    staff_country = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'staff_country')))

    assert staff_name.is_displayed()
    assert staff_ID.is_displayed()
    assert staff_email.is_displayed()
    assert staff_dept.is_displayed()
    assert staff_country.is_displayed()


##################### BACKEND TESTING #####################

"""
    Check get all staff
"""

def test_get_all_staff():
    
    response = requests.get(f'{backend_base_url_production}/staff')

    assert response.status_code == 200

    response_data = json.loads(response.content)
    assert "code" in response_data
    assert "data" in response_data
    assert "message" not in response_data
    assert len(response_data["data"]["staff"]) == 555