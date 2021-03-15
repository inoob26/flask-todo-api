from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
ma = Marshmallow()
jwtm = JWTManager()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    ma.init_app(app)
    jwtm.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api/v1")

    return app
