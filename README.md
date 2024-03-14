
  

## Step-by-Step Guide to Start Apis in local environment

  

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