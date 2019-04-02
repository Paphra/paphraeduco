import os

from flask import (render_template, redirect, url_for, send_from_directory)
from app.main import bp


@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')

@bp.route('/index')
@bp.route('/')
def index():
    faculties = [
        {
            'name': 'Education',
            '_link': '/facaulties/education'
        },
        {
            'name': 'Business and ICT',
            '_link': '/facaulties/bit'
        },
        {
            'name': 'Biomedical',
            '_link': '/facaulties/biomedical'
        }
    ]
    posts = [
        {
            'author': 'Univeristy',
            'faculty': 'Education',
            'timestamp': '2019020320',
            'topic': 'Anouncement 1',
            'short_description': 'Major announcement 1',
            '_link': '/faculties/education/posts/1'
        },
        {
            'author': 'Univeristy',
            'faculty': 'Education',
            'timestamp': '2019020320',
            'topic': 'Anouncement 2',
            'short_description': 'Major announcement 2',
            '_link': '/faculties/education/posts/1'
        }

    ]
    return render_template('index.html', faculties=faculties, posts=posts)
