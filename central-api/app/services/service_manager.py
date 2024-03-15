from pybreaker import CircuitBreaker, CircuitBreakerError
import json, requests


# Class to manage services
class ServiceManager:
    """
    This class is used to manage services. It provides the following functionalities:
    - Register a new service
    - Get a service
    - Check if a service exists
    - Get the URL of a service
    - Delete a service
    - Get all registered services
    - Get a circuit breaker associated with a service
    - Make an API call to a service
    - Create a circuit breaker associated with a service
    - The class uses the pybreaker library to implement the circuit breaker pattern.
    """

    def __init__(self):
        """
        The constructor initializes the following attributes:
        - registered_services: A dictionary to store the registered services
        - circuit_breakers: A dictionary to store the circuit breakers associated with the services
        """
        self.registered_services = {}
        self.circuit_breakers = {}

    # Function to create a circuit breaker associated with a service
    def create_circuit_breaker(self, service_name):
        """
        This function creates a circuit breaker associated with a service. It takes the following parameters:
        - service_name: The name of the service
        - The function creates a circuit breaker with the following parameters:
            - fail_max: The maximum number of failures before the circuit breaker opens
            - reset_timeout: The time in seconds before the circuit breaker switches from open to half-open
        """
        service_name = service_name.lower()
        self.circuit_breakers[service_name] = CircuitBreaker(
            fail_max=1, reset_timeout=10
        )

    # Function to register a new service
    def register_service(self, service_name, url):
        """
        This function registers a new service. It takes the following parameters:
        - service_name: The name of the service
        - url: The URL of the service
        - The function adds the service to the registered_services dictionary and creates a circuit breaker associated with the service.
        """
        service_name = service_name.lower()
        self.registered_services[service_name] = {"url": url}
        self.create_circuit_breaker(service_name)

    # Function to get a service
    def get_service(self, service_name):
        """
        This function returns a service. It takes the following parameters:
        - service_name: The name of the service
        - The function returns the service from the registered_services dictionary.
        """
        service_name = service_name.lower()
        return self.registered_services.get(service_name)

    # Function to check if a service exists
    def service_exists(self, service_name):
        """
        This function checks if a service exists. It takes the following parameters:
        - service_name: The name of the service
        - The function returns True if the service exists and False otherwise.
        """
        service_name = service_name.lower()
        return service_name in self.registered_services

    # Function to get the URL of a service
    def get_service_url(self, service_name):
        """
        This function returns the URL of a service. It takes the following parameters:
        - service_name: The name of the service
        - The function returns the URL of the service from the registered_services dictionary.
        """
        service_name = service_name.lower()
        return self.registered_services[service_name]["url"]

    # Function to delete a service
    def delete_service(self, service_name):
        """
        This function deletes a service. It takes the following parameters:
        - service_name: The name of the service
        - The function removes the service from the registered_services dictionary and the circuit breaker associated with the service.
        """
        service_name = service_name.lower()
        del self.registered_services[service_name]
        del self.circuit_breakers[service_name]

    # Function to get all registered services
    def get_all_services(self):
        """
        This function returns all registered services. It takes no parameters.
        """
        return self.registered_services

    # Function to get a circuit breaker associated with a service
    def get_circuit_breaker(self, service_name):
        """
        This function returns a circuit breaker associated with a service. It takes the following parameters:
        - service_name: The name of the service
        """
        return self.circuit_breakers[service_name]

    # Function to make an API call to a service
    def call_api(self, service_name, text):
        """
        This function makes an API call to a service. It takes the following parameters:
        - service_name: The name of the service
        - text: The text to send to the service
        - The function makes an API call to the service using the requests library and returns the results.
        """
        circuit_breaker_decorator = self.get_circuit_breaker(service_name)
        # The _api_call function is defined within the call_api function.
        # @self.circuit_breakers[service_name]  
        # This decorator uses the circuit breaker behavior to handle the service being down.
        @circuit_breaker_decorator
        def _api_call(service_name, text):
            """
            This function makes an API call to a service. It takes the following parameters:
            - service_name: The name of the service
            - text: The text to send to the service"""
            service_name = service_name.lower()
            url = self.registered_services[service_name]["url"]
            json_data = json.dumps({"text": text})
            request_body_json = json.loads(json_data)
            results = requests.post(url, json=request_body_json)
            results.raise_for_status()
            return results.json()

        try:
            return _api_call(service_name, text)
        except CircuitBreakerError as e:
            print("service is down try after few minutes")
            raise e  # This raise is purposefully not handled so that the error can be caught by the caller of the call_api function which is **analyze_text** in routes.py file to show the circuit breaker inter service communication pattern
