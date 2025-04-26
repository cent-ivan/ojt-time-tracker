from ...extensions import db, Column, Integer, String, Date, Time
from ...extensions import select, insert, orm, ForeignKey

class TimeSheetModel(db.Model):
    __tablename__ = 'timesheettbl'

    id = Column(Integer,primary_key=True)
    studentId = Column(Integer, ForeignKey('studentstbl.student_id'), name='student_id')
    date = Column(Date, nullable=False, name='date')
    timeIn = Column(Time, nullable=False, name='time_in')
    timeOut = Column(Time, nullable=False, name='time_out') #inserts string
    hoursWorked = Column(Integer, nullable=False, name='hours_worked')
    dutyStatus = Column(String(30), nullable=False, name='status')
    note = Column(String(50), name='note')