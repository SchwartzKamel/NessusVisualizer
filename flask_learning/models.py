"""Data models."""
from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash


class User(UserMixin, db.Model):
    """Data model for user accounts."""

    __tablename__ = 'users'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    username = db.Column(
        db.String(80),
        index=False,
        unique=True,
        nullable=False
    )
    email = db.Column(
        db.String(120),
        index=True,
        unique=True,
        nullable=False
    )
    password_hash = db.Column(
        db.String(200),
        index=False,
        unique=False,
        nullable=False
    )
    created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False
    )
    last_login = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    admin = db.Column(
        db.Boolean,
        index=False,
        unique=False,
        nullable=False
    )

    def set_password(self, password):
        """Create hashed password."""
        self.password_hash = generate_password_hash(
            password,
            method='sha256',
            salt_length=8
        )

    def __repr__(self):
        return '<User {}>'.format(self.username)
