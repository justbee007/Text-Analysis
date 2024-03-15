from flask import Flask

app = Flask(__name__)

from app.routes import *
from app.services.central_api_services import *
