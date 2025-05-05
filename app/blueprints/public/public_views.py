from flask import render_template, redirect, url_for, request
from flask_login import current_user
from . import public_bp

@public_bp.route('/')
def land_page():
    if current_user.is_authenticated:
        if current_user.userType == 'student':
            return redirect(url_for('student_home.index'))
        else:
            return redirect(url_for('adviser_home.index'))
        
    message = "This is a landing page"
    return render_template(template_name_or_list='landing_page.html', message=message)

