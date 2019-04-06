from flask import (redirect, render_template, url_for, g, current_app,
                   request, flash)
from flask_login import (current_user, login_user)
from app.auth import bp
from app.auth.forms import LoginForm

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
