from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from flask_login import login_user, logout_user, login_required, current_user
from create_app import db

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET','POST'])
def login():
    if(request.method == 'GET'):
        return render_template('login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Please signup before logging in")
            return redirect(url_for('auth.signup'))
        elif not(check_password_hash(user.password,password)):
            flash("Incorrect username or password")
            return redirect(url_for('auth.login'))
        login_user(user,remember=remember)
        return redirect(url_for('main.index'))

@auth.route('/signup', methods=['GET','POST'])
def signup():
    if(request.method == 'GET'):
        return render_template('signup.html')
    else:
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists')
            return redirect(url_for('auth.signup'))

        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        flash('Signed up successfully! Please login to enter')
        return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out. Please login to continue..')
    return redirect(url_for('auth.login'))