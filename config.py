"""App configuration."""
from os import environ, path
from dotenv import load_dotenv

# Load variables from .env
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


def get_redis_connection():
    """Get Redis connection with fallback handling."""
    redis_uri = environ.get('REDIS_URI')
    if redis_uri:
        try:
            import redis
            return redis.from_url(redis_uri)
        except (redis.ConnectionError, redis.TimeoutError, ImportError):
            return None
    return None


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
    SESSION_TYPE = environ.get('SESSION_TYPE', 'filesystem')
    SESSION_REDIS = get_redis_connection()


class ProdConfig(Config):
    """Prod config"""
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = environ.get('PROD_DATABASE_URI')
    SQLALCHEMY_ECHO = True


class DevConfig(Config):
    """Dev config"""
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = environ.get('DEV_DATABASE_URI')
    SQLALCHEMY_ECHO = True
    TEMPLATES_AUTO_RELOAD = True


class DockerConfig(Config):
    """Docker config - uses Redis from docker-compose network."""
    FLASK_ENV = environ.get('FLASK_ENV', 'production')
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = environ.get('PROD_DATABASE_URI', 'sqlite:////app/nessus_visualizer.db')
    SQLALCHEMY_ECHO = False

    # Redis is required in Docker environment
    SESSION_TYPE = 'redis'
