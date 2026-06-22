"""Tests for app startup and basic routing."""


def test_app_boots_with_test_config(app):
    """Prove the factory can build a test app without external services."""
    assert app.config["TESTING"] is True
    assert app.config["SECRET_KEY"]
    assert app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite:///")


def test_login_page_is_available(client):
    """Prove the login route renders for anonymous users."""
    response = client.get("/login")
    assert response.status_code == 200


def test_home_redirects_anonymous_users(client):
    """Prove the landing page still requires authentication."""
    response = client.get("/")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]
