from os import getenv
from os.path import abspath, dirname, join


BASEDIR = abspath(dirname(__name__))


class Config:
    SECRET_KEY = getenv('SECRET_KEY')

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
