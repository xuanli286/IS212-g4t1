import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import *
from datetime import datetime
import requests
import json

# @pytest.fixture
# def url():
#     return f'{frontend_base_url}/'

##################### BACKEND TESTING #####################

"""
    Check if number of rolelistings shown on frontend is equivalent to
    the number of rolelistings actually on backend
"""
def test_get_all_skill():
    
    response = requests.get(f'{backend_base_url_production}/get_all_skill')
    response_content = json.loads(response.content)

    assert "code" in response_content
    assert "data" in response_content
    assert "message" not in response_content

    print(response_content)
    
    assert len(response_content["data"]) == 81
