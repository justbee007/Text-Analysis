from unittest.mock import MagicMock, patch
import os, pytest,requests
import sys
from flask import Response
import requests_mock
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
from app.services.service_manager import ServiceManager
from requests.exceptions import RequestException
from pybreaker import CircuitBreakerError


@pytest.fixture
def service_manager():
    return ServiceManager()


# Test the create_circuit_breaker function
def test_create_circuit_breaker(service_manager):
    service_manager.create_circuit_breaker("test")
    assert "test" in service_manager.circuit_breakers


# Test the register_service function
def test_register_service(service_manager):
    service_manager.register_service("test", "http://test.com")
    assert "test" in service_manager.registered_services
    assert "test" in service_manager.circuit_breakers


# Test the get_service function
def test_get_service(service_manager):
    service_manager.register_service("test", "http://test.com")
    assert service_manager.get_service("test") == {"url": "http://test.com"}


# Test the service_exists function
def test_service_exists(service_manager):
    service_manager.register_service("test", "http://test.com")
    assert service_manager.service_exists("test") == True
    assert service_manager.service_exists("test2") == False


# Test the get_service_url function
def test_get_service_url(service_manager):
    service_manager.register_service("test", "http://test.com")
    assert service_manager.get_service_url("test") == "http://test.com"

# Test the delete_service function
def test_delete_service(service_manager):
    service_manager.register_service("test", "http://test.com")
    service_manager.delete_service("test")
    assert "test" not in service_manager.registered_services
    assert "test" not in service_manager.circuit_breakers

# Test the get_all_services function
def test_get_all_services(service_manager):
    service_manager.register_service("test", "http://test.com")
    service_manager.register_service("test2", "http://test2.com")
    print(service_manager.get_all_services())
    assert service_manager.get_all_services() ==  {
        "test": {"url": "http://test.com"},
        "test2": {"url": "http://test2.com"}
    }

# Test the get_circuit_breaker function
def test_get_circuit_breaker(service_manager):
    service_manager.register_service("test", "http://test.com")
    assert (
        service_manager.get_circuit_breaker("test")
        == service_manager.circuit_breakers["test"]
    )

# Test the call_api function
def test_api_call_success(service_manager,mocker):
    mock_response = mocker.Mock() # create a mock object
    mock_response.json.return_value ={"status": 200, "message": "success"} # set the return value of the json method
    mock_response.raise_for_status.return_value = 200 # set the return value of the raise_for_status method
    mocker.patch("app.service_manager.service_manager.requests.post" , return_value = mock_response)
    service_manager.register_service("test", "http://test.com")
    response = service_manager.call_api("test", "This is a test")
    assert response == mock_response.json.return_value


# Test for circuit breaker opening
def test_call_api_circuit_breaker_open(service_manager, mocker):
    mocker.patch("app.service_manager.service_manager.requests.post", side_effect=CircuitBreakerError())
    service_manager.register_service("test", "http://test.com")
    # Check if circuit break error is raised when the service is down
    with pytest.raises(CircuitBreakerError):
        service_manager.call_api("test", "This is a test")