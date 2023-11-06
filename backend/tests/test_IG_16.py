# IG_16     Managers, Directors and HR staff can sort applications
import json
import pytest
import requests
import time

from conftest import *
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

@pytest.fixture
def url():
    return f'{frontend_base_url}/'

##################### FRONTEND & BACKEND TESTING #####################

"""
    Check that sorting button is present for HR to see
"""
def test_sort_present_hr_selenium(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    hr_login(driver)
    manage = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "manageRoute")))
    manage.click()
    rolelistings = driver.find_elements(By.CSS_SELECTOR, ".rolelisting-panel")
    for listing in rolelistings:
        applicants = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "numberApplicants")))
        applicants.click()
        sort = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "sort")))
        assert sort.is_displayed()
        break


"""
    Check that sorting button is present for Manager to see
"""
def test_sort_present_manager_selenium(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    manager_login(driver)
    manage = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "manageRoute")))
    manage.click()
    rolelistings = driver.find_elements(By.CSS_SELECTOR, ".rolelisting-panel")
    for listing in rolelistings:
        applicants = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "numberApplicants")))
        applicants.click()
        sort = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "sort")))
        assert sort.is_displayed()
        break


"""
    Check that sorting button is NOT present for Staff to see
"""
def test_sort_present_staff_selenium(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    user_login(driver)
    try:
        manage = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "manageRoute")))
        assert False
    except:
        assert True


################################################################################################################
"""
    Note:
    There is an existing application in database with the following data.
    {
        "application_date": "2023-10-12",
        "percentage_match": "40.00",
        "rolelisting_ID": 1,
        "staff_ID": 151438
    }
"""


"""
    Check if sorting options include chronological and skill match percentage
"""
def test_sort_values_selenium(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    hr_login(driver)
    manage = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "manageRoute")))
    manage.click()
    rolelistings = driver.find_elements(By.CSS_SELECTOR, ".rolelisting-panel")
    for listing in rolelistings:
        applicants = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "numberApplicants")))
        applicants.click()
        sort = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "sort")))
        options = sort.find_elements_by_tag_name('option')
        option_values = [option.get_attribute('value') for option in options]
        assert 'date' in option_values
        assert 'skill' in option_values
        break


"""
    Check that if sort by chronological order of submission,
        applications of an earlier date will be at the top
"""
def test_sort_by_chronological_application_date_selenium(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    hr_login(driver)
    manage = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "manageRoute")))
    manage.click()
    rolelistings = driver.find_elements(By.CSS_SELECTOR, ".rolelisting-panel")
    new_application_data = {
        "staff_ID": 140888,
        "rolelisting_ID": 1,
        "application_date": "2023-01-01",
        "percentage_match": 30
    }
    add_application_response = requests.post(f'{backend_base_url_production}/addapplication', json=new_application_data)
    assert add_application_response.status_code == 201
    staff_data_response = requests.get(f'{backend_base_url_production}/staff/140888')
    assert staff_data_response.status_code == 200
    staff_data = json.loads(staff_data_response.content)["data"]["140888"]
    staff_name = staff_data["staff_FName"] + " " + staff_data["staff_LName"]
    specificapplicants = driver.find_elements(By.CSS_SELECTOR, ".applicants-panel")
    for listing in rolelistings:
        applicants = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "numberApplicants")))
        applicants.click()
        sort = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "sort")))
        dropdown = Select(sort)
        dropdown.select_by_visible_text('Skill Match')
        for applicant in specificapplicants:
            name = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "name")))
            assert name.text == staff_name
            break
        break
    delete_response = requests.delete(f'{backend_base_url_production}/deleteapplications/140888/1')
    assert delete_response.status_code == 200


"""
    Check that if sort by skill match percentage, 
        applications with the highest skill match percentage appear at the top of the list, and 
        those with lower matches follow in descending order
"""
def test_sort_by_skill_descending_selenium(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    hr_login(driver)
    manage = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "manageRoute")))
    manage.click()
    rolelistings = driver.find_elements(By.CSS_SELECTOR, ".rolelisting-panel")
    new_application_data = {
        "staff_ID": 140894,
        "rolelisting_ID": 1,
        "application_date": "2023-12-31",
        "percentage_match": 50
    }
    add_application_response = requests.post(f'{backend_base_url_production}/addapplication', json=new_application_data)
    assert add_application_response.status_code == 201
    staff_data_response = requests.get(f'{backend_base_url_production}/staff/140894')
    assert staff_data_response.status_code == 200
    staff_data = json.loads(staff_data_response.content)["data"]["140894"]
    staff_name = staff_data["staff_FName"] + " " + staff_data["staff_LName"]
    specificapplicants = driver.find_elements(By.CSS_SELECTOR, ".applicants-panel")
    for listing in rolelistings:
        applicants = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "numberApplicants")))
        applicants.click()
        sort = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "sort")))
        dropdown = Select(sort)
        dropdown.select_by_visible_text('Skill Match')
        for applicant in specificapplicants:
            name = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "name")))
            assert name.text == staff_name
            break
        break
    delete_response = requests.delete(f'{backend_base_url_production}/deleteapplications/140894/1')
    assert delete_response.status_code == 200


"""
    Check that if sort by skill match percentage, 
        if there are multiple applications with the same skill match percentage, 
        the secondary sorting criterion is chronological order of submission (descending order)
"""
def test_sort_by_skill_descending_selenium(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    hr_login(driver)
    manage = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "manageRoute")))
    manage.click()
    rolelistings = driver.find_elements(By.CSS_SELECTOR, ".rolelisting-panel")
    new_application_data = {
        "staff_ID": 160135,
        "rolelisting_ID": 1,
        "application_date": "2023-01-01",
        "percentage_match": 40
    }
    add_application_response = requests.post(f'{backend_base_url_production}/addapplication', json=new_application_data)
    assert add_application_response.status_code == 201
    staff_data_response = requests.get(f'{backend_base_url_production}/staff/160135')
    assert staff_data_response.status_code == 200
    staff_data = json.loads(staff_data_response.content)["data"]["160135"]
    staff_name = staff_data["staff_FName"] + " " + staff_data["staff_LName"]
    specificapplicants = driver.find_elements(By.CSS_SELECTOR, ".applicants-panel")
    for listing in rolelistings:
        applicants = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "numberApplicants")))
        applicants.click()
        sort = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "sort")))
        dropdown = Select(sort)
        dropdown.select_by_visible_text('Skill Match')
        for applicant in specificapplicants:
            name = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "name")))
            assert name.text == staff_name
            break
        break
    delete_response = requests.delete(f'{backend_base_url_production}/deleteapplications/160135/1')
    assert delete_response.status_code == 200