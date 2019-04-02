import os
from flask import (render_template, url_for, redirect, g,
                   url_for)
from app.faculties import bp


@bp.route('/faculties')
def all_faculties():
    faculties = [
        {
            'name': 'Education',
            'id': 1,
            'info': 'Teaching the future teachers',
            '_link': url_for('faculties.faculties', id=1)
        },
        {
            'name': 'Business and ICT',
            'id': 2,
            'info': 'Educating the future business and IT overloads',
            '_link': url_for('faculties.faculties', id=2)
        },
        {
            'name': 'Biomedical',
            'id': 3,
            'info': 'Equipped to train others in te field of medical practice',
            '_link': url_for('faculties.faculties', id=3)
        }
    ]

    return render_template('faculties/faculties.html', title='Faculties',
                           faculties=faculties, a='f', af=0)


@bp.route('/faculties/<int:id>')
def faculties(id):

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

    faculty = None
    for f in faculties:
        if f['id'] == id:
            faculty = f

    posts = [
        {
            'author': 'Administration',
            'faculty': faculty['name'],
            'timestamp': '2019020320',
            'topic': 'Anouncement 1',
            'short_description': 'Major announcement 1',
            '_link': url_for('faculties.faculty_posts',
                             faculty_id=id, post_id=1)
        },
        {
            'author': 'Univeristy',
            'faculty': faculty['name'],
            'timestamp': '2019020320',
            'topic': 'Anouncement 2',
            'short_description': 'Major announcement 2',
            '_link': url_for('faculties.faculty_posts',
                             faculty_id=id, post_id=2)
        }
    ]

    if id < 1:
        return redirect(url_for('faculties.faculties'))

    return render_template('faculties/faculty.html',
                           faculties=faculties, faculty=faculty,
                           title='Faculty', posts=posts, a='f',
                           af=id)


@bp.route('/faculties/<int:faculty_id>/posts/<int:post_id>')
def faculty_posts(faculty_id, post_id):
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
    faculty = None

    for f in faculties:
        if f['id'] == faculty_id:
            faculty = f
    post = {
        'author': 'Univeristy',
        'faculty': faculty['name'],
        'timestamp': '2019020320',
        'topic': 'Anouncement 1',
        'short_description': 'Major announcement 1',
        'body': 'The main body of the post is to go here after being' \
            'read from the database',
        '_link': url_for('faculties.faculties', id=faculty_id)
    }

    return render_template('faculties/post.html',
                           title='{} Post'.format(faculty['name']),
                           post=post, faculties=faculties, a='f',
                           af=faculty_id)
