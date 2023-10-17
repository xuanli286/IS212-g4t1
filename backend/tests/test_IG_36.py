import json
import requests
from conftest import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


##################### FRONTEND TESTING ####################

"""
    Check if manager dropdown has all elements as expected
"""
@pytest.fixture
def url():
    return f'{frontend_base_url}/addrolelisting'

def test_manager_dropdown_selenium(chrome_driver, url):
    driver = chrome_driver
    driver.get(url)
    
    manager_dropdown = driver.find_element(By.ID, "manager")
    
    manager_dropdown.click()
    
    select = Select(manager_dropdown)
    
    all_options = [option.text for option in select.options]
    
    response = requests.get(f'{backend_base_url}/staff')
    expected_options=[]
    
    if response.status_code == 200:
        response_data = json.loads(response.content)
        staff_list = response_data["data"]["staff"]

        for item in staff_list:
            for key in item:
                if key in ["staff_FName", "staff_LName"]:
                    expected_options.append(f"{item[key]['staff_FName']} {item[key]['staff_LName']}")
    
    assert all(option in all_options for option in expected_options)

##################### BACKEND TESTING #####################

def test_get_staff():
    
    response = requests.get(f'{backend_base_url}/staff')

    assert response.status_code == 200
    
    response_data = json.loads(response.content)
    assert "code" in response_data
    assert "data" in response_data
    
    staff_list = response_data["data"]["staff"]
    
    assert len(staff_list) !=0