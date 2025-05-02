from flask import redirect, url_for
from ....extensions import db, insert, SQLAlchemyError, IntegrityError
from ..auth_models import SchoolsModel, AdviserModel, StudentModel

from ..utils.signup_error_checker import SignUpErrorChecker

#This serve as an interaction with the view to the database. SQL queries are performed here

class SignUpRepository:

    #REGISTER---------------------------------------------------------------------------------
    #for the dropdown, to show registered schools
    @staticmethod #this enables the method to be used directly.
    def list_schools() -> list:
        try:
            schools = SchoolsModel.query.all()
            return schools
        except SQLAlchemyError as e:
            return f'An error returned {str(e)}'


    #convert word to school id
    @staticmethod
    def get_school_id(school_name):
        try:
            school = SchoolsModel.query.filter(SchoolsModel.schoolName==school_name).first()

            return school.schoolId
        except SQLAlchemyError as e:
            return f'An error returned {str(e)}'


    #INSERT STUDENT TO DB
    @staticmethod
    def insert_student(**user) -> str:
        try:
            #check first if the email is unique
            school = AdviserModel.query.filter(AdviserModel.schoolName==user['school']).first()
            email = AdviserModel.query.filter(AdviserModel.email==user['email']).first()
            
            if school:
                if email:
                    return SignUpErrorChecker.signup_error_checker('email')
                return SignUpErrorChecker.signup_error_checker('school')
            
            data = StudentModel(
                studentId =  user['uid'],
                studentName = user['name'],
                email = user['email'],
                schoolId = user['school_id'],
                companyName = user['company'],
                totalHours = user['total_hours'],
                userType = user['type'],
            )
            db.session.add(data)
            db.session.commit()
            return 200
        except SQLAlchemyError as e:
            return f'An error returned {str(e)}'


    #INSERT ADVISER TO DB
    @staticmethod
    def insert_adviser(**user):
        try:
            #1. Retrive data from db first
            school = AdviserModel.query.filter(AdviserModel.schoolName==user['school']).first()
            email = AdviserModel.query.filter(AdviserModel.email==user['email']).first()
            
            #2. Check if there is data
            if school:
                if email:
                    #assign error type
                    return SignUpErrorChecker.signup_error_checker('email')
                return SignUpErrorChecker.signup_error_checker('school')
            else:
                data = AdviserModel(
                    adviserId=user['uid'], 
                    adviserName=user['name'], 
                    email=user['email'], 
                    schoolName=user['school'], 
                    userType=user['type'])
                db.session.add(data)
                
                SignUpRepository.create_school(school = user['school'], adviser_id = user['uid'])
                db.session.commit()
                return 200
        #If user already exists
        except IntegrityError:
            return SignUpErrorChecker.signup_error_checker('user')
        except SQLAlchemyError as e:
            return f'An error returned {str(e)}'


    @staticmethod
    def create_school(**data) -> None:
        #when an adviser object is created it automatically inserts or create a data about the school
        try:
            qry = insert(SchoolsModel).values(schoolName=data['school'], adviserId=data['adviser_id'])
            db.session.execute(qry)
            db.session.commit()
        except SQLAlchemyError as e:
            print("an Error has occured")


