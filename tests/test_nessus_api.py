"""Tests for the Nessus API client."""

from unittest.mock import Mock, patch

from app.modules.nessus_api import NessusAPI


def test_nessus_api_builds_urls():
    """Prove URL joining works for Nessus resources."""
    api = NessusAPI(
        url="https://nessus.local:8834",
        username="tester",
        password="secret",
    )

    assert api.build_url("/session") == "https://nessus.local:8834/session"


@patch("app.modules.nessus_api.requests.post")
def test_login_success(mock_post):
    """Prove login reads the token from the Nessus session response."""
    mock_response = Mock()
    mock_response.json.return_value = {"token": "token-123"}
    mock_post.return_value = mock_response

    api = NessusAPI(
        url="https://nessus.local:8834",
        username="tester",
        password="secret",
    )

    token = api.login()
    assert token == "token-123"
    assert api.token == "token-123"


@patch("app.modules.nessus_api.requests.get")
def test_folders_list_returns_json(mock_get):
    """Prove GET responses are decoded for folder lookups."""
    mock_response = Mock()
    mock_response.text = '{"folders":[{"id":1,"name":"General"}]}'
    mock_get.return_value = mock_response

    api = NessusAPI(
        url="https://nessus.local:8834",
        username="tester",
        password="secret",
    )
    api.token = "token-123"

    folders = api.folders_list()
    assert folders["folders"][0]["name"] == "General"


def test_update_payload_token_injects_current_token():
    """Prove request payloads always inherit the active auth token."""
    api = NessusAPI(
        url="https://nessus.local:8834",
        username="tester",
        password="secret",
    )
    api.token = "token-123"

    payload = {}
    api.update_payload_token(payload)
    assert payload == {"token": "token-123"}
