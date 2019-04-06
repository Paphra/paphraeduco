from flask import (redirect, render_template, url_for, g, current_app,
                   request, flash)
from flask_login import (current_user, login_user)
from app.auth import bp
from app.auth.forms import (LoginForm, RegisterForm)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user = {
        'username': 'paphra',
        'password': '7374'
    }
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember_me = int(form.remember_me.data)

        next_page = request.args.get('next') or url_for('main.index')
        if username != user['username'] or password != user['password']:
            flash('Invalid Username or Password')
            redirect(url_for('auth.login'))

        login_user(user, remember=remember_me)
        return redirect(next_page)


    return render_template('auth/login.html', a='l', title='Login',
                           form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        fullname = form.fullname.data
        gender = form.gender.data
        username = form.username.data
        email = form.email.data
        password = form.password.data

        return redirect(url_for('groups.groups'))

    return render_template('auth/register.html', title='Register',
                           a='r', form=form)
