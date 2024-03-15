from flask import Flask
# create an instance of the Flask class
app = Flask(__name__)

from app.routes import *
from app.word_count_services import *
