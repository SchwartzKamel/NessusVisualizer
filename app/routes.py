"""Route declaration."""
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
import pandas as pd
from .forms import ViewForm
from .models import db, User


# Blueprint Configuration
main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@main_bp.route("/", methods=("GET", "POST"))
@login_required
def home():
    form = ViewForm()
    # POST
    # Validate folder ID selection
    if form.validate_on_submit():
        # Get selected host
        host = request.form.get("host")

        return redirect(url_for('main_bp.scan_results', host=host))

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

    return render_template("index.jinja2", hosts=df_scan_results.values, os_cpe=df_cpe.values, form=form)


@main_bp.route("/scan_results")
@login_required
def scan_results():
    # GET
    host = request.args['host']

    sql = """SELECT * FROM scan_data WHERE host = ? """

    df_results = pd.read_sql_query(sql, con=db.engine, params=[host])

    # Define data by column number in loops (view scan_results.jinja2 for example)
    # 0 Plugin ID
    # 1 CVE
    # 2 CVSS
    # 3 Risk
    # 4 Host
    # 5 Protocol
    # 6 Port
    # 7 Name
    # 8 Synopsis
    # 9 Description
    # 10 Solution
    # 11 See Also
    # 12 Plugin Output

    return render_template("scan_results.jinja2", scan_data=df_results.to_dict('records'))


@ main_bp.route("/users")
@ login_required
def users():
    return render_template(
        'users.jinja2',
        users=User.query.all()
    )
