from flask import render_template,request,redirect,url_for
from flask_login import current_user, login_user, logout_user, login_required, LoginManager
from models.models import Appointment, Student, createMockAppointments,db,init
import datetime
from datetime import time
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
    logout_user()
    return redirect(url_for(index))

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
            times_list.append({'start_time':time})

    print(times_list)

    return render_template('datetimes.html', times_list=times_list)
