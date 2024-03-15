import pytest
import os,pytest
import sys
from flask import Response

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
from app.entity_recoginition_services import build_response, json_validation

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


@pytest.mark.parametrize("input_text, valid_json", [
    ({"text":"This is a test"}, True),
    ({""}, False),
    ({"text":"   This is a test   "}, True),
    ({"text":None}, False),
    ({"text":123}, False),
    ({"text":[]}, False),
    ({"text":{}}, False),
    ({"text":"This is a test", "extra":"extra"}, True),
    ({"other_field":"This is a test"}, False)
])

def test_valid_json(input_text, valid_json):
    assert json_validation(input_text) == valid_json