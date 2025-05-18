from ....extensions import db, insert, select, and_, SQLAlchemyError, IntegrityError
from ..auth_models import SchoolsModel, AdviserModel, StudentModel


class LoginRepository:
    #LOGIN-----------------------------------------------------------------------------------
    @staticmethod
    def check_adviser(email):
        try:
            user = AdviserModel.query.filter(AdviserModel.email == email).first()
            if user:
                return user
            return None
        except SQLAlchemyError as e:
            return f'An error returned {str(e)}'
        
    @staticmethod
    def check_student(email):
        try:
            user = StudentModel.query.filter(StudentModel.email == email).first()
            if user:
                return user
            return None #returns none if 0 results
        except SQLAlchemyError as e:
            return f'An error returned {str(e)}' 