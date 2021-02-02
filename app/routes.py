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
        "SELECT DISTINCT host FROM scan_data", con=db.engine
    )

    df_cpe = pd.read_sql(
        "SELECT `plugin output` FROM scan_data WHERE `plugin id`=45590", con=db.engine
    )
    df_cpe['OS'] = df_cpe['Plugin Output'].str.extract(
        r'(cpe.+)'
    )
    df_cpe = df_cpe.drop(['Plugin Output'], axis=1)

    return render_template("index.jinja2", column_names=df_scan_results.columns.values, row_data=list(df_scan_results.values.tolist()), zip=zip, os_cpe=df_cpe.values)


@main_bp.route("/users")
@login_required
def users():
    return render_template(
        'users.jinja2',
        users=User.query.all()
    )
