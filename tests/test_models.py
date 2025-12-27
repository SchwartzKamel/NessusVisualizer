"""Tests for the data models."""
import pytest
from datetime import datetime


class TestUserModel:
    """Test suite for the User model."""
    
    def test_user_model_creation(self, app):
        """Test creating a user model instance."""
        from app.models import User
        
        with app.app_context():
            user = User(
                username='modeltest',
                email='model@test.com',
                created_on=datetime.now(),
                admin=False
            )
            
            assert user.username == 'modeltest'
            assert user.email == 'model@test.com'
            assert user.admin is False
    
    def test_user_password_set(self, app):
        """Test setting a user password."""
        from app.models import User
        
        with app.app_context():
            user = User(
                username='passtest',
                email='pass@test.com',
                created_on=datetime.now(),
                admin=False
            )
            user.set_password('securepassword123')
            
            assert user.password_hash is not None
            assert user.password_hash != 'securepassword123'
    
    def test_user_admin_flag(self, app):
        """Test admin flag on user model."""
        from app.models import User
        
        with app.app_context():
            admin_user = User(
                username='adminuser',
                email='admin@test.com',
                created_on=datetime.now(),
                admin=True
            )
            
            assert admin_user.admin is True
            
            regular_user = User(
                username='regularuser',
                email='regular@test.com',
                created_on=datetime.now(),
                admin=False
            )
            
            assert regular_user.admin is False


class TestNessusScanResultsModel:
    """Test suite for the NessusScanResults model."""
    
    def test_scan_results_model_creation(self, app):
        """Test creating a scan results model instance."""
        from app.models import NessusScanResults
        
        with app.app_context():
            result = NessusScanResults(
                plugin_id=12345,
                cve='CVE-2024-1234',
                cvss=7,
                risk='High',
                host='192.168.1.1',
                protocol='tcp',
                port=443,
                name='Test Vulnerability',
                synopsis='Test synopsis',
                description='Test description',
                solution='Apply patch',
                see_also='https://example.com',
                plugin_output='Test output'
            )
            
            assert result.plugin_id == 12345
            assert result.cve == 'CVE-2024-1234'
            assert result.risk == 'High'
            assert result.port == 443
    
    def test_scan_results_nullable_fields(self, app):
        """Test that optional fields can be null."""
        from app.models import NessusScanResults
        
        with app.app_context():
            result = NessusScanResults(
                plugin_id=99999,
                risk='Info'
            )
            
            assert result.cve is None
            assert result.cvss is None
            assert result.solution is None


class TestDatabaseOperations:
    """Test suite for database CRUD operations."""
    
    def test_add_user_to_database(self, app):
        """Test adding a user to the database."""
        from app.models import User
        from app import db
        
        with app.app_context():
            user = User(
                username='dbtest',
                email='db@test.com',
                created_on=datetime.now(),
                admin=False
            )
            user.set_password('testpass')
            
            db.session.add(user)
            db.session.commit()
            
            retrieved = User.query.filter_by(username='dbtest').first()
            assert retrieved is not None
            assert retrieved.email == 'db@test.com'
            
            # Cleanup
            db.session.delete(retrieved)
            db.session.commit()
    
    def test_query_users(self, app, init_database):
        """Test querying users from the database."""
        from app.models import User
        
        with app.app_context():
            users = User.query.all()
            assert len(users) >= 1
            
            test_user = User.query.filter_by(username='testuser').first()
            assert test_user is not None
