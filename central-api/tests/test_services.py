import pytest
import os,pytest
import sys
from flask import Response

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from app.services.services import build_response,json_validator


@pytest.mark.parametrize(
    "status, message, expected_response",
    [
        (200, None, b""),
        (
            200,
            {"message": "Service registered successfully"},
            b'{"message": "Service registered successfully"}',
        ),
        (
            404,
            {"message": "Service does not exist"},
            b'{"message": "Service does not exist"}',
        ),
        (201, {}, b""),
    ],
)
# Check if the build_response function returns a Response object and if the status code and mimetype are correct
def test_build_response(status, message, expected_response):
    response = build_response(status, message)
    assert isinstance(response, Response)
    assert response.status_code == status
    assert response.mimetype == "application/json"
    assert response.data == expected_response


# Invalid input and expected error
@pytest.mark.parametrize(
    "status, message",
    [
        ("Service registered successfully", None),
        (200, "Service registered successfully"),
        (None, None),
    ],
)

# Check if the build_response function raises a TypeError when the input is invalid
def test_build_response_invalid_input(status, message):
    with pytest.raises(TypeError):
        build_response(status, message)


@pytest.mark.parametrize(
    "status",
    [
        700,
        600,
        99,
        0,
        -1,
        -100,
        -600,
        -700,
    ],
)
def test_build_response_invalid_status(status):
    with pytest.raises(ValueError):
        build_response(status)




# Valid input and expected output

@pytest.mark.parametrize(
    "json_data",
    [
        ({"service": "sentiment analysis", "text": "This is a test"}),
        ({"service": "word count", "text": "This is a test"}),
        ({"service": "entity recognition", "text": "this is a test"}),
    ],
)
# Check if the json_validator function returns True when the input is valid
def test_json_validator(json_data):
    assert json_validator(json_data) == True
        
# Invalid input and expected error
@pytest.mark.parametrize(
    "json_data, expected_error",
    [
        ({"service": "sentiment analysis"}, "Missing required key: text"),
        ({"text": "Hello World"}, "Missing required key: service"),
        ({"service": "sentiment analysis", "text": 123}, "Input text must be a string"),
        ({"service": 123, "text": "Hello World"}, "Service name must be a string"),
        (123, "json_data must be a dictionary"),
        ({}, "json_data must not be empty"),

    ],
)

# Check if the json_validator function raises a ValueError when the input is invalid
def test_json_validator(json_data, expected_error):
    with pytest.raises(Exception) as e:
        json_validator(json_data)
    assert str(e.value) == expected_error
