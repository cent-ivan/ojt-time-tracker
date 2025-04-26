#table with relationships
from ...extensions import db, UserMixin, Column, Integer, String, ForeignKey, orm

#CHANGE
class AdviserModel(db.Model, UserMixin):
    __tablename__ = 'adviserstbl'

    adviserId = Column(Integer, primary_key=True, name='adviser_id')
    adviserName = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    schoolName = Column(String(50), nullable=False, unique=True)
    userType = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False, unique=True)

    school = orm.relationship('SchoolModel', back_populates='adviser')

    #create this for overriding the User_loader in login_manager -> goto config.py. NOTE you can override methods in packages
    def get_id(self):
        return f"adviser-{self.adviserId}"


class SchoolsModel(db.Model):
    __tablename__ = 'schoolstbl'

    schoolId = Column(Integer, primary_key=True, name='school_id')
    schoolName = Column(String(50), nullable=False, unique=True)
    adviserId = Column(Integer, ForeignKey('adviserstbl.adviser_id'), name='adviser_id')

    #establish relationship to AdviserModel, there must a`school` variable in AdviserModel. Meaning I have this connection with adviser model
    adviser = orm.relationship('AdviserModel', back_populates='school') 
    ojtList = orm.relationship('OjtListModel', back_populates='school')


class StudentModel(db.Model, UserMixin):
    __tablename__ = 'studentstbl'

    studentId =  Column(Integer, primary_key=True, name='student_id')
    studentName = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    schoolId = Column(Integer, ForeignKey('schoolstbl.school_id'), name='school_id')
    companyName = Column(String(50), nullable=False, unique=True)
    totalHours = Column(Integer, nullable=False)
    userType = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False, unique=True)

    ojtList = orm.relationship('OjtListModel', back_populates='student')

     #create this for overriding the User_loader in login_manager -> goto config.py
    def get_id(self):
        return f"student-{self.studentId}"


#create TimeSheetModel

#many-to-many
class OjtListModel(db.Model):
    __tablename__ = 'ojtlisttbl'

    id = Column(Integer,primary_key=True)
    studentId = Column(Integer, ForeignKey('studentstbl.student_id'), name='student_id')
    schoolId = Column(Integer, ForeignKey('schoolstbl.school_id'), name='school_id')

    student = orm.relationship('StudentModel', back_populates='ojtList')
    school = orm.relationship('OjtListModel', back_populates='ojtList')