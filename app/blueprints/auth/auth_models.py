#table with relationships
from ...extensions import db, UserMixin, Column, Integer, Boolean, String, ForeignKey, orm

#CHANGE
class AdviserModel(db.Model, UserMixin):
    __tablename__ = 'adviserstbl'

    adviserId = Column(String(255), primary_key=True, name='adviser_id')
    adviserName = Column(String(50), nullable=False, name='adviser_name')
    email = Column(String(50), nullable=False, unique=True, name='email')
    schoolName = Column(String(50), nullable=False, unique=True, name='school_name')
    userType = Column(String(50), nullable=False, name='type')
    password = Column(String(255), nullable=False, name='password')


    school = orm.relationship('SchoolsModel', back_populates='adviser')


    #create this for overriding the User_loader in login_manager -> goto config.py. NOTE you can override methods in packages
    def get_id(self):
        return str(self.adviserId)


class SchoolsModel(db.Model):
    __tablename__ = 'schoolstbl'

    schoolId = Column(Integer, primary_key=True, name='school_id')
    schoolName = Column(String(50), nullable=False, unique=True, name='school_name')
    adviserId = Column(String(255), ForeignKey('adviserstbl.adviser_id'), name='adviser_id')

    #establish relationship to AdviserModel, there must a`school` variable in AdviserModel. Meaning I have this connection with adviser model
    adviser = orm.relationship('AdviserModel', back_populates='school') 
    ojtList = orm.relationship('OjtListModel', back_populates='school')


class StudentModel(db.Model, UserMixin):
    __tablename__ = 'studentstbl'

    studentId =  Column(String(255), primary_key=True, name='student_id')
    studentName = Column(String(50), nullable=False, unique=True, name='student_name')
    email = Column(String(50), nullable=False, unique=True, name='email')
    schoolId = Column(Integer, ForeignKey('schoolstbl.school_id'), name='school_id')
    companyName = Column(String(50), nullable=False, name='company_name')
    totalHours = Column(Integer, nullable=False, name='total_hours')
    userType = Column(String(50), nullable=False, name='type')
    password = Column(String(255), nullable=False, name='password')
    isActive = Column(Boolean, nullable=False, name='is_active')

    ojtList = orm.relationship('OjtListModel', back_populates='student')
    timesheet = orm.relationship('TimeSheetModel', back_populates='student')

     #create this for overriding the User_loader in login_manager -> goto config.py
    def get_id(self):
        return str(self.studentId)


#create TimeSheetModel

#many-to-many
class OjtListModel(db.Model):
    __tablename__ = 'ojtlisttbl'

    id = Column(Integer,primary_key=True)
    studentId = Column(String(255), ForeignKey('studentstbl.student_id'), name='student_id')
    schoolId = Column(Integer, ForeignKey('schoolstbl.school_id'), name='school_id')

    student = orm.relationship('StudentModel', back_populates='ojtList')
    school = orm.relationship('SchoolsModel', back_populates='ojtList')