from flask import (render_template, redirect, url_for, current_app,
                   flash)
from flask_login import (current_user, login_required)

from app.groups import bp
from app.groups.forms import GroupPostForm
from app.models import User, Group


@bp.route('/groups')
@login_required
def groups():
    groups = current_user.get_groups()
    if not groups:
        flash('You do not belong to any Group!')

    return render_template('groups/groups.html', a='g', groups=groups,
                           title='Groups')

@bp.route('/groups/<int:id>')
@login_required
def get_group(id):

    post_form = GroupPostForm()
    sample = None
    if post_form.validate_on_submit():
        post = post_form.post.data
        sample = post

    group = Group.query.get_or_404(id)
    if not group.is_member(current_user):
        flash('You are not a member of {}'.format(group.name))
        return redirect(url_for('groups.groups'))

    title = group.name + '-' + group.course_code

    return render_template('groups/group.html', a='g', group=group,
                           title=title,
                           form=post_form, sample=sample)
