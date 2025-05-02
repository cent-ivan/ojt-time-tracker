from flask import render_template, redirect, url_for, request, flash
from . import auth_bp
#always import repository in view if any
from .repositories.signup_repository import SignUpRepository
from .utils.validators import Validators

from ...extensions import bcrypt #you do not need bcrypt for this, because Firebase handles hashing and storing of passwords
from .firebase_auth_services import FirebaseAuth
'''
to avoid circular imports: Make sure that two or more modules don’t rely on importing each other at the top level during initial loading.
Like (auth_views.py) signup_repository import SignUpRepository -> from ....extensions import db -> from .app_blueprints.auth.firebase_auth_services import FirebaseAuth so it didnt read the 'db' variable
But after it reads 'import SignUpRepository' it then import again extensions like (auth_views.py) ...extensions import FirebaseAuth -> from .app_blueprints.auth.firebase_auth_services import FirebaseAuth
'''


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
                #INSERT QUERY
                user_id = FirebaseAuth.register_to_firebase_auth(email, password)
                if user_id == 'exists':
                    flash('Password must have a lenght of 5 or more')
                    return redirect(url_for('auth.adviser_signup'))
                else:
                    qry = SignUpRepository.insert_adviser(
                        uid=user_id, 
                        name=name, 
                        email=email, 
                        school=school, 
                        type = 'adviser',
                    )
                
                    if qry == 200:
                        return redirect(url_for('auth.student_login'))
                    else:
                        flash(f'')
                        return redirect(url_for('auth.adviser_signup'))
                    
            else:
                flash('Password must have a lenght of 6 or more')
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

        schoolId = SignUpRepository.get_school_id(school_name) #getting the id of the school
        
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


