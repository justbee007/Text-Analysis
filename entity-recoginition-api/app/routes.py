from app import app
from flask import request

from app.services import build_response,json_validation


@app.route("/entityrecognition", methods=["POST"])
def get_entity_recognition():
    response = None
    try:    # Check if the request is in JSON format
        if request.is_json:
            json_data = request.get_json()
            # Validate the input JSON
            if not json_validation(json_data):
                response_data = {"error": "Invalid input"}
                response = build_response(400, response_data)
            else:
                # Hardcoded response for entity recognition
                entity_recognition_response = {  
                "text": "Apple Inc was founded by Steve Jobs.",
                "entities": [
                    {
                        "text": "Apple Inc",
                        "type": "ORG",
                        "start_char": 0,
                        "end_char": 8
                    },
                    {
                        "text": "Steve Jobs",
                        "type": "PERSON",
                        "start_char": 17,
                        "end_char": 26
                    }
                ]
            }
                response = build_response(200, entity_recognition_response)
        else:
            #  Return error if the request is not in JSON format
            response_data = {"error": "Invalid input"}
            response = build_response(400, response_data)
    except Exception as e:
        response = build_response(500, {"error": str(e)})
    return response    