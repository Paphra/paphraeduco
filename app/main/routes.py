import os

from flask import (render_template, redirect, url_for, send_from_directory,
                   g)
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
            'id': 1,
            '_link': url_for('faculties.faculties', id=1)
        },
        {
            'name': 'Business and ICT',
            'id': 2,
            '_link': url_for('faculties.faculties', id=2)
        },
        {
            'name': 'Biomedical',
            'id': 3,
            '_link': url_for('faculties.faculties', id=3)
        }
    ]

    posts = [
        {
            'author': 'Univeristy',
            'faculty': 'Education',
            'timestamp': '2019020320',
            'topic': 'Anouncement 1',
            'short_description': 'Major announcement 1',
            '_link': '/faculties/2/posts/1'
        },
        {
            'author': 'Lecturer',
            'faculty': 'Education',
            'timestamp': '2019020320',
            'topic': 'Anouncement 2',
            'short_description': 'Major announcement 2',
            '_link': '/faculties/3/posts/1'
        }

    ]
    return render_template('index.html', posts=posts, faculties=faculties,
                           a='i', title='Home')
