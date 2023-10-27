import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import *
from datetime import datetime
import requests
import json
import time
from selenium.common.exceptions import TimeoutException

##################### FRONTEND TESTING #####################
@pytest.fixture
def url():
    return f'{frontend_base_url}/'

"""
    Check if filter by country work successfully
"""
def test_successful_filter_country(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)

    hr_login(driver)
    
    manage_route_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "manageRoute"))
    )
    manage_route_button.click()

    country_element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, 'country'))
    )

    option_to_select = WebDriverWait(country_element, 10).until(
        EC.presence_of_element_located((By.XPATH, ".//option[text()='Malaysia']"))
    )
    option_to_select.click()
    
    time.sleep(10)
    
    country_results = []

    try:
        role_listings = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//li[contains(@class, "rolelisting-panel")]'))
        )
        for listing in role_listings:
            role_country = listing.find_element(By.CLASS_NAME, 'role-country').text
            country_results.append(role_country == "Malaysia")

        assert all(country_results)
    except TimeoutException:
        no_matching_roles_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//li[@class="py-5 text-center message"]'))
        )
        assert no_matching_roles_element.is_displayed()


"""
    Check if filter by department work successfully
"""
def test_successful_filter_department(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)

    hr_login(driver)
    
    manage_route_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "manageRoute"))
    )
    manage_route_button.click()

    department_element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, 'department'))
    )

    option_to_select = WebDriverWait(department_element, 10).until(
        EC.presence_of_element_located((By.XPATH, ".//option[text()='Consultancy']"))
    )
    option_to_select.click()
    
    time.sleep(20)
    
    department_results = []
    
    try:
        role_listings = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//li[contains(@class, "rolelisting-panel")]'))
        )
        for listing in role_listings:
            role_department = listing.find_element(By.CLASS_NAME, 'role-department').text
            department_results.append(role_department == "Consultancy")
        assert all(department_results)
    except TimeoutException:
        no_matching_roles_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//li[@class="py-5 text-center message"]'))
        )
        assert no_matching_roles_element.is_displayed()

"""
    Check if filter by skills work successfully
"""
def test_successful_filter_skills(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)

    hr_login(driver)
    
    manage_route_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "manageRoute"))
    )
    manage_route_button.click()

    checkbox_label = "Accounting and Tax Systems"
    checkbox = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, checkbox_label))
    )

    checkbox.click()
    assert checkbox.is_selected()
    
    time.sleep(10)
    
    allMatch = []
    
    try:
        role_listings = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//li[contains(@class, "rolelisting-panel")]'))
        )
        for listing in role_listings:
            role_title = listing.find_element(By.CLASS_NAME, 'role-title').text
            response = requests.get(f'{backend_base_url_production}/get_role_skill/{role_title}')
            skills = json.loads(response.content)["data"]
            skillMatch = False
            for skill in skills:
                if skill == checkbox_label:
                    skillMatch = True
            allMatch.append(skillMatch)
        assert all(allMatch)
        
    except TimeoutException:
        no_matching_roles_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//li[@class="py-5 text-center message"]'))
        )
        assert no_matching_roles_element.is_displayed()
        
"""
    Check if clear filter button works
"""
def test_clear_filter(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)

    hr_login(driver)

    clear_filter_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "clearFilterButton"))
    )
    clear_filter_button.click()

    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element_value((By.ID, "country"), "all")
    )
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element_value((By.ID, "department"), "all")
    )
    
    assert driver.find_element(By.ID, "country").get_attribute("value") == "all"
    assert driver.find_element(By.ID, "department").get_attribute("value") == "all"

    selected_skills_checkboxes = driver.find_elements(By.CLASS_NAME, "skill")
    for checkbox in selected_skills_checkboxes:
        assert not checkbox.is_selected()
        
##################### BACKEND TESTING #####################

def test_get_all_skill():
    
    response = requests.get(f'{backend_base_url_production}/get_all_skill')
    response_content = json.loads(response.content)

    assert "code" in response_content
    assert "data" in response_content
    assert "message" not in response_content
    
    assert len(response_content["data"]) == 81
    
def test_get_country():
    
    response = requests.get(f'{backend_base_url_production}/get_dept_country/country')
    response_content = json.loads(response.content)

    assert "code" in response_content
    assert "data" in response_content
    assert "message" not in response_content
    
    assert len(response_content["data"]) == 5
    
def test_get_dept():
    
    response = requests.get(f'{backend_base_url_production}/get_dept_country/dept')
    response_content = json.loads(response.content)

    assert "code" in response_content
    assert "data" in response_content
    assert "message" not in response_content
    
    assert len(response_content["data"]) == 9
    
def test_get_open_rolelisting():
    
    response = requests.get(f'{backend_base_url_production}/openrolelisting')
    response_content = json.loads(response.content)

    assert "code" in response_content
    assert "data" in response_content
    assert "message" not in response_content
    
    assert len(response_content["data"]) >= 0
    
def test_get_close_rolelisting():
    
    response = requests.get(f'{backend_base_url_production}/closerolelisting')
    response_content = json.loads(response.content)

    assert "code" in response_content
    assert "data" in response_content
    assert "message" not in response_content
    
    assert len(response_content["data"]) >= 0
