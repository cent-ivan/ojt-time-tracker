from datetime import date, datetime

from .....extensions import db, insert, update, select, and_, SQLAlchemyError, IntegrityError
from ..student_dashboard_models import TimeSheetModel


class StudentDashboardRepository:
    
    @staticmethod
    def get_timesheet(uid):
        timesheet = TimeSheetModel.query.filter(TimeSheetModel.studentId == uid).all()
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

    @staticmethod
    def get_timein(uid, date):
        qry = select(TimeSheetModel.timeIn, TimeSheetModel.date).where(and_(TimeSheetModel.studentId == uid, TimeSheetModel.date == date))
        return db.session.execute(qry).first()
    

    @staticmethod
    def get_count_days(uid) -> int:
        #for counting the days
        qry = db.session.query(TimeSheetModel.date).filter(TimeSheetModel.studentId == uid).count()
        if qry == None:
            return 0
        else:
            return qry

    #FOR TIMEIN
    @staticmethod
    def insert_timein(uid, date, timein):
        #checks first for an existing date
        if StudentDashboardRepository.get_timein(uid, date) != date:
            stm = insert(TimeSheetModel).values(studentId=uid, date=date, timeIn=timein)
            db.session.execute(stm)
            db.session.commit()
        else:
            update_qry = update(TimeSheetModel).values(studentId=uid, date=date, timeIn=timein).where(and_( TimeSheetModel.studentId==uid, TimeSheetModel.date == date))
            db.session.execute(update_qry)
            db.session.commit()

    #FOR TIMEOUT
    def insert_timeout(uid, date, timeout, hours_worked, status, note):
        update_qry = update(TimeSheetModel).values(timeOut = timeout, hoursWorked = hours_worked, dutyStatus = status, note = note).where(and_( TimeSheetModel.studentId==uid, TimeSheetModel.date == date))
        db.session.execute(update_qry)
        db.session.commit()
  