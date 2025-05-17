from flask import render_template, redirect, url_for, request, flash, make_response
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime

from . import auth_bp
#always import repository in view if any
from .repositories.signup_repository import SignUpRepository
from .repositories.login_repository import LoginRepository
from app.blueprints.dashboard.student_dashboard.repositories.student_dashboard_repository import StudentDashboardRepository
from ...extensions import bcrypt
from .utils.validators import Validators
from .utils.generators import Generators

#use JWT
'''
to avoid circular imports: Make sure that two or more modules don’t rely on importing each other at the top level during initial loading.
'''


#--LOG IN---------------------------------------------------------------
@auth_bp.route('/adviser-login', methods=['GET', 'POST'])
def adviser_login():
    if request.method == 'GET':
        return render_template('auth/login/adviser_login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('pass')

        if not Validators.is_valid_email(email):
            flash('Invalid Email. Please put a valid email')
            return redirect(url_for('auth.adviser_login'))
        
        if not Validators.is_password_correct_length(password):
            flash('Password must have a lenght of 6 or more')
            return redirect(url_for('auth.adviser_login'))
        
        #CHECK
        try:
            user = LoginRepository.check_adviser(email)
            if not bcrypt.check_password_hash(user.password, password):
                flash('Incorrect password. Check your credentials')
                return redirect(url_for('auth.adviser_login'))
            
            if user == 0:
                flash('User do not exist. Check your credentials')
                return redirect(url_for('auth.adviser_login'))
                
            
            #logs in user
            login_user(user)
            return redirect(url_for('adviser_home.index'))
        except AttributeError:
            flash('User do not exist. Check your credentials or register.')
            return redirect(url_for('auth.adviser_login'))
            

@auth_bp.route('/student-login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'GET':
        return render_template('auth/login/student_login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('pass')

        if not Validators.is_valid_email(email):
            flash('Invalid Email. Please put a valid email')
            return redirect(url_for('auth.student_login'))
        
        if not Validators.is_password_correct_length(password):
            flash('Password must have a lenght of 6 or more')
            return redirect(url_for('auth.student_login'))
        
        #CHECK
        user = LoginRepository.check_student(email)
        if user == 0:
            flash('User do not exist. Check your credentials')
            return redirect(url_for('auth.student_login'))
                
        if not bcrypt.check_password_hash(user.password, password):
            flash('Incorrect password. Check your credentials')
            return redirect(url_for('auth.student_login'))
        
        #logs in user
        login_user(user)
        return redirect(url_for('student_home.index'))


@auth_bp.route('/logout/<string:user_type>/<string:uid>')
def logout(user_type, uid):
    logout_user()
    response = make_response(redirect(url_for('auth.student_login')))
    if user_type == 'student':
        timeout = StudentDashboardRepository.get_timeOut(uid, datetime.now().strftime('%Y-%m-%d'))
        if timeout != 0:
            response.set_cookie(key='time_pressed', expires=0)
            return response
        else:
            return response
    
    return response

@auth_bp.route('/redirect-to-signup')
def redirect_to_signup():
    return redirect(url_for('auth.choose_signup'))


#--SIGN UP--------------------------------------------------------------
@auth_bp.route('/signup')
def choose_signup():
    return render_template('auth/signup/choose_signup.html')

#ADVISER SIGNUP
@auth_bp.route('/adviser-signup', methods=['GET', 'POST'])
def adviser_signup():
    if request.method == 'GET':
        return render_template('auth/signup/adviser_signup.html')
    else:
        name = request.form.get('name')
        email = request.form.get('email')
        school = request.form.get('school')
        password= request.form.get('password')
        type = 'adviser'
        #"Return uid when registered in firebase"

        if not Validators.is_valid_email(email):
            flash('Invalid Email. Please put a valid email')
            return redirect(url_for('auth.adviser_signup'))
        
        if not Validators.is_password_correct_length(password):
            flash('Password must have a lenght of 6 or more')
            return redirect(url_for('auth.adviser_signup'))
        
        count = SignUpRepository.get_count_users(type)        
        uid = Generators.generate_uid(type, count)
        hashed_password = Generators.generate_hash(password)

        #INSERT QUERY
        qry = SignUpRepository.insert_adviser(
            uid=uid, 
            name=name, 
            email=email, 
            school=school, 
            type = type,
            password = hashed_password
        )
                
        if qry == 200:
            return redirect(url_for('auth.student_login'))
        else:
            #create a category in flash
            flash(f'{qry}')
            return redirect(url_for('auth.adviser_signup'))


#STUDENT SIGNUP
@auth_bp.route('/student-signup', methods=['GET', 'POST'])
def student_signup():
    if request.method == 'GET':
        schools = SignUpRepository.list_schools()
        return render_template(template_name_or_list='auth/signup/student_signup.html', schools=schools)
    else:
        name = request.form.get('name')
        email = request.form.get('email')
        school_name = request.form.get('school')
        company = request.form.get('company')
        type = "student"
        total_hours = request.form.get('ojt-hours')
        password = request.form.get('password')

        schoolId = SignUpRepository.get_school_id(school_name) #getting the id of the school

        #setting uo ID
        count = SignUpRepository.get_count_users(type) #for ID generation, returns the newest user counts
        uid = Generators.generate_uid(type, count)
        hashed_password = Generators.generate_hash(password)

        if not Validators.is_valid_email(email):
            flash('Invalid Email. Please put a valid email')
            return redirect(url_for('auth.student_signup'))
        
        if not Validators.is_password_correct_length(password):
            flash('Password must have a lenght of 6 or more')
            return redirect(url_for('auth.student_signup'))
        
        qry = SignUpRepository.insert_student(
            uid = uid,
            name = name,
            email=email,
            school_id = schoolId,
            company = company,
            total_hours = total_hours,
            type = type,
            password = hashed_password,
            active = True
        )
                
        if qry == 200:
            return redirect(url_for('auth.student_login'))
        else:
            flash(f'{qry}')
            return redirect(url_for('auth.student_signup'))


