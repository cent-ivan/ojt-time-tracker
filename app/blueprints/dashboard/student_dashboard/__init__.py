from flask import Blueprint

stud_dashboard_bp = Blueprint('student_home', __name__, template_folder='templates')

from . import student_dashboard_views
