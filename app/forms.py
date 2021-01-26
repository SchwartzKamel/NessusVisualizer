"""Form class declaration."""
from flask_wtf import FlaskForm
from wtforms.fields import (
    PasswordField,
    StringField,
    SubmitField,
    IntegerField
)
from wtforms.validators import DataRequired, Email, EqualTo, Length


class SignupForm(FlaskForm):
    """Sign up for a user account."""

    username = StringField(
        "Username", [DataRequired(), Length(
            min=4, message="Username is too short."
        )]
    )
    email = StringField(
        "Email", [Email(message="Not a valid email address."), DataRequired()]
    )
    password = PasswordField(
        "Password",
        [
            DataRequired(message="Please enter a password."), EqualTo(
                'confirmPassword', message="Passwords must match")
        ],
    )
    confirmPassword = PasswordField(
        "Repeat Password"
    )
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    """Log in registered users."""
    username = StringField(
        'Username',
        validators=[
            DataRequired(), Length(
                min=4, message="Username is too short."
            )
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ]
    )
    submit = SubmitField('Log In')


class FoldersForm(FlaskForm):
    """Scan Folder Selection Form"""
    scan_folder = IntegerField(
        'ID',
        validators=[
            DataRequired()
        ]
    )
    select = SubmitField('Select')


class ScansForm(FlaskForm):
    """Scan Selection Form"""
    scan = IntegerField(
        'ID',
        validators=[
            DataRequired()
        ]
    )
    select = SubmitField('Select')
