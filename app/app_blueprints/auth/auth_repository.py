from ...extensions import db, insert
from .models import SchoolsModel, AdviserModel, StudentModel

def get_adviser(uid) -> AdviserModel:
    user = AdviserModel.query.get(uid)
    return user

def get_student(uid) -> StudentModel:
    user = StudentModel.query.get(uid)
    return user

def create_school(adviser):
    #when an adviser object is created it automatically inserts or create a data about the school
    try:
        qry = insert(SchoolsModel).values(schoolName=adviser.schoolName)
        db.session.execute(qry)
        db.session.commit()
    except:
        print("an Error has occured")

