"""Route declaration."""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
from .models import db, User


# Blueprint Configuration
main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@main_bp.route("/", methods=("GET", "POST"))
def home():
    return render_template("index.jinja2", template="home-template")


@main_bp.route("/success", methods=("GET", "POST"))
def success():
    return render_template("success.jinja2", template="success-template")


@main_bp.route("/users", methods=("GET", "POST"))
@login_required
def users():
    return render_template(
        'users.jinja2',
        users=User.query.all()
    )
