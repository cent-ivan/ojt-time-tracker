from flask import render_template,redirect,url_for
from flask_login import login_required, current_user

from . import stud_dashboard_bp


@stud_dashboard_bp.route('/')
@login_required
def index():
    id = current_user.studentId
    return render_template('dashboard.html', uid=id)