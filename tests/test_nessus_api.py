"""Tests for the NessusAPI module."""
import pytest
from unittest.mock import Mock, patch, MagicMock


class TestNessusAPIInit:
    """Test suite for NessusAPI initialization."""
    
    def test_nessus_api_init(self):
        """Test NessusAPI can be initialized."""
        from app.modules.nessus_api import NessusAPI
        
        api = NessusAPI(
            url='https://test.nessus.local:8834',
            username='testuser',
            password='testpass'
        )
        
        assert api.url == 'https://test.nessus.local:8834'
        assert api.username == 'testuser'
        assert api.password == 'testpass'
        assert api.token is None
    
    def test_build_url(self):
        """Test URL building functionality."""
        from app.modules.nessus_api import NessusAPI
        
        api = NessusAPI(
            url='https://test.nessus.local:8834',
            username='testuser',
            password='testpass'
        )
        
        url = api.build_url('/session')
        assert url == 'https://test.nessus.local:8834/session'
        
        url = api.build_url('/folders')
        assert url == 'https://test.nessus.local:8834/folders'


class TestNessusAPIConnection:
    """Test suite for NessusAPI connection methods."""
    
    @patch('app.modules.nessus_api.requests.post')
    def test_login_success(self, mock_post):
        """Test successful login."""
        from app.modules.nessus_api import NessusAPI
        
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {'token': 'test-token-12345'}
        mock_post.return_value = mock_response
        
        api = NessusAPI(
            url='https://test.nessus.local:8834',
            username='testuser',
            password='testpass'
        )
        
        token = api.login()
        
        assert token == 'test-token-12345'
        assert api.token == 'test-token-12345'
        mock_post.assert_called_once()
    
    @patch('app.modules.nessus_api.requests.delete')
    def test_logout(self, mock_delete):
        """Test logout functionality."""
        from app.modules.nessus_api import NessusAPI
        
        mock_response = Mock()
        mock_delete.return_value = mock_response
        
        api = NessusAPI(
            url='https://test.nessus.local:8834',
            username='testuser',
            password='testpass'
        )
        api.token = 'test-token'
        
        api.logout()
        mock_delete.assert_called_once()
    
    def test_get_session_token_creates_token(self):
        """Test that get_session_token creates a new token if none exists."""
        from app.modules.nessus_api import NessusAPI
        
        api = NessusAPI(
            url='https://test.nessus.local:8834',
            username='testuser',
            password='testpass'
        )
        
        # Mock the login method
        with patch.object(api, 'login', return_value='new-token'):
            token = api.get_session_token()
            assert token == 'new-token'
    
    def test_get_session_token_returns_existing(self):
        """Test that get_session_token returns existing token."""
        from app.modules.nessus_api import NessusAPI
        
        api = NessusAPI(
            url='https://test.nessus.local:8834',
            username='testuser',
            password='testpass'
        )
        api.token = 'existing-token'
        
        token = api.get_session_token()
        assert token == 'existing-token'


class TestNessusAPIScanOperations:
    """Test suite for NessusAPI scan operations."""
    
    @patch('app.modules.nessus_api.requests.get')
    def test_folders_list(self, mock_get):
        """Test getting folder list."""
        from app.modules.nessus_api import NessusAPI
        
        mock_response = Mock()
        mock_response.text = '{"folders": [{"id": 1, "name": "Test Folder"}]}'
        mock_get.return_value = mock_response
        
        api = NessusAPI(
            url='https://test.nessus.local:8834',
            username='testuser',
            password='testpass'
        )
        api.token = 'test-token'
        
        folders = api.folders_list()
        
        assert 'folders' in folders
        assert len(folders['folders']) == 1
        assert folders['folders'][0]['name'] == 'Test Folder'
    
    @patch('app.modules.nessus_api.requests.get')
    def test_scans_list(self, mock_get):
        """Test getting scans list."""
        from app.modules.nessus_api import NessusAPI
        
        mock_response = Mock()
        mock_response.text = '{"scans": [{"id": 1, "name": "Test Scan"}]}'
        mock_get.return_value = mock_response
        
        api = NessusAPI(
            url='https://test.nessus.local:8834',
            username='testuser',
            password='testpass'
        )
        api.token = 'test-token'
        
        scans = api.scans_list()
        
        assert 'scans' in scans
        assert len(scans['scans']) == 1
        assert scans['scans'][0]['name'] == 'Test Scan'
    
    def test_update_payload_token(self):
        """Test that update_payload_token adds token to payload."""
        from app.modules.nessus_api import NessusAPI
        
        api = NessusAPI(
            url='https://test.nessus.local:8834',
            username='testuser',
            password='testpass'
        )
        api.token = 'test-token'
        
        payload = {}
        api.update_payload_token(payload)
        
        assert 'token' in payload
        assert payload['token'] == 'test-token'
