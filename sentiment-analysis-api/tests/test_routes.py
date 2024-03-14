import pytest
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from app import app

# Create a test client using the Flask application context
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

input_json_list = [
    {"text":"I am happy","result":"positive"},
    {"text":"I am sad","result":"negative"},
    {"text":"I am neutral","result":"neutral"}
]
# Test the /analyzesentiment route
@pytest.mark.parametrize("data", input_json_list)
def test_get_sentiment(client,data):
    response = client.post("/analyzesentiment", json={"text":data["text"]})
    assert response.status_code == 200
    assert response.json == {"result": data["result"]}

# Define test data for invalid and empty inputs
invalid_and_empty_inputs = [
    ({"text": 123}, {"error": "Invalid input"}),
    ({}, {"error": "Invalid input"}),
    ({"message:": "I am happy"}, {"error": "Invalid input"})
]

# Test the /analyzesentiment route for invalid and empty inputs
@pytest.mark.parametrize("input_data, expected_response", invalid_and_empty_inputs)
def test_get_sentiment_invalid_input(client, input_data, expected_response):
    response = client.post("/analyzesentiment", json=input_data)
    assert response.status_code == 400
    assert response.json == expected_response