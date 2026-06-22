"""App configuration."""
from os import environ, path
from dotenv import load_dotenv
import redis
from cachelib.file import FileSystemCache

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
    SESSION_TYPE = environ.get('SESSION_TYPE', 'cachelib')
    REDIS_URI = environ.get('REDIS_URI')
    SESSION_CACHE_DIR = environ.get(
        'SESSION_CACHE_DIR',
        environ.get('SESSION_FILE_DIR', '/tmp/flask_session')
    )
    SESSION_CACHELIB = (
        FileSystemCache(cache_dir=SESSION_CACHE_DIR)
        if SESSION_TYPE in {'filesystem', 'cachelib'}
        else None
    )
    SESSION_REDIS = redis.from_url(REDIS_URI) if REDIS_URI else None


class ProdConfig(Config):
    """Prod config"""
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = environ.get(
        'PROD_DATABASE_URI',
        'sqlite:///' + path.join(basedir, 'nessus_visualizer.db')
    )
    SQLALCHEMY_ECHO = True


class DevConfig(Config):
    """Dev config"""
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = environ.get(
        'DEV_DATABASE_URI',
        'sqlite:///' + path.join(basedir, 'nessus_visualizer.db')
    )
    SQLALCHEMY_ECHO = True
    TEMPLATES_AUTO_RELOAD = True
