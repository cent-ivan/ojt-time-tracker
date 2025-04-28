from flask import render_template, redirect, url_for, request
from . import auth_bp
from .auth_repository import insert_adviser, insert_student, get_school_id, list_schools

from ...extensions import bcrypt


@auth_bp.route('/student-login')
def student_login():
    return render_template('auth/login/student_login.html')

@auth_bp.route('/adviser-login')
def adviser_login():
    return render_template('auth/login/adviser_login.html')


@auth_bp.route('/signup')
def choose_signup():
    return render_template('auth/signup/choose_signup.html')


#STUDENT SIGNUP
@auth_bp.route('/adviser-signup', methods=['GET', 'POST'])
def adviser_signup():
    if request.method == 'GET':
        return render_template('auth/signup/adviser_signup.html')
    else:
        name = request.form.get('name')
        email = request.form.get('email')
        school = request.form.get('school')
        password= request.form.get('password')
        uid = '180j193'#"Return uid when registered in firebase"

        hashed_password =  bcrypt.generate_password_hash(password).decode('utf-8')
        qry = insert_adviser(
            uid=uid, name=name, 
            email=email, 
            school=school, 
            type = 'adviser',
            hashed_password=hashed_password
        )
        if qry == '202':
            return redirect(url_for('auth.student_login'))
        else:
            return qry


#ADVISER SIGNUP
@auth_bp.route('/student-signup', methods=['GET', 'POST'])
def student_signup():
    if request.method == 'GET':
        schools = list_schools()
        return render_template(template_name_or_list='auth/signup/student_signup.html', schools=schools)
    else:
        name = request.form.get('name')
        email = request.form.get('email')
        school_name = request.form.get('school')
        company = request.form.get('company')
        total_hours = request.form.get('ojt-hours')
        password = request.form.get('password')
        uid = '13ehjc544'#"Return uid when registered in firebase"

        schoolId = get_school_id(school_name)
        hashed_password =  bcrypt.generate_password_hash(password).decode('utf-8')
        
        qry = insert_student(
            uid = uid,
            name = name,
            email=email,
            school_id = schoolId,
            company = company,
            total_hours = total_hours,
            type = "student",
            password= hashed_password
        )
        if qry == '202':
            return redirect(url_for('auth.student_login'))
        else:
            return qry


