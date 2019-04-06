import os

from flask import (render_template, redirect, url_for, send_from_directory,
                   g, current_app, flash)
from flask_login import (current_user)
from app.main import bp
from app.main.forms import MainSearchForm


@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(current_app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')

@bp.route('/index')
@bp.route('/')
def index():

    search_form = MainSearchForm()
    posts = [
        {
            'author': 'Paphra',
            'group': {
                'name': 'Group 1',
                'id': 1,
                'course': 'IDSK1201'
            },
            'timestamp': '2019020320',
            'topic': 'Anouncement 1',
            'body': 'Major announcement 1',
            'attachment': 'attachment 1',
            'attachment_link': '/attachments/1',
            '_link': '/posts/1'
        },
        {
            'author': 'James',
            'group': {
                'name': 'Group 4',
                'id': 3,
                'course': 'IDSK1201'
            },
            'timestamp': '2019020320',
            'topic': 'Anouncement 2',
            'body': 'Major announcement 2',
            'attachment': 'attachment 1',
            'attachment_link': '/attachments/1',
            '_link': '/posts/2'
        }

    ]
    flash('Welcome to pEduco!')
    return render_template('index.html', posts=posts, a='i', title='Home',
                           search_form=search_form)
