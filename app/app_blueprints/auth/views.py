from flask import render_template, redirect, url_for, request
from . import auth_bp
from .auth_repository import create_school, get_adviser

@auth_bp.route('/student-login')
def student_login():
    return render_template('auth/login/student_login.html')

@auth_bp.route('/adviser-login')
def adviser_login():
    return render_template('auth/login/adviser_login.html')


@auth_bp.route('/signup')
def choose_signup():
    return render_template('auth/signup/choose_signup.html')

@auth_bp.route('/adviser-signup', methods=['GET', 'POST'])
def adviser_signup():
    if request.method == 'GET':
        return render_template('auth/signup/adviser_signup.html')
    else:
        #check first if the user is a student or adviser, if the user is an adviser create a school data check auth_repository
        pass

@auth_bp.route('/student-signup', methods=['GET', 'POST'])
def student_signup():
    if request.method == 'GET':
        return render_template('auth/signup/student_signup.html')
    else:
        #check first if the user is a student or adviser, if the user is an adviser create a school data check auth_repository
        pass