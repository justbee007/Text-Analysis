- [Step-by-Step Guide to Start Apis in local environment](#step-guide)
- [Flask Apps and Circuit Breaker Implementation](#circuit-implementation)

## Step-by-Step Guide to Start Apis in local environment <a name="step-guide"></a>

  **Note:** Python 3.8 is required for the project as the Pybreaker library used in the project requires it.

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

python app.py &

  
  

### Repeat the same operation for entity recognition API, word count API and Sentiment Analysis.

# Now all the apis are running

  

Once all  services  are  running  as  expected  follow  the  below  steps  to

  
  
  

## 2. Service Registration

  

#### To register a new service, send a POST request to the endpoint:

  
  

```

POST http://127.0.0.1:5003/services

```

  

Include the following JSON payload in the request body:

  

```json

{

"url": "http://<service_url>",

"name": "<service_name>"

}

```

  

Replace `<service_url>` with the URL of the service and `<service_name>` with the name of the service.

  

## Get All Registered Services

  

To retrieve details of all registered services, send a GET request to the endpoint:

  

```

GET http://127.0.0.1:5009/services

```

  

The response will be a JSON object containing details of all registered services.

  

## Delete a Registered Service

  

To delete a registered service, send a POST request with the HTTP method set to DELETE to the endpoint:

  

```

POST http://127.0.0.1:5009/services

```

  

Include the following JSON payload in the request body:

  

```json

{

"name": "<service_name>"

}

```

  

Replace `<service_name>` with the name of the service you want to delete.

  

If the deletion is successful, you will receive a 204 No Content response.

# Flask Apps and Circuit Breaker Implementation <a name="circuit-implementation"></a>

I have 4 Flask apps inside a folder:

1. central-api
2. entity-recognition-api
3. sentiment-analysis-api
4. word-count-api

The central API is responsible for registering the other three services. 

## Circuit Breaker Implementation

I have implemented a circuit breaker in the inter-service communication between the central API and the other three services. 

The circuit breaker pattern is a design pattern used in modern software development to prevent cascading failures in distributed systems. It is described in detail by Martin Fowler [here](https://martinfowler.com/bliki/CircuitBreaker.html) and also another read to understand the circuit breaker pattern [here](https://microservices.io/patterns/reliability/circuit-breaker.html).

For the implementation of the circuit breaker in Python, I have used the Pybreaker library. 

### Pybreaker Library

Pybreaker is a Python implementation of the circuit breaker pattern. It provides a simple interface to use circuit breakers in Python applications. 

You can find more information about the Pybreaker library on its [PyPI page](https://pypi.org/project/pybreaker/).