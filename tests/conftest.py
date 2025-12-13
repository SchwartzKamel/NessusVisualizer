"""Test configuration and fixtures for pytest."""
import os
import pytest
from app import create_app, db


@pytest.fixture(scope='function')
def app():
    """Create application for testing."""
    # Set test environment variables
    os.environ['SECRET_KEY'] = 'test-secret-key-for-testing-only'
    os.environ['FLASK_APP'] = 'wsgi.py'
    os.environ['SESSION_TYPE'] = 'filesystem'
    os.environ['PROD_DATABASE_URI'] = 'sqlite:///:memory:'
    os.environ['DEV_DATABASE_URI'] = 'sqlite:///:memory:'
    # Mock Redis URI - tests will use filesystem session
    os.environ['REDIS_URI'] = 'redis://localhost:6379'
    
    # Import and patch config before creating app
    import config
    
    # Override the Config class to not use Redis for testing
    class TestConfig(config.Config):
        """Test config."""
        SECRET_KEY = 'test-secret-key-for-testing-only'
        FLASK_ENV = 'testing'
        DEBUG = True
        TESTING = True
        SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
        SQLALCHEMY_ECHO = False
        SESSION_TYPE = 'filesystem'
        WTF_CSRF_ENABLED = False
        SERVER_NAME = 'localhost:5000'
        
        # Remove Redis dependency for testing
        SESSION_REDIS = None
    
    # Patch the config
    config.TestConfig = TestConfig
    
    # Create a custom test app factory
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_login import LoginManager
    from flask_session import Session
    
    test_app = Flask(__name__, instance_relative_config=False)
    test_app.config.from_object(TestConfig)
    
    # Initialize Plugins without Redis
    from app import db as app_db, login_manager as app_login_manager
    app_db.init_app(test_app)
    app_login_manager.init_app(test_app)
    
    # Use filesystem session for testing
    Session(test_app)
    
    with test_app.app_context():
        from app import routes, auth, nessus
        
        # Register Blueprints
        test_app.register_blueprint(routes.main_bp)
        test_app.register_blueprint(auth.auth_bp)
        test_app.register_blueprint(nessus.nessus_bp)
        
        # Create database models
        app_db.create_all()
    
    yield test_app
    
    # Cleanup
    with test_app.app_context():
        app_db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """Create a test client."""
    return app.test_client()


@pytest.fixture(scope='function')
def runner(app):
    """Create a test CLI runner."""
    return app.test_cli_runner()


@pytest.fixture(scope='function')
def init_database(app):
    """Initialize database with test data."""
    from app import db as app_db
    from app.models import User
    from datetime import datetime
    
    with app.app_context():
        # Check if user already exists
        existing_user = User.query.filter_by(username='testuser').first()
        if existing_user:
            app_db.session.delete(existing_user)
            app_db.session.commit()
        
        # Create a test user
        test_user = User(
            username='testuser',
            email='test@example.com',
            created_on=datetime.now(),
            admin=False
        )
        test_user.set_password('testpassword123')
        app_db.session.add(test_user)
        app_db.session.commit()
        
        yield app_db
        
        # Cleanup
        app_db.session.rollback()
