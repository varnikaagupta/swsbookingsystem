from enum import unique
import sys
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
sys.path.append("..")
from server import app

db = SQLAlchemy(app)

class Student(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False,)
    username = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    address = db.Column(db.String(200), unique=False)
    postal_code = db.Column(db.String(6), unique=False)
    date_of_birth = db.Column(db.DateTime, unique=False)
    student_no = db.Column(db.String(8), unique=True)
    ohip = db.Column(db.String(12), unique=True)
    sex = db.Column(db.String(1), unique=False)
    province = db.Column(db.String(2), unique=False)
    perm_addr = db.Column(db.String(200), unique=False)
    faculty = db.Column(db.String(50), unique=False)
    program = db.Column(db.String(50), unique=False)
    year = db.Column(db.String(1), unique=False)
    degree_type = db.Column(db.String(50), unique=False)
    domestic = db.Column(db.Boolean, unique=False)
    full_time = db.Column(db.Boolean, unique=False)
    appointments = db.relationship('Appointment', backref='student', lazy=True)
    emerg_contact = db.relationship('EmergContact', backref='student', lazy=True)

    def __repr__(self):
        return '<Student %r>' % self.email


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_email = db.Column(db.String(120), db.ForeignKey('student.email'), nullable = False)
    appointment_date = db.Column(db.DateTime, nullable=False, unique=True)
    description = db.Column(db.String(2000), nullable=True)

    def __repr__(self):
        return '<Appointment %r>' % self.id


class EmergContact(db.Model):
    student_email = db.Column(db.String(120), db.ForeignKey('student.email'), nullable = False, primary_key=True)
    full_name = db.Column(db.String(200), nullable=False)
    relationship = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    province = db.Column(db.String(2), nullable=False)
    postal_code = db.Column(db.String(6), nullable=False)
    country = db.Column(db.String(50), nullable=False)


def init():
    db.drop_all()
    db.create_all()

def create_user(user):

    user = Student(
        email=user["email"],
        username=user["username"],
        password=user["password"],
        first_name=user["first_name"],
        last_name=user["last_name"],
        address=user["address"],
        postal_code=user["postal_code"],
        date_of_birth=user["date_of_birth"],
        student_no=user["student_no"],
        ohip=user["ohip"],
        sex=user["sex"],
        province=user["province"],
        perm_addr=user["perm_addr"],
        faculty=user["faculty"],
        program=user["program"],
        year=user["year"],
        degree_type=user["degree_type"],
        domestic=user["domestic"],
        full_time=user["full_time"]
        )

    # add it to the current database session if it exists
    if (user is not None):
        db.session.add(user)
        # commit the change
        db.session.commit()
        return user

    else:
        return None


def login(email, password):
    '''
    Check login information
    Parameters:
        email (string)
        password (string)

    Returns:
        user object if successful, returns none o/w
    '''
    if((len(email) == 0) or (len(password) == 0)):
        return False

    valids = Student.query.filter_by(email=email, password=password).all()

    if len(valids) != 1:
        return None

    return valids[0]

def createMockAppointments():
    init()
    user = Student(username='mockUser', password='test123456@1', email='mock@test.com')
    db.session.add(user)
    
    for i in range(9, 14):
        appointment_date=datetime.datetime(2022, 3, 29, i, 0)
        newAppointment = Appointment(student_email='mock@test.com',\
             appointment_date=appointment_date,\
             description='testing description')
        print(appointment_date)
        db.session.add(newAppointment)
    
    db.session.commit()
    return
    
def bookAppointment(user, date):
    '''
    books a new appointment using the user object and date object.
    Returns appointment object if successful
    otherwise return None
    
    '''
    if(Appointment.query.filter_by(appointment_date=date).first() is None):
        new_appointment = Appointment(student_email=user.email, appointment_date=date)
        db.session.add(new_appointment)
        db.session.commit()

        return new_appointment

    else:

        return None
    
