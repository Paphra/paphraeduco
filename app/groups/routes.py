from flask import (render_template, redirect, url_for, current_app)
from flask_login import (current_user, login_required)
from app.groups import bp
from app.groups.forms import GroupPostForm

@bp.route('/groups')
@login_required
def groups():
    groups = [
        {
            'name': 'Group 1',
            'course': 'IDSK1201',
            'members': 12,
            '_link': url_for('groups.get_group', id=1)
        },
        {
            'name': 'Group 4',
            'course': 'EDU1202',
            'members': 8,
            '_link': url_for('groups.get_group', id=2)
        }
    ]

    return render_template('groups/groups.html', a='g', groups=groups,
                           title='Groups')

@bp.route('/groups/<int:id>')
def get_group(id):

    post_form = GroupPostForm()
    sample = None
    if post_form.validate_on_submit():
        post = post_form.post.data
        sample = post

    group = {
        'name': 'Group 1',
        'course': 'IDSK1201',
        'posts': [
            {
                'id': 0,
                'topic': 'Post 1',
                'body': 'Hello',
                'author': 'User 1',
                'attachment': 'attachment 1',
                'attachment_link': '/attachments/1',
                'timestamp': '2202020202Z'
            },
            {
                'id': 1,
                'topic': 'Post 2',
                'body': 'Again',
                'author': 'User 2',
                'attachment': 'attachment 1',
                'attachment_link': '/attachments/1',
                'timestamp': '2322020202Z'
            }
        ]
    }
    return render_template('groups/group.html', a='g', group=group,
                           title=group['name'] + '-' + group['course'],
                           form=post_form, sample=sample)
