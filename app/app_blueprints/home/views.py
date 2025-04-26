from flask import render_template,redirect,url_for

from . import home_bp


@home_bp.route('/')
def index():
    return 'Hello, World'