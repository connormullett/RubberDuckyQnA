
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from .config import app_config

db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app(env_name):
    app = Flask(__name__)
    app.config.from_object(app_config[env_name])
    CORS(app)
    db.init_app(app)
    bcrypt.init_app(app)

    return app
