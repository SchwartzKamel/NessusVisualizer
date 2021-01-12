"""App configuration."""
from os import environ, path
from dotenv import load_dotenv
import redis

# Load variables from .env
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    """Base config vars from .env file."""
    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_APP = environ.get("FLASK_APP")
    SERVER_NAME = environ.get("SERVER_NAME")
    #SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Static Assets
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    # Flask-Session
    SESSION_TYPE = environ.get('SESSION_TYPE')
    SESSION_REDIS = redis.from_url(environ.get('REDIS_URI'))


class ProdConfig(Config):
    """Prod config"""
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    #DATABASE_URI = environ.get('PROD_DATABASE_URI')


class DevConfig(Config):
    """Dev config"""
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = environ.get('DEV_DATABASE_URI')
    SQLALCHEMY_ECHO = True
    TEMPLATES_AUTO_RELOAD = True
