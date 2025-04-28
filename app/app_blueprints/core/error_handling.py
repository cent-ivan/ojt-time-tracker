from flask import render_template, redirect, url_for, request
from . import core_bp

@core_bp.route('/error/<string:err_type>')
def signup_error(err_type):
    match err_type:
        case 'email':
            return 'Email already taken'
        case 'school':
            return 'School already registered'
        case defaut:
            return f'Some error: {err_type}'