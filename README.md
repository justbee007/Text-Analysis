- [Step-by-Step Guide to Start Apis in local environment](#step-guide)
- [Flask apis and Circuit Breaker Implementation](#circuit-implementation)
- [Step by step guide to see circuit breaker in action](#circuit-breaker-in-action) 
- [Documentation of all Apis used in this project](https://documenter.getpostman.com/view/32183113/2sA2xmUqFn)
- [Running Unit Tests inside each api using Pytest](#tests-using-pytest)
- [Running the APIS using Docker](#run-the-apis-using-docker-)
## Step-by-Step Guide to Start Apis in local environment <a name="step-guide"></a>

  **Note:** Python 3.8 is required for the project as the Pybreaker library used in the project requires it.
  **Note:** If Python 3.8 is unavailable in your system considering running the app using Docker. Here is the guide to run the application using Docker [Guide to start Apis using Docker](#run-the-apis-using-docker-)

### 1. Clone the Repository:

  

```bash

# Clone the repository

git clone  https://github.com/justbee007/Text-Analysis.git

  

# Navigate to central-api directory

cd Text-Analysis/central-api

  

# Create a virtual environment

python3.8 -m  venv  env

  

# Activate the virtual environment

source env/bin/activate  # for Unix/Mac

# or

.\env\Scripts\activate # for Windows

  

# Install requirements

pip install  -r  requirements.txt

  

# Start the central-api app

python app.py

  
  

### Repeat the same operation for entity recognition API, word count API and Sentiment Analysis.

# Now all the apis are running

  
```
Once all  services  are  running the end points will be available at the following URLS
1. **Entity Recognition API**
   - Localhost URL: [http://127.0.0.1:5009/entityrecognition](http://127.0.0.1:5009/entityrecognition)

2. **Sentiment Analysis API**
   - Localhost URL: [http://127.0.0.1:5010/wordcount](http://127.0.0.1:5010/wordcount)

3. **Word Count API**
   - Localhost URL: [http://127.0.0.1:5005/wordcount](http://127.0.0.1:5009/entityrecognition)
```
## 2. Service Registration 

To register a service
```
POST [http://127.0.0.1:5008/services]
```
Include the following JSON payload in the request body:
```

{

"url": "http://<service_url>",

"name": "<service_name>"

}

```

Replace `<service_url>` with the URL of the service and `<service_name>` with the name of the service.

  

## 3. Get All Registered Services

  

To retrieve details of all registered services, send a GET request to the endpoint:

  

```

GET [http://127.0.0.1:5008/services]

```

  

The response will be a JSON object containing details of all registered services.

  

## 4. Delete a Registered Service

  

To delete a registered service, send a POST request with the HTTP method set to DELETE to the endpoint:

  

```

DELETE [http://127.0.0.1:5008/services]

```

  

Include the following JSON payload in the request body:

  

```

{

"name": "<service_name>"

}

```  

Replace `<service_name>` with the name of the service you want to delete.

  
If the deletion is successful, you will receive a 204 No Content response.

## 5. Get Text Analysis  

To retrieve a text analysis response, send a post request along with the text analysis service name along with the text that needs to be analysed

```

POST [http://127.0.0.1:5008/analyze]

```
Include the following JSON payload in the request body:

```
{
"service": "<service_name>",
"text": "Apple was founded by Steve jobs"
}

```
Replace `<service_name>` with the name of the service you want to delete.

The response will be a JSON object containing the response of the the text analysis service that was called.
```
# Flask Apis and Circuit Breaker Implementation <a name="circuit-implementation"></a>

I have 4 Flask apps inside a folder:

1. [central-api](/central-api)
2. [entity-recognition-api](/entity-recoginition-api)
3. [sentiment-analysis-api](/sentiment-analysis-api)
4. [word-count-api](/wordcount-api)

The central API is responsible for registering the other three services along with communicating with the regsitered services.

## Circuit Breaker Implementation

I have implemented a circuit breaker in the inter-service communication between the central API and the other three services. 

The circuit breaker pattern is a design pattern used in modern software development to prevent cascading failures in distributed systems. It is described in detail by Martin Fowler [here](https://martinfowler.com/bliki/CircuitBreaker.html) and also another read to understand the circuit breaker pattern [here](https://microservices.io/patterns/reliability/circuit-breaker.html).

For the implementation of the circuit breaker in Python, I have used the Pybreaker library. 

### Pybreaker Library

Pybreaker is a Python implementation of the circuit breaker pattern. It provides a simple interface to use circuit breakers in Python applications. 

You can find more information about the Pybreaker library on its [PyPI page](https://pypi.org/project/pybreaker/).


# Simulate Circuit Breaker with the Central API <a name="circuit-breaker-in-action"></a>

To see the circuit breaker pattern in action with the Central API, follow these steps:

1. **Register a Text Analysis Service**: Use the Central API `/services`to register one of the available text analysis services (e.g., entity-recognition-api, sentiment-analysis-api, word-count-api).

2. **Stop the Registered Service**: Manually stop the registered service by shutting down the corresponding service. For example, if you registered the `entity-recognition-api`, stop the server running that service.

3. **Communicate with the Service via Central API**: Attempt to communicate with the stopped service using the `/analyze` route of the Central API. Send a sample text to analyze.

4. **Observe Circuit Breaker Behavior**: Upon attempting to call the stopped service, the Central API will respond with a status 503 indicating that the service is unavailable.  The first time the api is hit
{
"message": "Failures threshold reached, circuit breaker opened"
}  
When you try to hit the api again you get a response of 503 with the following message
{
"message": "Timeout not elapsed yet, circuit breaker still open"
}
Even if the service in this example `entity-recognition-api` is started again the circuit breaker prevents the central-api from accessing the `entity-recognition-api`  for a period of 10 seconds after which when you try to access the api the circuit breaker tries to make an api call to the `entity-recognition-api`. 

We have individual circuit breakers managing each of the service and the above described behavior can be replicated for all three text analysis services at once.
This behavior demonstrates the circuit breaker pattern in action, as the Central API detects the service failure and gracefully handles the situation by preventing further API calls to the unavailable service. 

By following these steps, you can observe how the circuit breaker pattern effectively manages service failures and ensures the resilience of the Central API.

# Service Manager Class

The [Service Manager class](/central-api/app/services/service_manager.py)  is a Python class in the [Central Api](/central-api)
designed to manage services within a microservices architecture. It provides functionalities for registering, accessing, and interacting with services, as well as implementing the circuit breaker pattern for handling service failures.

## Functionality

The `ServiceManager` class offers the following functionalities:

- **Register a New Service**: Register a new service with a unique service name and its corresponding URL.
- **Get a Service**: Retrieve information about a registered service based on its service name.
- **Check if a Service Exists**: Check whether a service with a specific service name is registered.
- **Get the URL of a Service**: Retrieve the URL associated with a registered service.
- **Delete a Service**: Remove a registered service from the service registry.
- **Get All Registered Services**: Retrieve a dictionary containing information about all registered services.
- **Get a Circuit Breaker**: Obtain the circuit breaker associated with a specific service for implementing fault tolerance.
- **Make an API Call to a Service**: Execute an API call to a registered service, handling failures gracefully using the circuit breaker pattern.

## Circuit Breaker Pattern

The `ServiceManager` class employs the `pybreaker` library to implement the circuit breaker pattern, ensuring robust handling of service failures.  We are creating multiple `circuit breaker` objects to keep track of various service availability. When calling APIs, the circuit breaker monitors service health. Upon surpassing failure thresholds which we have set to 1 it temporarily halts further API requests. After a 10-second timeout, it shifts to a half-open state, permitting a few test calls. Success restores normal operation; however, persistent failures keep the circuit breaker open, safeguarding against service degradation.

## Usage

To use the `ServiceManager` class in your Python application, follow these steps:

1. Create an instance of the `ServiceManager` class.
2. Register services using the `register_service` method, providing the service name and URL.
3. Access services and interact with them using the provided methods.
4. Handle service failures gracefully using the circuit breaker pattern implemented in the `call_api` method.

By leveraging the `ServiceManager` class, you can effectively manage services within your microservices architecture and ensure fault tolerance and reliability in your distributed systems.

## Running Tests using Pytest<a name="tests-using-pytest"></a>

To run the tests for all Apis routes and services, follow these steps:

1. **Clone the Repository**: If you haven't already, clone the repository containing the project code.

2. **Install Dependencies**: Navigate to the project root directory and install the necessary dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up Environment**: Ensure that you have set up a virtual environment for the project. You can create and activate a virtual environment using the following commands:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

4. **Run the Tests**: Once the environment is activated, navigate to the `tests` folder and run the tests using pytest:

    ```bash
    cd /path/to/<api-folder>/tests
    pytest -vv
    ```

    This command will execute all the tests in the `tests` folder and provide verbose output (`-vv`) for better visibility of the test results.

5. **View Test Results**: After running the tests, pytest will display the results in the terminal. You'll see information about which tests passed and which ones failed, along with any relevant error messages.


## Run the Apis using Docker <a name="Running Using Docker"></a>
Clone the repository. Locate the [docker-compose file](/central-api/docker-compose.yaml) file in the folder.
Before starting the services, it's important to ensure that the required ports are available and not being used by any other processes. Look at a code snippet from the docker- compose file below. 
```bash
sentiment-analysis-api:
image: justbee007/sentiment-analysis-api:latest
ports:
- "5001:5005" Ensure that Port 5001 is available on your machine. Else change it to another port 
networks:
- custom-network
depends_on:
- central-api
```
- Similarly check whether all the ports in the docker-compose file are available
- Make sure you have [Docker](https://www.docker.com/products/docker-desktop/) is installed on your system.

***How to Start up the docker container*** 
1.  Open your terminal or command prompt.
2.  Navigate to the directory where your [docker-compose file](/central-api/docker-compose.yaml) file is located.
3.  Run the following command to start all services defined in the `docker-compose.yaml` file:
	```
	docker-compose up -d
	```
The Api End Points to access the following services through docker is 

1. entity-recognition-api - http://entity-recognition-api:5009/entityrecognition
2. sentiment-analysis-api - http://word-count-api:5010/wordcount
3. word-count-api - http://entity-recognition-api:5009/entityrecognition

###  Service Registration
To register a service use the below end point through a tool like Postman
POST [http://127.0.0.1:5008/services]

```
Include the following JSON payload in the request body:
JSON
{

"url": "http://<service_url>",

"name": "<service_name>"

}
Example:
JSON
{

"url": "http://entity-recognition-api:5009/entityrecognition",

"name": "entity recognition"

}
```

Replace `<url>` with the URL of the service and `<service_name>` with the name of the service.


To see **Circuit Breaker pattern** in action run a command 
```bash
Run the command ``` docker ps  ```

The above command lists a list of all containers. Locate the container ID and run the command 
``` docker stop <container_id> ``` 
- Now when trying to access the respective Api text analysis service through central service  you get an error along with HTTP STATUS CODE 503
Service Unavailable 
{
"message": "Failures threshold reached, circuit breaker opened"
}  
When you try to hit the api again you get a response of 503 with the following message
{
"message": "Timeout not elapsed yet, circuit breaker still open"
}
```
