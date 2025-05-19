from ....extensions import db, insert, select, and_, SQLAlchemyError, IntegrityError
from ..auth_models import SchoolsModel, AdviserModel, StudentModel, OjtListModel

from ..utils.signup_error_helpers import SignUpErrorHelper

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
            raise ValueError(f'An error returned {str(e)}')


    #convert word to school id
    @staticmethod
    def get_school_id(school_name):
        try:
            school = SchoolsModel.query.filter(SchoolsModel.schoolName==school_name).first()

            if school:
                return school.schoolId
            return None
        except SQLAlchemyError as e:
            raise ValueError(f'An error returned {str(e)}')
        
    
    #for id
    @staticmethod
    def get_count_users(type):
        try:
            if type == 'student':
                #change it to getting the last user's id last number
                user = StudentModel.query.order_by(StudentModel.studentId.desc()).first()
                if user:
                    prefix, number = user.studentId.split(':')
                    return int(number)
                else:
                    return 1
            else:
                user = AdviserModel.query.order_by(AdviserModel.adviserId.desc()).first()
                if user:
                    prefix, number = user.adviserId.split(':')
                    return int(number)
                else:
                    return 1
        except SQLAlchemyError as e:
            raise ValueError(f'An error returned {str(e)}')


    #INSERT STUDENT TO DB--------------------------------
    @staticmethod
    def insert_student(**user):
        try:
            #check first if the email is unique
            email_adviser = StudentModel.query.filter(StudentModel.email==user['email']).first()
            email_student = StudentModel.query.filter(StudentModel.email==user['email']).first()
            
            
            if email_adviser or email_student:
                return SignUpErrorHelper.signup_error_checker('email')
            
            data = StudentModel(
                studentId =  user['uid'], # type: ignore
                studentName = user['name'].upper(), # type: ignore
                email = user['email'], # type: ignore # type: ignore
                schoolId = user['school_id'], # type: ignore
                companyName = user['company'], # type: ignore
                totalHours = user['total_hours'], # type: ignore
                userType = user['type'], # type: ignore
                password = user['password'], # type: ignore
                isActive = user['active'] # type: ignore
            )
            db.session.add(data)

            SignUpRepository.insert_ojt_list(student_id=user['uid'], school_id=user['school_id'])
            db.session.commit()
            return 200
        except SQLAlchemyError as e:
            return f'An error returned {str(e)}'
        
    #INSERT OJT-----------------------------------------------------------
    @staticmethod
    def insert_ojt_list(**data):
        try:
            qry = insert(OjtListModel).values(studentId=data['student_id'], schoolId=data['school_id'])
            db.session.execute(qry)
            db.session.commit()
            
        except SQLAlchemyError as e:
            return f'An error returned {str(e)}'


    #INSERT ADVISER TO DB------------------------------------
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
                    return SignUpErrorHelper.signup_error_checker('email')
                return SignUpErrorHelper.signup_error_checker('school')
            else:
                data = AdviserModel(
                    adviserId=user['uid'],  # type: ignore
                    adviserName=user['name'].upper(),  # type: ignore
                    email=user['email'],  # type: ignore
                    schoolName=user['school'],  # type: ignore
                    userType=user['type'], # type: ignore
                    password = user['password'] # type: ignore
                )
                
                db.session.add(data)
                
                SignUpRepository.create_school(school = user['school'], adviser_id = user['uid'])
                db.session.commit()
                return 200
        #If user already exists
        except IntegrityError:
            return SignUpErrorHelper.signup_error_checker('user')
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


