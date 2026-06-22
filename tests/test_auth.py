"""Tests for authentication behavior."""

from app.models import User


def test_login_with_valid_credentials_redirects(client, seed_user):
    """Prove a seeded user can log in and reach the home redirect."""
    response = client.post(
        "/login",
        data={"username": "testuser", "password": "testpassword123"},
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")


def test_login_rejects_invalid_password(client, seed_user):
    """Prove invalid credentials stay on the login flow."""
    response = client.post(
        "/login",
        data={"username": "testuser", "password": "wrong-password"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Invalid username/password combination" in response.data


def test_register_rejects_existing_user(client, app, seed_user):
    """Prove the duplicate-user guard stops a second insert."""
    with app.app_context():
        before = User.query.count()

    response = client.post(
        "/register",
        data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "newpassword123",
            "confirmPassword": "newpassword123",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"A user already exists with that email address or username." in response.data

    with app.app_context():
        assert User.query.count() == before
