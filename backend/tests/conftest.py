import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from g4t1_test import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True

    # Create the test database
    with app.app_context():
        db.create_all()

    # Create a test client for the application
    with app.test_client() as client:
        yield client

    # Drop the test database after the tests are finished
    with app.app_context():
        db.drop_all()