import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from g4t1 import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    
    # Create the test database
    with app.app_context():
        db.create_all() 
        print("Test database created successfully.")

    with app.test_client() as client:
        yield client
    
    # Drop the test database
    with app.app_context():
        db.drop_all() 
        print("Test database dropped successfully.")