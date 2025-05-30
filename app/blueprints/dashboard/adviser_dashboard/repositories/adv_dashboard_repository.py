from datetime import date, datetime

from .....extensions import db, insert, update, select, and_, SQLAlchemyError, IntegrityError, psycopg, LiteralString, cast
from ...student_dashboard.student_dashboard_models import TimeSheetModel
from ....auth.auth_models import SchoolsModel, StudentModel

from . import PostgresDatabaseConfig

class AdviserDashboardRepository:

    #CONVERTS word to school id
    @staticmethod
    def get_school_id(school_name):
        try:
            school = SchoolsModel.query.filter(SchoolsModel.schoolName==school_name).first()

            if school == None:
                return None
            return school.schoolId
        except SQLAlchemyError as e:
            return f'An error returned {str(e)}'
        
    #READS the sql file,reads it and returns a string. Recommended
    @staticmethod
    def load_query(filename):
        with open(f'app/sql/{filename}','r') as sql:
            return cast(LiteralString, sql.read())
    
    #returns a list list of tuples with data, raw data needs to be formated
    @staticmethod
    def get_ojt_list(school_name):
        #for the 
        try:
            school_id = AdviserDashboardRepository.get_school_id(school_name)
            data = []
            with psycopg.connect(**PostgresDatabaseConfig().return_dict()) as conn:
                with conn.cursor() as cur:
                    query = AdviserDashboardRepository.load_query('get_ojt_list.sql')
                    cur.execute(query, (school_id,))
                    data =  cur.fetchall()

            return data

        except psycopg.Error as Error:
            print("Error in Postgre", Error)
    

    #returns a list list of tuples with data, raw data needs to be formated
    @staticmethod
    def get_ojt_list_filter(school_name, search_data):
        #for the 
        try:
            school_id = AdviserDashboardRepository.get_school_id(school_name)
            data = []
            with psycopg.connect(**PostgresDatabaseConfig().return_dict()) as conn:
                with conn.cursor() as cur:
                    query = AdviserDashboardRepository.load_query('get_ojt_list_filter.sql')
                    cur.execute(query, (school_id, search_data,))
                    data =  cur.fetchall()

            return data

        except psycopg.Error as Error:
            print("Error in Postgre", Error)

    
    #GET timesheet
    @staticmethod
    def get_student_timesheet(student_id):
        try:
            timesheet = TimeSheetModel.query.filter(TimeSheetModel.studentId == student_id).all()
            result = []
            for time in timesheet:
                data = {
                    'date': time.date,
                    'time_in':time.timeIn,
                    'time_out':time.timeOut if time.timeOut != None else 0,
                    'hours_worked':time.hoursWorked if time.hoursWorked != None else 0 ,
                    'status':time.dutyStatus,
                    'note':time.note
                }   
                result.append(data)
            return result
        except SQLAlchemyError as e:
            return f'An error returned {str(e)}'
        
    
    #GET student info
    @staticmethod
    def get_student_data(uid):
        try:
            user = StudentModel.query.filter(StudentModel.studentId == uid).first()
            return user
        except SQLAlchemyError as e:
            return f'An error returned {str(e)}'