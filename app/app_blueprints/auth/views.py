from flask import render_template, redirect, url_for, request, flash
from . import auth_bp
#always import repository in view if any
from .repositories.signup_repository import SignUpRepository
from .utils.validators import Validators

from ...extensions import bcrypt


#--LOG IN---------------------------------------------------------------
@auth_bp.route('/student-login', methods=['GET', 'POST'])
def student_login():
    return render_template('auth/login/student_login.html')

@auth_bp.route('/adviser-login', methods=['GET', 'POST'])
def adviser_login():
    return render_template('auth/login/adviser_login.html')

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
        uid = '180j19833'#"Return uid when registered in firebase"
        
        if Validators.is_valid_email(email):
            if Validators.is_password_correct_length(password):
                hashed_password =  bcrypt.generate_password_hash(password).decode('utf-8') #turns to hashed text
                #INSERT QUERY
                qry = SignUpRepository.insert_adviser(
                    uid=uid, name=name, 
                    email=email, 
                    school=school, 
                    type = 'adviser',
                    hashed_password=hashed_password
                )
                if qry == 200:
                    return redirect(url_for('auth.student_login'))
                else:
                    flash(f'{qry}')
                    return redirect(url_for('auth.adviser_signup'))
                
            else:
                flash('Password must have a lenght of 5 or more')
                return redirect(url_for('auth.adviser_signup'))
        else:
            flash('Invalid Email. Please put a valid email')
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
        total_hours = request.form.get('ojt-hours')
        password = request.form.get('password')
        uid = '13ehjc5sd'#"Return uid when registered in firebase"

        schoolId = SignUpRepository.get_school_id(school_name)
        hashed_password =  bcrypt.generate_password_hash(password).decode('utf-8')
        
        if Validators.is_valid_email(email):
            if Validators.is_password_correct_length(password):
                qry = SignUpRepository.insert_student(
                    uid = uid,
                    name = name,
                    email=email,
                    school_id = schoolId,
                    company = company,
                    total_hours = total_hours,
                    type = "student",
                    password= hashed_password
                )
                if qry == 200:
                    return redirect(url_for('auth.student_login'))
                else:
                    flash(f'{qry}')
                    return redirect(url_for('auth.student_signup'))
                
            else:
                flash('Password must have a lenght of 5 or more')
                return redirect(url_for('auth.student_signup'))
        else:
            flash('Invalid Email. Please put a valid email')
            return redirect(url_for('auth.student_signup'))


