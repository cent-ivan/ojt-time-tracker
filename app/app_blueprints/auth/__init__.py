#initialize the blueprint
from flask import Blueprint

auth_bp = Blueprint('auth', __name__, template_folder='templates')

from app.app_blueprints.auth import auth_views