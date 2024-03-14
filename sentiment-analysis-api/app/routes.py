from flask import Flask, jsonify, request, Response
from app import app
from .services import sentiment_analysis, json_validation, check_input_type
import json
# Route to check sentiment of the input text
@app.route("/analyzesentiment", methods=["POST"])
def get_sentiment():
    if(request.method == "POST"):
        if request.is_json == True:
            json_data = request.json
            if not json_validation(json_data):
                return Response(json.dumps({"error": "Invalid input"}), status=400, mimetype='application/json')
            text_data = request.json["text"]
            if not check_input_type(text_data):
                return Response(json.dumps({"error": "Invalid input"}), status=400, mimetype='application/json')
            sentiment = sentiment_analysis(text_data)
            return Response(json.dumps({"result": sentiment}), status=200, mimetype='application/json')
        else:
            return Response(json.dumps({"error": "Invalid input"}), status=400, mimetype='application/json')
    else:
        return Response(status=405, mimetype='application/json')