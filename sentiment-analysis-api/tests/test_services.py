import pytest
import os
import sys  # Add the path to the project root directory to the system path

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
from app import app  # Import the Flask application
from app.sentiment_analysis_services import json_validation


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
]


@pytest.mark.parametrize("data", input_json_list)
def test_json_validation(data):

    for data in input_json_list:
        assert json_validation(data["text"]) == data["result"]
