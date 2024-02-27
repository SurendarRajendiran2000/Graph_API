import os

from flask import Flask
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("FLASK_SECRET_KEY")  # Set a secret key for session management

    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
