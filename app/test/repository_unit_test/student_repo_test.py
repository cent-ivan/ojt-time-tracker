from flask import render_template, redirect, url_for, request, flash, make_response
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime

from . import test_bp
from app.blueprints.dashboard.student_dashboard.repositories.student_dashboard_repository import StudentDashboardRepository


@test_bp.route('/repo/student')
def repo_student_test():
    uid = current_user.studentId
    date = datetime.now().strftime('%Y-%m-%d')

    title = 'Student Repository tests'
    is_pressed = request.cookies['time_pressed']
    user = current_user.studentName
    timein_test = {'method_name':'StudentDashboardRepository.get_timein', 'data': StudentDashboardRepository.get_timein(uid, date)[0]} 
    timeout_test = {'method_name':'StudentDashboardRepository.get_timeOut', 'data': StudentDashboardRepository.get_timeOut(uid, date)} 
    return render_template(template_name_or_list='repo_unit_test.html', title=title, is_pressed=is_pressed, user=user, timein_test=timein_test, timeout_test=timeout_test)


@test_bp.app_template_filter('format_time')
def format_time(time:datetime) -> str:
    result = ""
    if time.hour > 12:
        result = f"{time.hour - 12}:{time.minute} PM"
    elif time == 12:
        result = f"{time.hour}:{time.minute} PM"
    else:
        result = f"{time.hour}:{time.minute} AM"
    
    return result