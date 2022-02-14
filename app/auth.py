#user auth routes
#trying to figure out flask_login for user session management, not yet set up properly

from flask import render_template,flash,redirect,url_for,request,Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from forms import UserLoginForm,AdminLoginForm,AppointmentForm,RegistrationForm
from models.models import Student, Appointment

auth = Blueprint('auth',__name__)

@auth.route('/register',methods=['GET','POST'])
def register():
  form = RegistrationForm()

  if form.validate_on_submit():
    user = Student(email=form.email.data,
                password=form.password.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                address=form.address.data,
                postal_code=form.postal_code.data,
                date_of_birth=form.date_of_birth.data,
                student_no=form.student_no.data,
                ohip=form.ohip.data,
                sex=form.sex.data,
                province=form.province.data,
                postal_code=form.postal_code.data,
                perm_addr=form.perm_addr.data,
                faculty=form.faculty.data,
                program=form.program.data,
                year=form.year.data,
                degree_type=form.degree_type.data,
                domestic=form.domestic.data,
                full_time=user.full_time.data)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for(auth.login))

  return render_template('register.html',form=form)

@auth.route('/login',methods=['GET','POST'])
def login():
  form = UserLoginForm()

  if form.validate_on_submit():
    user = Student.query.filter_by(email=form.email.data).first()
    if user.check_pw(form.password.data) and user is not None: #check_pw doesn't exist yet

      login_user(user)

      next = request.args.get('next')

      if next ==None or not next[0]=='/':
        next = url_for('core.index')

      return redirect(next)

  return render_template('login.html',form=form)

@auth.route('/appointment',methods=['GET','POST'])
@login_required
def appointment():
  form = AppointmentForm()

  if form.validate_on_submit():
    appointment = Appointment(id=form.id.data,
                              student_email=form.student_email.data,
                              request_date=form.request_date.data,
                              appointment_date=form.appointment_date.data,
                              description=form.description.data)
    db.session.add(appointment)
    db.session.commit()
    return redirect(url_for(auth.login))
