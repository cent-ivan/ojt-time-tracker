from flask import Blueprint

public_bp = Blueprint('core', __name__, template_folder='templates')

from . import views