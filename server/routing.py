from flask import render_template,request,redirect,url_for,session
# to be added to init.py
from flask_login import current_user, login_user, logout_user, login_required, LoginManager
from models.models import Appointment, Student, createMockAppointments,db,init,bookAppointment
import datetime
from datetime import time
import json
import os
from server import app

createMockAppointments()

package_dir = os.path.dirname(
    os.path.abspath(__file__)
)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Student.query.get(int(user_id))

@app.route('/')
def index():
    if 'logged_in' in session:
        return render_template('index_profile.html')
    return render_template('index.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.form['Username']
        print(username)
        user = Student.query.filter_by(username = username).first()
        print(user.password)
        if user is not None and user.password == request.form['password']:
            login_user(user)
            session['logged_in'] = user.username
            return redirect('/')

    return render_template('login.html'), 404

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        email = request.form['email']
        username = request.form['Username']
        password = request.form['password']

        if Student.query.filter_by(email=email).first():
            return ('Email already exists')

        user = Student(email=email, username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in', None)
    logout_user()
    return redirect('/')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/booking', methods=['GET'])
@login_required
def booking():
    return render_template('booking.html')

@app.route('/booking', methods=['POST'])
def booking_check():
    times_list = []
    date_str = request.form['date']
    date_obj = datetime.datetime.strptime(date_str, '%d/%m/%Y')

    for i in range(9, 19):
        date_obj = date_obj.replace(hour=i)
        if(Appointment.query.filter_by(appointment_date=date_obj).first() is None):
            time = date_obj.strftime('%H:%M')
            date = date_obj.strftime('%d/%m/%Y')
            times_list.append({'start_time':time, 'date':date})

    print('times_list \n')
    print(times_list)

    return render_template('datetimes.html', times_list=times_list)

@app.route('/confirmation', methods=['POST'])
def confirmation():
    date = request.form['bookDate']
    date = date.replace("\'", "\"")
    print(date)
    date = json.loads(date)
    print('DATE DICTIONARY OBJECT: ')
    print(type(date))
    print(date)
    date_str = date['date'] + ' ' + date['start_time']

    date_obj = datetime.datetime.strptime(date_str, '%d/%m/%Y %H:%M')
    print('date_str: \n')
    print(date_str)

    print('date_obj: ')
    print(date_obj)


    username = session['logged_in']
    user = Student.query.filter_by(username = username).first()

    if(user is not None):
        success = bookAppointment(user, date_obj)
        return render_template('confirmation.html', msg='Success!', date=date['date'], start_time=date['start_time'])
    else:
        return render_template('/', msg='Error! Could not book appointment')
