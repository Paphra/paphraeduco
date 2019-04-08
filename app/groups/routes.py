import os

from flask import (render_template, redirect, url_for, current_app,
                   flash)
from flask_login import (current_user, login_required)
from werkzeug.utils import secure_filename

from app.groups import bp
from app.groups.forms import GroupPostForm, CreateGroupForm
from app.models import User, Group, Post
from app import db
import config


@bp.route('/groups')
@login_required
def groups():
    groups = current_user.get_groups()
    if not groups.all():
        flash('You do not belong to any Group!')

    return render_template('groups/groups.html', a='g', groups=groups,
                           title='Groups')

@bp.route('/groups/<int:id>', methods=['GET', 'POST'])
@login_required
def get_group(id):

    form = GroupPostForm()
    if form.validate_on_submit():
        topic = form.topic.data
        body = form.body.data
        attachment = form.attachment.data
        filename = None
        if attachment is not None:
            filename = secure_filename(attachment.filename)
            location = os.path.join(
                config.basedir, 'app/posts/attachments', filename)
            attachment.save(location)

        post = Post(topic=topic, body=body, posted_by=current_user.id,
                    to_group=id, attachment=filename)
        db.session.add(post)
        db.session.commit()

        flash('Your post is now live!')
        return redirect(url_for('groups.get_group', id=id))

    group = Group.query.get_or_404(id)
    if not group.is_member(current_user):
        flash('You are not a member of {}'.format(group.name))
        return redirect(url_for('groups.groups'))
    if not group.posts.count():
        flash('There are no Posts in this Group')

    posts = group.posts.order_by(Post.timestamp.desc())
    title = group.name + '-' + group.course_code

    return render_template('groups/group.html', a='g', group=group,
                           title=title, posts=posts,
                           form=form)

@bp.route('/groups/create', methods=['GET', 'POST'])
@login_required
def create_group():
    no_groups = current_user.groups_created.count()
    if no_groups > 3:
        flash('You have reached the Maximum number of Groups you can'
              'create!')
        return redirect(url_for('groups.groups'))

    form = CreateGroupForm()
    if form.validate_on_submit():
        name = form.name.data
        code = form.course_code.data
        c_name = form.course_name.data

        group = Group(
            name=name, course_code=code, course_name=c_name,
            created_by=current_user.id)
        db.session.add(group)
        db.session.commit()
        flash('{} of {} is created!'.format(name, code))
        return redirect(url_for('groups.groups'))

    return render_template('groups/create.html', title='Create Group',
                           a='g', form=form)
