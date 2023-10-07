import json
import requests
from conftest import *

##################### FRONTEND TESTING ####################


##################### BACKEND TESTING #####################

def test_get_staff():
    
    response = requests.get(f'{backend_base_url}/staff')

    assert response.status_code == 200
    
    response_data = json.loads(response.content)
    assert "code" in response_data
    assert "data" in response_data
    
    staff_list = response_data["data"]["staff"]
    
    assert len(staff_list) !=0



