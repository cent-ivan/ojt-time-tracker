from flask import Blueprint

test_bp = Blueprint('test', __name__, template_folder='templates')

from . import student_repo_test