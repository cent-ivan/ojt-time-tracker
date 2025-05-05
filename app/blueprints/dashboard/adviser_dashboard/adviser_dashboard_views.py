from flask import render_template,redirect,url_for
from flask_login import login_required, current_user

from . import adviser_dashboard_bp


@adviser_dashboard_bp.route('/')
@login_required
def index():
    id = current_user.password
    return render_template('dashboard.html', uid=id)