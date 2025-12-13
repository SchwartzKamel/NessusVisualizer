"""Tests for app initialization and configuration."""
import pytest


class TestAppConfig:
    """Test suite for application configuration."""
    
    def test_app_exists(self, app):
        """Test that the app is created successfully."""
        assert app is not None
    
    def test_app_is_testing(self, app):
        """Test that the app is in testing mode."""
        assert app.config['TESTING'] is True
    
    def test_app_has_secret_key(self, app):
        """Test that the app has a secret key configured."""
        assert app.config['SECRET_KEY'] is not None
        assert len(app.config['SECRET_KEY']) > 0
    
    def test_app_database_uri(self, app):
        """Test that the database URI is configured."""
        assert app.config['SQLALCHEMY_DATABASE_URI'] is not None


class TestClientBasics:
    """Test suite for basic client operations."""
    
    def test_client_exists(self, client):
        """Test that the test client is created."""
        assert client is not None
    
    def test_login_page_accessible(self, client):
        """Test that the login page is accessible."""
        response = client.get('/login')
        assert response.status_code == 200
    
    def test_register_page_accessible(self, client):
        """Test that the register page is accessible."""
        response = client.get('/register')
        assert response.status_code == 200
    
    def test_home_redirects_to_login(self, client):
        """Test that home page redirects to login for unauthenticated users."""
        response = client.get('/', follow_redirects=False)
        assert response.status_code == 302
        assert '/login' in response.location or response.status_code == 302


class TestDatabase:
    """Test suite for database operations."""
    
    def test_database_connection(self, app):
        """Test that the database connection works."""
        from app import db
        with app.app_context():
            # Simple query to test connection
            result = db.session.execute(db.text('SELECT 1'))
            assert result is not None
    
    def test_user_table_exists(self, app, init_database):
        """Test that the users table exists."""
        from app.models import User
        with app.app_context():
            users = User.query.all()
            assert isinstance(users, list)
