from flask import Flask
# Create a Flask app instance
app = Flask(__name__)

from app.routes import *
from app.entity_recoginition_services import *