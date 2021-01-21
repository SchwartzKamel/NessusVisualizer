"""Routes for Nessus API"""
from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required
from app.modules.nessus_api import NessusAPI
from .forms import FoldersForm
from .models import db, NessusScanResults


# Blueprint Configuration
nessus_bp = Blueprint(
    'nessus_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

# Define variables for Nessus API
url = "https://10.0.0.137:8834"
username = "nessusadmin"
password = "admin"

# This calls the login function and passes it your credentials, no need to modify this.
nessus = NessusAPI(url=url, username=username, password=password)
token = nessus.login()


@nessus_bp.route("/select_folder", methods=("GET", "POST"))
@login_required
def select_folder():
    # POST
    form = FoldersForm()
    # GET
    folders = nessus.folders_list()
    folders = folders['folders']
    return render_template("select_folder.jinja2", form=form)
