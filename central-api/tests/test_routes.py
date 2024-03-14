import pytest
import os,pytest
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

from app import app
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


input_json = {"name": "sentiment analysis", "url": "http://127.0.0.1:5000/wordcount"}
# @pytest.mark.parametrize(
#     "input_json, expected_response",
#     [
#         (
#             {"name": "sentiment analysis", "url": "http://127.0.0.1:5000/wordcount"}, 
#             (201, {"message": "Service registered successfully"})
#         )
#     ]
# )
# @pytest.mark.parametrize("data",input_json)
# def test_services_post(data,client):
#     print(input_json)
#     data = json.loads(input_json)
#     response = client.post("/services",json=data)
#     assert response == (201, {"message": "Service registered successfully"})



# def test_services_post(client):
#     response = client.post("/services",json=input_json)
#     assert response.status_code == 201
#     assert response.json == {"message": "Service registered successfully"}


input_json_list =[    
       { "input":{"name": "sentiment analysis", "url": "http://127.0.1/wordcount"},"response":{"status_code":201, "message": "Service registered successfully"},
        },
        { "input":{"name": "sentiment analysis", "url": "http://127.0.1/wordcount"},"response":{"status_code":409, "message": "Service already exists"},
        }
]
@pytest.mark.parametrize("data",input_json_list)
def test_register_services(client,data):
    response = client.post("/services",json=data["input"])
    assert response.status_code == data["response"]["status_code"]
    assert response.json["message"] == data["response"]["message"]

invalid_input_list  =[
    {"input":{},"response":{"status_code":400, "message": "Request body must be a JSON object"}},
    {"input":{"name": "sentiment analysis"},"response":{"status_code":400, "message": "Request body must contain name and url"}},
    {"input":{"url": "http://127.0.1/wordcount"},"response":{"status_code":400, "message": "Request body must contain name and url"}},    
]

@pytest.mark.parametrize("data",invalid_input_list)
def test_register_services_invalid_input(client,data):
    response = client.post("/services",json=data["input"])
    assert response.status_code == data["response"]["status_code"]
    assert response.json["message"] == data["response"]["message"]


def test_get_all_services(client):
    response = client.get("/services")
    assert response.status_code == 200
    assert response.json == {'sentiment analysis':{ 'url': 'http://127.0.1/wordcount'},}

def test_delete_service(client):
    response = client.delete("/services",json={"name":"sentiment analysis"})
    assert response.status_code == 204
    response = client.delete("/services",json = {"name":"sentiment analysis"})
    assert response.status_code == 404


invalid_delete_input_list =[
    {"input":{},"response":{"status_code":400, "message": "Request body must be a JSON object"}},
    {"input":{"name": "sentiment analysis"},"response":{"status_code":404, "message": "Service does not exist"}}
]
@pytest.mark.parametrize("data",invalid_delete_input_list)
def test_invalid_delete_service(client,data):
    response = client.delete("/services",json=data["input"])
    assert response.status_code == data["response"]["status_code"]
    assert response.json["message"] == data["response"]["message"]