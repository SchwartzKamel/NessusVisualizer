"""Pytest fixtures for NessusVisualizer."""

from datetime import datetime
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import create_app, db
from app.models import User


@pytest.fixture()
def app(tmp_path, monkeypatch):
    """Create a test app with an isolated SQLite database.

    This proves the app can boot without Redis and keeps every test hermetic.
    """
    db_path = tmp_path / "test.db"
    session_dir = tmp_path / "sessions"

    monkeypatch.setenv("SECRET_KEY", "test-secret-key-for-testing-only")
    monkeypatch.setenv("FLASK_APP", "wsgi.py")
    monkeypatch.setenv("SESSION_TYPE", "cachelib")
    monkeypatch.setenv("SESSION_CACHE_DIR", str(session_dir))
    monkeypatch.setenv("PROD_DATABASE_URI", f"sqlite:///{db_path}")
    monkeypatch.setenv("DEV_DATABASE_URI", f"sqlite:///{db_path}")
    monkeypatch.setenv("REDIS_URI", "redis://localhost:6379/0")
    monkeypatch.setenv("NESSUS_URL", "https://nessus.local:8834")
    monkeypatch.setenv("NESSUS_USER", "testuser")
    monkeypatch.setenv("NESSUS_PASS", "testpass")
    monkeypatch.setenv("NESSUS_VERIFY_SSL", "false")

    test_app = create_app()
    test_app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)

    with test_app.app_context():
        db.create_all()

    yield test_app

    with test_app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    """Return a Flask test client."""
    return app.test_client()


@pytest.fixture()
def seed_user(app):
    """Create a baseline user for auth and database tests."""
    with app.app_context():
        user = User(
            username="testuser",
            email="test@example.com",
            created_on=datetime.now(),
            admin=False,
        )
        user.set_password("testpassword123")
        db.session.add(user)
        db.session.commit()
        yield user
        db.session.delete(user)
        db.session.commit()
