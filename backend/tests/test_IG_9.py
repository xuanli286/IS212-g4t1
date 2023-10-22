# import pytest
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from conftest import *
# from datetime import datetime
# import requests
# import json

# @pytest.fixture
# def url():
#     return f'{frontend_base_url}/rolelistingstaff'

# ##################### FRONTEND TESTING #####################

# """
#     Check if all items on each rolelisting panel are displayed,
#         if no rolelistings are available, the page should display 'No listings available!'
# """
# def test_rolelisting_items(chrome_driver, url):
#     driver = chrome_driver
#     driver.get(url)
    
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".rolelisting-panel"))
#     )
    
#     if len(driver.find_elements(By.CSS_SELECTOR, ".rolelisting-panel")) > 0:
#         rolelistings = driver.find_elements(By.CSS_SELECTOR, ".rolelisting-panel")
#         for listing in rolelistings:
#             assert listing.find_element(By.CSS_SELECTOR, ".role-title").is_displayed()
#             assert listing.find_element(By.CSS_SELECTOR, ".role-manager").is_displayed()
#             assert listing.find_element(By.CSS_SELECTOR, ".role-applicants").is_displayed()
#             assert listing.find_element(By.CSS_SELECTOR, ".role-deadline").is_displayed()
#             assert listing.find_element(By.CSS_SELECTOR, ".role-department").is_displayed()
#             assert listing.find_element(By.CSS_SELECTOR, ".role-country").is_displayed()
#     else:
#         assert driver.find_element(By.XPATH, "//div[contains(text(), 'No listings available!')]").is_displayed()

# """
#     Check if number of rolelistings shown on frontend is equivalent to
#     the number of rolelistings on backend
# """
# def test_openrolelisting(chrome_driver, url):
#     driver = chrome_driver
#     driver.get(url)
    
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".rolelisting-panel"))
#     )

#     num_frontend = len(driver.find_elements(By.CSS_SELECTOR, ".rolelisting-panel"))

#     open_role_listings_response = requests.get(f'{backend_base_url_production}/openrolelisting')
#     open_role_listings = json.loads(open_role_listings_response.content)
#     if open_role_listings['code'] == 404:
#         open_role_listings = []
#     else:
#         open_role_listings = open_role_listings['data']['rolelisting']

#     assert len(open_role_listings) == num_frontend


# ##################### BACKEND TESTING #####################





