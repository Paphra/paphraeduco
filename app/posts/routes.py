import os

from flask import (render_template, redirect, url_for, current_app,
                   send_file, flash)
from flask_login import (login_required, current_user)

from app import db
from app.posts import bp
from app.models import Group, Post
import config


@bp.route('/groups/<int:group_id>/posts/<int:post_id>/publish')
@login_required
def publish_post(group_id, post_id):
    group = Group.query.get_or_404(group_id)
    post = Post.query.get_or_404(post_id)

    if not group.is_admin(current_user):
        flash('You are not allowed to publish this post!')
        return redirect(url_for('groups.get_group', id=group_id))

    if post.is_published():
        post.unpublish()
        flash('The Post is Unpublished!')
    else:
        post.publish()
        flash('The Post is Published!')
    db.session.commit()

    return redirect(url_for('groups.get_group', id=group_id))


@bp.route('/groups/<int:group_id>/posts/<int:post_id>/attachment')
@login_required
def get_attachment(group_id, post_id):
    group = Group.query.get_or_404(group_id)
    post = Post.query.get_or_404(post_id)

    if not group.is_member(current_user) and not post.published:
        flash('You are not allowed to access this attachment')
        return redirect(url_for('groups.groups'))

    try:
        return send_file(
            os.path.join(config.basedir, 'app\\posts\\attachments', post.attachment),
            attachment_filename=post.attachment)
    except Exception as e:
        return str(e)
