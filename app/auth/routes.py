from flask import (redirect, render_template, url_for, g, current_app,
                   request, flash)
from flask_login import (current_user, login_user, logout_user)

from app.auth import bp
from app.auth.forms import (LoginForm, RegisterForm)
from app.models import (User)
from app import db

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('groups.groups'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        username = username.lower()
        password = form.password.data
        remember_me = form.remember_me.data
        user = None
        users = User.query.all()
        for u in users:
            if u.username.lower() == username or u.email.lower() == username:
                user = u
        if user is None or not user.check_password(password):
            flash('Invalid Username/Email or Password')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember_me)
        next_page = request.args.get('next') or url_for('main.index')
        return redirect(next_page)

    return render_template('auth/login.html', a='l', title='Login',
                           form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('groups.groups'))
        
    form = RegisterForm()
    if form.validate_on_submit():
        fullname = form.fullname.data
        gender = form.gender.data
        username = form.username.data
        email = form.email.data
        password = form.password.data

        user = User(fullname=fullname, gender=gender, username=username,
                    email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('User Account Created! Please Login to Continue.')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title='Register',
                           a='r', form=form)

@bp.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('auth.login'))
