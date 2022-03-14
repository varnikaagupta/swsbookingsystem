from flask import render_template,request,redirect,url_for
from flask_login import current_user, login_user, logout_user, login_required
from models.models import Student,db
import os
from server import app

package_dir = os.path.dirname(
    os.path.abspath(__file__)
)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(index))

    if request.method == 'POST':
        username = request.form['Username']
        user = Student.query.filter_by(username = username).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for(index))

    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for(index))

    if request.method == 'POST':
        email = request.form['email']
        username = request.form['Username']
        password = request.form['password']

        if Student.query.filter_by(email=email).first():
            return ('Email already exists')

        user = Student(email=email, username=username)
        user.set_password(password)
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

@app.route('/booking')
@login_required
def booking():
    return render_template('booking.html')