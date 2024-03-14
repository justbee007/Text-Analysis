import pytest
import os, pytest
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) # This is the path to the root of the project
sys.path.append(PROJECT_ROOT) # This is to add the project root to the system path so that we can import the app module
from app import app


# The client fixture is used to make requests to the application
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


# Test the register_services route
input_json_list = [
    {
        "input": {"name": "sentiment analysis", "url": "http://127.0.1/wordcount"},
        "response": {"status_code": 201, "message": "Service registered successfully"},
    },
    {
        "input": {"name": "sentiment analysis", "url": "http://127.0.1/wordcount"},
        "response": {"status_code": 409, "message": "Service already exists"},
    },
]


# Test the register_services route
@pytest.mark.parametrize("data", input_json_list)
def test_register_services(client, data):
    response = client.post("/services", json=data["input"])
    assert response.status_code == data["response"]["status_code"]
    assert response.json["message"] == data["response"]["message"]


# Test the register_services route with invalid input
invalid_input_list = [
    {
        "input": {},
        "response": {
            "status_code": 400,
            "message": "Request body must be a JSON object",
        },
    },
    {
        "input": {"name": "sentiment analysis"},
        "response": {
            "status_code": 400,
            "message": "Request body must contain name and url",
        },
    },
    {
        "input": {"url": "http://127.0.1/wordcount"},
        "response": {
            "status_code": 400,
            "message": "Request body must contain name and url",
        },
    },
]


# Test the register_services route with invalid input
@pytest.mark.parametrize("data", invalid_input_list)
def test_register_services_invalid_input(client, data):
    response = client.post("/services", json=data["input"])
    assert response.status_code == data["response"]["status_code"]
    assert response.json["message"] == data["response"]["message"]


# Test the get_all_services route
def test_get_all_services(client):
    response = client.get("/services")
    assert response.status_code == 200
    assert response.json == {
        "sentiment analysis": {
            "url": "http://127.0.1/wordcount"
        },  # Since we are using a single client for all tests, the service is already registered from the previous test
    }


# Test the delete_service route
def test_delete_service(client):
    response = client.delete(
        "/services", json={"name": "sentiment analysis"}
    )  # Since we are using a single client for all tests, the service is already registered from the previous test
    assert response.status_code == 204
    response = client.delete("/services", json={"name": "sentiment analysis"})
    assert response.status_code == 404


# Test the delete_service route with invalid input
invalid_delete_input_list = [
    {
        "input": {},
        "response": {
            "status_code": 400,
            "message": "Request body must be a JSON object",
        },
    },
    {
        "input": {"name": "sentiment analysis"},
        "response": {"status_code": 404, "message": "Service does not exist"},
    },
]


@pytest.mark.parametrize("data", invalid_delete_input_list)
def test_invalid_delete_service(client, data):
    response = client.delete("/services", json=data["input"])
    assert response.status_code == data["response"]["status_code"]
    assert response.json["message"] == data["response"]["message"]