from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)

class Student(db.Model):
    user_name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(
        db.String(120), unique=True, nullable=False,
        primary_key=True)
    password = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(200), unique=False, nullable=False)
    postal_code = db.Column(db.String(6), unique=False, nullable=False)
    date_of_birth = db.Column(db.DateTime, unique=False, nullable=False)
    student_no = db.Column(db.String(8), unique=True, nullable=False)
    ohip = db.Column(db.String(12), unique=True, nullable=False)
    sex = db.Column(db.String(1), unique=False, nullable=False)
    province = db.Column(db.String(2), unique=False, nullable=False)
    perm_addr = db.Column(db.String(200), unique=False, nullable=False)
    faculty = db.Column(db.String(50), unique=False, nullable=False)
    program = db.Column(db.String(50), unique=False, nullable=False)
    year = db.Column(db.String(1), unique=False, nullable=False)
    degree_type = db.Column(db.String(50), unique=False, nullable=False)
    domestic = db.Column(db.Boolean, unique=False, nullable=False)
    full_time = db.Column(db.Boolean, unique=False, nullable=False)
    appointments = db.relationship('Request', backref='student', lazy=True)
    emerg_contact = db.relationship('EmergContact', backref='student', lazy=True)    

    def __repr__(self):
        return '<Student %r>' % self.email


class Request(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False)
    student_email = db.Column(db.String(120), db.ForeignKey('student.email'), nullable = False)
    request_date = db.Column(db.DateTime, nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    
    def __repr__(self):
        return '<Request %r>' % self.id


class EmergContact(db.Model):
    student_email = db.Column(db.String(120), db.ForeignKey('student.email'), nullable = False)
    full_name = db.Column(db.String(200), nullable=False)
    relationship = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    province = db.Column(db.String(2), nullable=False)
    postal_code = db.Column(db.String(6), nullable=False)
    country = db.Column(db.String(50), nullable=False)



def create_user(user):
    
    user = Student(
        email=user["email"],
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
        postal_code=user["postal_code"],
        perm_addr=user["perm_addr"],
        faculty=user["faculty"],
        program=user["program"],
        year=user["year"],
        degree_type=user["degree_type"],
        domestic=user["domestic"],
        full_time=user["full_time"]
        )
    
    # add it to the current database session
    db.session.add(user)
    # actually save the user object
    db.session.commit()

    return

def login(email, password):
    return