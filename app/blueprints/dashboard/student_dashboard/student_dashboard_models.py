from ....extensions import db, Column, Integer, String, Date, Time
from ....extensions import select, insert, orm, ForeignKey

class TimeSheetModel(db.Model):
    __tablename__ = 'timesheettbl'

    id = Column(Integer,primary_key=True)
    studentId = Column(String(255), ForeignKey('studentstbl.student_id'), name='student_id')
    date = Column(Date, nullable=False, index=True, name='date')
    timeIn = Column(Time, nullable=True, name='time_in')
    timeOut = Column(Time, nullable=True, name='time_out') #inserts string
    hoursWorked = Column(Integer, nullable=True, name='hours_worked')
    dutyStatus = Column(String(30), nullable=True, name='status')
    note = Column(String(50), nullable=True, name='note')

    student = orm.relationship('StudentModel', back_populates='timesheet')