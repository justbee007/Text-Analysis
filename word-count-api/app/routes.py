from flask import Flask, jsonify, request, Response
from app import app
from .word_count_services import calculate_word_count, json_validation
import json


@app.route("/wordcount", methods=["POST"])
def get_word_count():
    # Check if the request method is POST
    if request.method == "POST":
        # Check if the request is in JSON format
        if request.is_json:
            json_data = request.get_json()
            # Validate the input JSON
            if not json_validation(json_data):
                response_data = {"error": "Invalid input"}
                return Response(
                    json.dumps(response_data), status=400, mimetype="application/json"
                )
            else:
                # Calculate the word count
                text = json_data["text"]
                wordCount = calculate_word_count(text)
                response_data = {"wordCount": wordCount}
                return Response(
                    json.dumps(response_data), status=200, mimetype="application/json"
                )
        else:
            #  Return error if the request is not in JSON format
            response_data = {"error": "Invalid input"}
            return Response(
                json.dumps(response_data), status=400, mimetype="application/json"
            )
    else:
        # Return error if the request method is not POST
        return Response(status=405, mimetype="application/json")
