import os

from datetime import datetime
from flask import (render_template, redirect, url_for, send_from_directory,
                   g, current_app, flash, request)
from flask_login import (current_user)
from flask_babel import _, get_locale

from app import db
from app.main import bp
from app.main.forms import MainSearchForm
from app.models import Post, Group

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

    g.locale = str(get_locale())


@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(current_app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')

@bp.route('/index', methods=['GET', 'POST'])
@bp.route('/', methods=['GET', 'POST'])
def index():
    search_form = MainSearchForm()
    search_results = []
    if search_form.validate_on_submit():
        txt = search_form.search.data.lower()
        posts = Post.query.filter_by(published=1).order_by(
            Post.timestamp.desc())

        def return_back():
            return redirect(url_for('main.index'))

        if not posts:
            flash('Sorry, there are no Published Posts!')
            return return_back()
        for post in posts:
            if txt in (post.topic + post.body + post.author.username + \
                       post.author.fullname + post.group.name + \
                       post.group.course_name + post.group.course_code
                       ).lower():
                search_results.append(post)

        flash('{} result(s) found!'.format(len(search_results)))

    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['POSTS_PER_PAGE']
    posts = Post.query.filter_by(published=1).order_by(
        Post.timestamp.desc()).paginate(page, per_page, False)

    prev = url_for(
        'main.index', page=posts.prev_num) if posts.has_prev else None
    next = url_for(
        'main.index', page=posts.next_num) if posts.has_next else None
    if not posts:
        flash('No Published posts')

    return render_template('index.html', posts=posts.items, a='i',
                           title='Home', search_form=search_form,
                           next=next, prev=prev,
                           search_results=search_results)
