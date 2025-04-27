from ...extensions import db, insert, SQLAlchemyError,select
from .models import SchoolsModel, AdviserModel, StudentModel

def get_adviser(uid) -> AdviserModel:
    user = AdviserModel.query.get(uid)
    return user

def get_student(uid) -> StudentModel:
    user = StudentModel.query.get(uid)
    return user


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
        school = SchoolsModel.query.all()
        return school
    except SQLAlchemyError as e:
         return f'An error returned {str(e)}'


def insert_student(**user) -> str:
    try:
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

      
def insert_adviser(**user) -> str:
    try:
        data = AdviserModel(adviserId=user['uid'], adviserName=user['name'], email=user['email'], schoolName=user['school'], userType=user['type'], password = user['hashed_password'])
        qry = db.session.add(data)
        
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
    except:
        print("an Error has occured")


