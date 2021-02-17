"""Routes for user authentication."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, logout_user, current_user, login_user
from werkzeug.security import check_password_hash
from datetime import datetime as dt
from .forms import SignupForm, LoginForm
from .models import db, User
from . import login_manager


# Blueprint Configuration
auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@auth_bp.route("/login", methods=("GET", "POST"))
def login():
    # Bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.user_records'))

    # POST
    form = LoginForm()
    # Validate login attempt
    if form.validate_on_submit():
        # Get Form Fields
        user = User.query.filter_by(username=form.username.data).first()
        password = request.form.get('password')
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            # Remember which user has logged in
            session["user_id"] = user.id

            # Send user back to the page they were on, or to users
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main_bp.home'))
        flash('Invalid username/password combination')
        return redirect(url_for('auth_bp.login'))
    # GET
    return render_template("login.html", form=form, template="form-template")


@auth_bp.route("/register", methods=("GET", "POST"))
def register():
    form = SignupForm()
    # POST
    if form.validate_on_submit():
        # Get Form Fields
        username = request.form.get('username')
        email = request.form.get('email')
        if username and email:
            existing_user = User.query.filter(
                User.username == username or User.email == email
            ).first()
            if existing_user:
                flash('A user already exists with that email address or username.')
            new_user = User(
                username=username,
                email=email,
                created_on=dt.now(),
                admin=False
            )
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth_bp.login'))
    # GET
    return render_template("signup.html", form=form, template="form-template")


@auth_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""

    # Forget any user_id
    session.clear()

    # Log user out and redirect to login page
    logout_user()
    return redirect(url_for('auth_bp.login'))


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login'))
