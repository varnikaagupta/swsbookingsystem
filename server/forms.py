from nbformat import ValidationError
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,EqualTo
from models.models import *

class UserLoginForm(FlaskForm):
  username = StringField('Username',validators=[DataRequired()])
  password = PasswordField('Password',validators=[DataRequired()])
  submit = SubmitField("Log in")

class AppointmentForm(FlaskForm): #Still need to implement proper rules for each specific input
  id = StringField('ID',validators=[DataRequired()])
  student_email = StringField('Student Email',validators=[DataRequired()])
  request_date = StringField('Request Date',validators=[DataRequired()])
  appointment_date = StringField('Appointment Date',validators=[DataRequired()])
  description = StringField('Description',validators=[DataRequired()])
  submit = SubmitField("Make Appointment")

class RegistrationForm(FlaskForm): #Still need to implement proper rules for each specific input
  email = StringField('Email', validators=[DataRequired(),Email()])
  password = PasswordField('Password',validators=[DataRequired()])
  pass_confirm = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('pass_confirm')])
  first_name = StringField('First Name', validators=[DataRequired()])
  last_name = StringField('Last Name', validators=[DataRequired()])
  address = StringField('Address', validators=[DataRequired()])
  postal_code = StringField('Postal Code', validators=[DataRequired()])
  date_of_birth = StringField('Date Of Birth', validators=[DataRequired()])
  student_no = StringField('Student Number', validators=[DataRequired()])
  ohip = StringField('OHIP', validators=[DataRequired()])
  sex = StringField('Sex', validators=[DataRequired()])
  province = StringField('Province', validators=[DataRequired()])
  postal_code = StringField('Postal Code', validators=[DataRequired()])
  perm_addr = StringField('Address', validators=[DataRequired()])
  faculty = StringField('Faculty', validators=[DataRequired()])
  program = StringField('Program', validators=[DataRequired()])
  year = StringField('Year', validators=[DataRequired()])
  degree_type = StringField('Degree', validators=[DataRequired()])
  domestic = StringField('Domestic', validators=[DataRequired()])
  full_time = StringField('Full Time', validators=[DataRequired()])
  submit = SubmitField('Register')

  def validate_email(self, email):
    if Student.query.filter_by(email=self.email.data).first():
      raise ValidationError
  def validate_username(self, username):
    if Student.query.filter_by(username=self.username.data).first():
      raise ValidationError

  #add validate_username function to check whether username is taken

# class UpdateInfo?
# class AdminRegistrationForm?