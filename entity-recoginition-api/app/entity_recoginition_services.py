from flask import Response
import json
def build_response(status:int,message:dict=None):
    '''
    Function to build the response
    :param status: The HTTP status code
    :param message: The response message
    :return: The response object
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

# Function used to validate the input JSON
def json_validation(json_data):
    '''
    Function to validate the input JSON
    :param json_data: The input JSON
    :return: True if the input JSON is valid, False otherwise'''
    if not json_data:
        return False
    if 'text' not in json_data:
        return False
    if not type(json_data['text']) is str:        
        return False
    return True    