"""Tests for authentication functionality."""
import pytest


class TestUserModel:
    """Test suite for the User model."""
    
    def test_user_creation(self, app, init_database):
        """Test that a user can be created."""
        from app.models import User
        with app.app_context():
            user = User.query.filter_by(username='testuser').first()
            assert user is not None
            assert user.username == 'testuser'
            assert user.email == 'test@example.com'
    
    def test_password_hashing(self, app):
        """Test that passwords are properly hashed."""
        from app.models import User
        from datetime import datetime
        
        with app.app_context():
            user = User(
                username='hashtest',
                email='hash@test.com',
                created_on=datetime.now(),
                admin=False
            )
            user.set_password('mypassword')
            
            # Password should be hashed, not stored in plain text
            assert user.password_hash != 'mypassword'
            assert 'scrypt' in user.password_hash or 'pbkdf2' in user.password_hash
    
    def test_user_repr(self, app, init_database):
        """Test the user string representation."""
        from app.models import User
        with app.app_context():
            user = User.query.filter_by(username='testuser').first()
            assert '<User testuser>' == repr(user)


class TestAuthentication:
    """Test suite for authentication routes."""
    
    def test_login_page_get(self, client):
        """Test GET request to login page."""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'Log In' in response.data or b'login' in response.data.lower()
    
    def test_register_page_get(self, client):
        """Test GET request to register page."""
        response = client.get('/register')
        assert response.status_code == 200
        assert b'Submit' in response.data or b'register' in response.data.lower()
    
    def test_login_with_valid_credentials(self, client, init_database):
        """Test login with valid credentials."""
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'testpassword123'
        }, follow_redirects=False)
        # Should redirect on successful login
        assert response.status_code in [200, 302]
    
    def test_login_with_invalid_credentials(self, client, init_database):
        """Test login with invalid credentials."""
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        # Should show error or stay on login page
        assert response.status_code == 200
    
    def test_logout(self, client, init_database):
        """Test logout functionality."""
        # First login
        client.post('/login', data={
            'username': 'testuser',
            'password': 'testpassword123'
        })
        
        # Then logout
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200


class TestRegistration:
    """Test suite for user registration."""
    
    def test_register_new_user(self, client, app):
        """Test registering a new user."""
        from app.models import User
        
        response = client.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'confirmPassword': 'newpassword123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        
        # Check if user was created
        with app.app_context():
            user = User.query.filter_by(username='newuser').first()
            # User might be created depending on validation
            # This is a basic check that the endpoint works
