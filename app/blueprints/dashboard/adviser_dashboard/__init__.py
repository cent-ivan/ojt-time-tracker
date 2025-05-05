from flask import Blueprint

adviser_dashboard_bp = Blueprint('adviser_home', __name__, template_folder='templates')

from . import adviser_dashboard_views
