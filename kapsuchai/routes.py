import os
import secrets
from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from kapsuchai import app, bcrypt, db
from kapsuchai.models import User
from kapsuchai.forms import RegistrationForm, LoginForm
from sqlalchemy import func


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='home')


@app.route('/about')
def about():
    return render_template('about.html', title='about')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(lastname=form.lastname.data,firstname=form.firstname.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='register', form=form)


@app.route('/account', methods=['GET', 'POST'])
def account():
    return render_template('account.html', title='account', form = form)
