from datetime import datetime
from flask import render_template,redirect,url_for
from flask_login import login_required, current_user

from . import stud_dashboard_bp


@stud_dashboard_bp.route('/')
@login_required
def index():
    name = current_user.studentName
    time = datetime.now()
    hour = time.hour - 12
    minute = time.minute
    am_pm = time.strftime('%p')
    return render_template('student_dashboard.html', name=name, check_time=int(time.strftime('%H')), time=f"{hour}:{minute} {am_pm}")