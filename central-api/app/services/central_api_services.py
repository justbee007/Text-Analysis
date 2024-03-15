import json
from flask import Response


# Function to build a response
def build_response(status:int,message:dict=None):
    '''
    Function to build a response to be returned to the client
    Args:
    status: int: HTTP status code
    message: dict: A dictionary containing the response message
    Returns:
    Response: A flask Response object
    '''
    try:
        if not isinstance(status, int):
            raise TypeError("status must be an integer")
        elif status<100 or status>599:
            raise ValueError("status must be a valid HTTP status code")
        if message:
            if not isinstance(message, dict):
                raise TypeError("message must be a dictionary")
            
            return Response(json.dumps(message), status, mimetype="application/json")
        else:
            return Response(status=status, mimetype="application/json")
    except Exception as e:
        raise e

# Function to validate JSON data
def json_validator(json_data):
    '''
    Function to validate JSON data
    Args:
    json_data: dict: A dictionary containing the JSON data to be validated
    Returns:
    bool: True if the JSON data is valid
    '''
    if not isinstance(json_data, dict):
        raise TypeError("json_data must be a dictionary")
    if not json_data:
        raise ValueError("json_data must not be empty")
    required_keys = {"service", "text"}

    for key in required_keys:
        if key not in json_data:
            raise ValueError(f"Missing required key: {key}")
    else:
        if not isinstance(json_data['service'],str):
            raise TypeError("Service name must be a string")  
        elif not isinstance(json_data['text'],str):
            raise TypeError("Input text must be a string")
        return True