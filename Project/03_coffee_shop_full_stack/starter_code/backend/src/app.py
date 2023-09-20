from flask import Flask
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth


app = Flask(__name__)
with app.app_context():
    setup_db(app)

CORS(app)
