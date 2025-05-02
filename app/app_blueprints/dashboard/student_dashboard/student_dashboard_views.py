from flask import render_template,redirect,url_for

from . import stud_dashboard_bp


@stud_dashboard_bp.route('/')
def index():
    return 'Hello, World'