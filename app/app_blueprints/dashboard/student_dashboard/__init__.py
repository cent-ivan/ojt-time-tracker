from flask import Blueprint

stud_dashboard_bp = Blueprint('home', __name__, template_folder='templates')

from . import views
