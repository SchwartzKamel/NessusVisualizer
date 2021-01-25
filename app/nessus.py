"""Routes for Nessus API"""
from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required
from app.modules.nessus_api import NessusAPI
from .forms import FoldersForm, ScansForm
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
    form = FoldersForm()
    # POST
    # Validate folder ID selection
    if form.validate_on_submit():
        # Get form fields
        folder_choice = request.form.get('scan_folder')
        return redirect(url_for('nessus_bp.select_scan', folder_choice=folder_choice))
    # GET
    folders = nessus.folders_list()
    # Filter out name and ID of folders, then create a dict of that
    folders = folders['folders']
    folder_id = [d['id'] for d in folders]
    folder_name = [d['name'] for d in folders]

    folder_info = {folder_id[i]: folder_name[i] for i in range(len(folder_id))}
    return render_template("select_folder.jinja2", form=form, folder_info=folder_info, template="form-template")


@nessus_bp.route("/select_scan", methods=("GET", "POST"))
@login_required
def select_scan():
    form = ScansForm()
    # POST
    # GET
    folder_choice = request.args['folder_choice']
    scans = nessus.scans_list(folder_id=folder_choice)
    scans = scans['scans']
    scan_id = [d['id'] for d in scans]
    scan_name = [d['name'] for d in scans]

    scan_info = {scan_id[i]: scan_name[i] for i in range(len(scan_id))}
    return render_template("select_scan.jinja2",  form=form, scan_info=scan_info, template="form-template")
