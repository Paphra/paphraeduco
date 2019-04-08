import os

from datetime import datetime
from flask import (render_template, redirect, url_for, send_from_directory,
                   g, current_app, flash)
from flask_login import (current_user)

from app import db
from app.main import bp
from app.main.forms import MainSearchForm
from app.models import Post, Group


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(current_app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')

@bp.route('/index')
@bp.route('/')
def index():
    if current_user.is_authenticated:
        flash('Hi, {}!'.format(current_user.username))

    search_form = MainSearchForm()

    posts = Post.query.filter_by(published=1).order_by(
        Post.timestamp.desc()).all()
    if not posts:
        flash('No Published posts')

    return render_template('index.html', posts=posts, a='i', title='Home',
                           search_form=search_form)
