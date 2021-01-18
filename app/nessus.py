"""Routes for Nessus API"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, logout_user, current_user, login_user
from app.modules.nessus_api import NessusAPI

# Blueprint Configuration
nessus_bp = Blueprint(
    'nessus_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@nessus_bp.route("/scan_results", methods=("GET", "POST"))
def scan_results():
    return render_template("scan_results.jinja2")
