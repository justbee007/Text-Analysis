import pytest
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
from app.services import calculate_word_count, json_validation


# Test case for valid JSON input
@pytest.mark.parametrize("input_text, expected_count", [
    ("This is a test", 4),
    ("", 0),
    ("   This is a test   ", 4),
    ("This    is    a    test", 4),
])
# Test case for word count
def test_calculate_word_count(input_text, expected_count):
    assert calculate_word_count(input_text) == expected_count


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