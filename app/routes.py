"""Route declaration."""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
import pandas as pd
from .models import db, User


# Blueprint Configuration
main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@main_bp.route("/", methods=("GET", "POST"))
def home():
    # GET
    # Query the scan data
    df_scan_results = pd.read_sql(
        "SELECT DISTINCT host FROM scan_data", con=db.engine)
    return render_template("index.jinja2", template="home-template", column_names=df_scan_results.columns.values, row_data=list(df_scan_results.values.tolist()), zip=zip)


@main_bp.route("/users", methods=("GET", "POST"))
@login_required
def users():
    return render_template(
        'users.jinja2',
        users=User.query.all()
    )
