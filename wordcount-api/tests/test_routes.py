import pytest
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
from app import app

# Test cases for word count API
inputJsonList =[
    {"text": "This is a test", "expected_word_count": 4},
    {"text": "Another test case", "expected_word_count": 3},
    {"text": "One more test", "expected_word_count": 3},
    {"text": "", "expected_word_count": 0}
]

# Test case for valid JSON input
@pytest.mark.parametrize("data", inputJsonList)
def test_getWordCount(data):
    client = app.test_client()
    response = client.post("/wordcount", json={"text": data["text"]})
    assert response.status_code == 200
    assert response.json == {"wordCount": data["expected_word_count"]}


# Test case for invalid JSON input
def test_invalid_word_count():
    client = app.test_client()
    response = client.post("/wordcount", json={"text": 123})
    assert response.status_code == 400
    assert response.json == {"error": "Invalid input"}


# Test case for empty JSON
def test_invalid_json():
    client = app.test_client()
    response = client.post("/wordcount", json={})
    assert response.status_code == 400
    assert response.json == {"error": "Invalid input"}


# Test case for invalid HTTP method
def test_invalid_http_method():
    client = app.test_client()
    response = client.get("/wordcount")
    assert response.status_code == 405


# Test case for No JSON data
def test_missing_json_data():
    client = app.test_client()
    response = client.post("/wordcount")
    assert response.status_code == 400
    assert response.json == {"error": "Invalid input"}
