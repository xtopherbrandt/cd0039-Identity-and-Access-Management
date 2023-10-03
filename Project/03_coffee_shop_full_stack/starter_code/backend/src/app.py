from flask import Flask
from flask_cors import CORS

from .database.models import setup_db


app = Flask(__name__)
with app.app_context():
    setup_db(app)

CORS(app)
