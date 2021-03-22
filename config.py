from os import getenv
from os.path import abspath, dirname, join
from datetime import timedelta


BASEDIR = abspath(dirname(__name__))


class Config:
    SECRET_KEY = getenv('SECRET_KEY', 'supersecretkey')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=10)
    JWT_SECRET_KEY = getenv('JWT_SECRET_KEY', 'supersecretkey2')
    
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.yaml'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{join(BASEDIR, 'data-dev.sqlite')}"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{join(BASEDIR, 'data-test.sqlite')}"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{join(BASEDIR, 'data.sqlite')}"


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
