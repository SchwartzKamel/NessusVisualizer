"""Tests for ORM models."""

from datetime import datetime

from werkzeug.security import check_password_hash

from app import db
from app.models import NessusScanResults, User


def test_user_password_is_hashed(app):
    """Prove password hashing uses Werkzeug and does not store plaintext."""
    with app.app_context():
        user = User(
            username="hashuser",
            email="hash@example.com",
            created_on=datetime.now(),
            admin=False,
        )
        user.set_password("super-secret")

        assert user.password_hash != "super-secret"
        assert check_password_hash(user.password_hash, "super-secret")


def test_user_repr(app):
    """Prove the user repr stays stable for debugging/logging."""
    with app.app_context():
        user = User(
            username="repruser",
            email="repr@example.com",
            created_on=datetime.now(),
            admin=False,
        )
        assert repr(user) == "<User repruser>"


def test_scan_results_model_allows_nullable_fields(app):
    """Prove the scan results model accepts sparse vulnerability rows."""
    with app.app_context():
        result = NessusScanResults(plugin_id=12345, risk="High")
        assert result.plugin_id == 12345
        assert result.cve is None
        assert result.solution is None


def test_user_can_persist(app):
    """Prove the database schema round-trips a user record."""
    with app.app_context():
        user = User(
            username="dbuser",
            email="dbuser@example.com",
            created_on=datetime.now(),
            admin=False,
        )
        user.set_password("db-password")
        db.session.add(user)
        db.session.commit()

        stored = User.query.filter_by(username="dbuser").first()
        assert stored is not None
        assert stored.email == "dbuser@example.com"
