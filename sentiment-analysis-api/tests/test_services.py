import pytest
import os
import sys  # Add the path to the project root directory to the system path

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
from app import app  # Import the Flask application
from app.sentiment_analysis_services import json_validation,check_input_type  # Import the function to be tested


# Create a test client using the Flask application context
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


input_json_list = [
    {"text": "This is a test", "result": True},
    {"text": 123, "result": False},
    {"text": {}, "result": False},
    {"other_field": "I am happy", "result": False},
    {"text": None, "result": False},
    {"text": "This is one field","other_field":"additional data", "result": True},
]

# Test the json_validation function
@pytest.mark.parametrize("data", input_json_list)
def test_json_validation(data):
    assert json_validation(data) == data["result"]


# Test cases for the check_input_type function
@pytest.mark.parametrize("input_data, expected_result", [
    ("test", True),        
    (123, False),           
    ({"key": "value"}, False), 
    ([1, 2, 3], False),     
    (True, False),          
    (None, False)           
])
def test_check_input_type(input_data, expected_result):
    assert check_input_type(input_data) == expected_result
