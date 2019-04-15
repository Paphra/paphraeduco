from flask import (render_template, redirect, url_for, request,
                   current_app)
from flask_login import (login_required, current_user)
from app.users import bp
from app.models import User, Post


@bp.route('/users')
@login_required
def users():
    pass

@bp.route('/profile')
@login_required
def profile():

    user = User.query.get_or_404(current_user.id)
    groups = user.get_groups()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['POSTS_PER_PAGE']
    posts = user.posts.order_by(Post.timestamp.desc()
                                ).paginate(page, per_page, False)

    next = url_for(
        'users.profile', page=posts.next_num) if posts.has_next else None
    prev = url_for(
        'users.profile', page=posts.prev_num) if posts.has_prev else None


    return render_template('users/profile.html', next=next, prev=prev, a='p',
                           posts=posts.items, groups=groups,
                           title=user.username, name=user.username)


@bp.route('/users/<int:id>')
@login_required
def get_user(id):
    user = User.query.get_or_404(id)
    if current_user == user:
        return redirect(url_for('users.profile'))

    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['POSTS_PER_PAGE']
    posts = user.posts.order_by(
        Post.timestamp.desc()
        ).filter_by(published=1).paginate(page, per_page, False)
    next = url_for(
        'users.get_user', page=posts.next_num) if posts.has_next else None
    prev = url_for(
        'users.get_user', page=posts.prev_num) if posts.has_prev else None
    groups = user.get_groups()

    return render_template('users/user.html', title='User', a='p', user=user,
                           next=next, prev=prev, posts=posts.items,
                           groups=groups, name=user.username)

@bp.route('/users/<int:id>/edit')
@login_required
def edit_user(id):
    pass

@bp.route('/users/<int:id>/change_password', methods=['GET', 'POST'])
def change_password(id):
    pass
