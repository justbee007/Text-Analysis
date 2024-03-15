from app import app
from flask import request
from app.services.service_manager import ServiceManager
from .services.central_api_services import build_response, json_validator
from pybreaker import CircuitBreakerError

# Create an instance of the ServiceManager class
service_manager = ServiceManager()

# This route returns a list of all services registered with the service manager
@app.route("/services", methods=["GET"])
def get_all_services():
    
    try:
        # Return a list of all services
        response = None

        if not service_manager.get_all_services():
            response = build_response(404, {"message": "No services registered"})
        else:
            response = build_response(200, service_manager.get_all_services())
    except Exception as e:
        response = build_response(500, {"message": "Internal server error"})
    return response


# Register a new service with the service manager
@app.route("/services", methods=["POST"])
def register_services():
    try:
        if not request.json:  # Check if the request body is a JSON object
            response = build_response(
                400, {"message": "Request body must be a JSON object"}
            )
            return response
        data = request.json
        if "name" not in data or "url" not in data:
            response = build_response(
                400, {"message": "Request body must contain name and url"}
            )
            return response
        service_name = data["name"]
        if service_name in service_manager.get_all_services():
            response = build_response(409, {"message": "Service already exists"})
        else:
            service_manager.register_service(service_name, data["url"])
            response = build_response(
                201, {"message": "Service registered successfully"}
            )
    except Exception as e:
        response = build_response(500, {"message": "Internal server error"})
    return response


# Delete a service from the service manager
@app.route("/services", methods=["DELETE"])
def delete_service():
    try:  # Delete a service
        if request.method == "DELETE":
            if not request.json:
                response = build_response(
                    400, {"message": "Request body must be a JSON object"}
                )
                return response
            elif "name" not in request.json:
                response = build_response(
                    400, {"message": "Request body must contain name"}
                )
                return response
            data = request.json
            service_name = data["name"]
            service_name = service_name.lower()
            if service_manager.service_exists(service_name):
                service_manager.delete_service(service_name)
                response = build_response(204)
            else:
                response = build_response(404, {"message": "Service does not exist"})
    except Exception as e:
        print(e)
        response = build_response(500, {"message": "Internal server error"})
    return response


# Analyze text using differnt services
@app.route("/analyze", methods=["POST"])
def analyze_text():
    response = None
    try:
        if request.method == "POST":
            if not request.json:
                response = build_response(
                    400, {"message": "Request body must be a JSON object"}
                )
                return response
            else:
                try:
                    # validate JSON data to check if it has the required keys are available
                    json_validator(request.json)
                except Exception as e:
                    response = build_response(400, {"message": str(e)})
                    return response

        data = request.json
        service_name = data["service"]
        service_name = service_name.lower()

        # Check if the service has been registered
        if service_manager.service_exists(service_name) == False:
            response = build_response(404, {"message": "Service does not exist"})

        else:
            try:  # make an API call to the service
                json_response = service_manager.call_api(service_name, data["text"])
                if json_response == {}:
                    response = build_response(500, {"message": "Internal server error"})
                else:
                    response = build_response(200, json_response)
            except CircuitBreakerError as e:
                response = build_response(
                    503, {"message": str(e)}
                )  # Service is down error is returned to showcase that the called service is down.
    except Exception as e:
        print(e)
        response = build_response(500, {"message": "Internal server error"})
    return response
