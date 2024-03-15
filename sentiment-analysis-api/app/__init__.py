from flask import Flask

app = Flask(__name__)

from app.routes import *
from app.sentiment_analysis_services import *
