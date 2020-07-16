from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from ..models import User
from .. import db
from . import auth
from .form import RegistrationForm, LoginForm



@auth.route('/signup', methods= ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
        title = 'Sign up'
    return render_template('auth/register.html', signup_form= form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(name = login_form.username.data).first()
        if user is not None and user.verify_password(login_form.password.data):

            login_user(user,login_form.remember.data)
            flash('Logged in successfully.')

            return redirect(request.args.get('next') or url_for('main.work_session'))
        flash('Invalid username or Password')

    title = "login"
    return render_template('auth/login.html',login_form = login_form,title=title)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
