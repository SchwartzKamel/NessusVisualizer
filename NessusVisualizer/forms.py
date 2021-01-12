"""Form class declaration."""
from flask_wtf import FlaskForm
from wtforms.fields import (
    PasswordField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length


class ContactForm(FlaskForm):
    """Contact form."""

    name = StringField("Name", [DataRequired()])
    email = StringField(
        "Email", [Email(message="Not a valid email address."), DataRequired()]
    )
    body = TextAreaField(
        "Message", [DataRequired(), Length(
            min=4, message="Your message is too short.")]
    )
    submit = SubmitField("Submit")


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
    """User Log-in Form."""
    username = StringField(
        'Username',
        validators=[
            DataRequired(), Length(
                min=4, message="Username is too short."
            )
        ]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')
