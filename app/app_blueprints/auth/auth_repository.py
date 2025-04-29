from flask import redirect, url_for
from ...extensions import db, insert, SQLAlchemyError,select
from .models import SchoolsModel, AdviserModel, StudentModel

from .error_handlers.signup_error_handlers import signup_checker

#This serve as an interaction with the view to the database. SQL queries are performed here



#for the dropdown, to show registered schools
def list_schools() -> list:
    try:
        schools = SchoolsModel.query.all()
        return schools
    except SQLAlchemyError as e:
         return f'An error returned {str(e)}'


#convert word to school id
def get_school_id(school_name):
    try:
        school = SchoolsModel.query.filter(SchoolsModel.schoolName==school_name).first()
        return school.schoolId
    except SQLAlchemyError as e:
         return f'An error returned {str(e)}'


#INSERT STUDENT TO DB
def insert_student(**user) -> str:
    try:
        #check first if the email is unique
        school = AdviserModel.query.filter(AdviserModel.schoolName==user['school']).first()
        email = AdviserModel.query.filter(AdviserModel.email==user['email']).first()
        
        if school:
            if email:
                return signup_checker('email')
            return signup_checker('school')
        
        data = StudentModel(
            studentId =  user['uid'],
            studentName = user['name'],
            email = user['email'],
            schoolId = user['school_id'],
            companyName = user['company'],
            totalHours = user['total_hours'],
            userType = user['type'],
            password = user['password']
        )
        db.session.add(data)
        db.session.commit()
        return '202'
    except SQLAlchemyError as e:
        return f'An error returned {str(e)}'


#INSERT ADVISER TO DB
def insert_adviser(**user) -> str:
    try:
        school = AdviserModel.query.filter(AdviserModel.schoolName==user['school']).first()
        email = AdviserModel.query.filter(AdviserModel.email==user['email']).first()
        
        if school:
            if email:
                return signup_checker('email')
            return signup_checker('school')
        else:
            data = AdviserModel(adviserId=user['uid'], adviserName=user['name'], email=user['email'], schoolName=user['school'], userType=user['type'], password = user['hashed_password'])
            db.session.add(data)
            
            create_school(school = user['school'], adviser_id = user['uid'])
            db.session.commit()
            return '202'
    except SQLAlchemyError as e:
        return f'An error returned {str(e)}'


def create_school(**data) -> None:
    #when an adviser object is created it automatically inserts or create a data about the school
    try:
        qry = insert(SchoolsModel).values(schoolName=data['school'], adviserId=data['adviser_id'])
        db.session.execute(qry)
        db.session.commit()
    except SQLAlchemyError as e:
        print("an Error has occured")


