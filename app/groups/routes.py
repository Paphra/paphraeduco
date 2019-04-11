import os

from flask import (render_template, redirect, url_for, current_app,
                   flash, request)
from flask_login import (current_user, login_required)
from werkzeug.utils import secure_filename

from app.groups import bp
from app.groups.forms import (GroupPostForm, CreateGroupForm,
                              GroupAddNewMemberForm)
from app.main.forms import MainSearchForm
from app.models import User, Group, Post
from app import db
import config


@bp.route('/groups')
@login_required
def groups():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['GROUPS_PER_PAGE']
    groups = current_user.get_groups().paginate(
        page, per_page, False)

    prev = url_for(
        'groups.groups', page=groups.prev_num) if groups.has_prev else None
    next = url_for(
        'groups.groups', page=groups.next_num) if groups.has_next else None
    if not groups.items:
        flash('You do not belong to any Group!')

    return render_template('groups/groups.html', a='g', groups=groups.items,
                           title='Groups', prev=prev, next=next)

@bp.route('/groups/<int:id>', methods=['GET', 'POST'])
@login_required
def get_group(id):
    group = Group.query.get_or_404(id)
    if not group.is_member(current_user):
        flash('You are not a member of {}'.format(group.name))
        return redirect(url_for('groups.groups'))
    if not group.posts.count():
        flash('There are no Posts in this Group')

    search_form = MainSearchForm()
    form = GroupPostForm()

    search_results = []
    if search_form.validate_on_submit():
        txt = search_form.search.data.lower()
        posts = Post.query.filter_by(group=group).order_by(
            Post.timestamp.desc())

        def return_back():
            return redirect(url_for('main.index'))

        if not posts:
            flash('Sorry, there are no Posts in this Group!')
            return return_back()

        for post in posts:
            if txt in (post.topic + post.body + post.author.username + \
                       post.author.fullname + post.group.name + \
                       post.group.course_name + post.group.course_code
                       ).lower():
                search_results.append(post)

        flash('{} result(s) found!'.format(len(search_results)))

    elif form.validate_on_submit():
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

    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['POSTS_PER_PAGE']
    posts = group.posts.order_by(
        Post.timestamp.desc()).paginate(page, per_page, False)

    next = url_for(
        'groups.get_group', id=id,
        page=posts.next_num) if posts.has_next else None
    prev = url_for(
        'groups.get_group', id=id,
        page=posts.prev_num) if posts.has_prev else None
    title = group.name + '-' + group.course_code

    return render_template('groups/group.html', a='g', group=group,
                           title=title, posts=posts.items, form=form,
                           prev=prev, next=next, search_form=search_form,
                           search_results=search_results)

@bp.route('/groups/create', methods=['GET', 'POST'])
@login_required
def create_group():
    no_groups = current_user.groups_created.count()
    if no_groups > 3:
        flash('You have reached the Maximum number of Groups you can'
              'create!')
        return redirect(url_for('groups.groups'))

    create_group_form = CreateGroupForm()
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
                           a='g', form=create_group_form)

@bp.route('/groups/<int:id>/members', methods=['GET', 'POST'])
@login_required
def get_members(id):
    search_form = MainSearchForm()
    add_form = GroupAddNewMemberForm()
    group = Group.query.get_or_404(id)
    if not group.is_member(current_user):
        flash('You do not belong to {} of {}!'.format(group.name,
                                                      group.course_code))
        return redirect(url_for('groups.groups'))
    members = group.get_members()
    users_search_results = []

    if search_form.validate_on_submit():
        txt = search_form.search.data.lower()
        users = User.query.all()
        for user in users:
            if txt in (user.username.lower() or user.email.lower() or \
                  user.fullname.lower()):
                users_search_results.append(user)

        flash('{} users found!'.format(str(len(users_search_results))))

    elif add_form.validate_on_submit():
        fullname = add_form.fullname.data
        email = add_form.email.data
        username = email.split('@')[0]
        gender = add_form.gender.data
        password = add_form.password.data

        i = 2
        while True:
            user = User.query.filter_by(username=username).first()
            if user is not None:
                username += '00' + str(i)
                i += 1
                continue
            break

        user = User(username=username, gender=gender, fullname=fullname,
                    email=email)
        user.set_password(password)
        db.session.add(user)
        group.add(user)
        db.session.commit()
        flash('New User has been Added!')

        return redirect(url_for('groups.get_members', id=id))

    if not group.is_admin(current_user):
        add_form = None
        search_form = None

    return render_template('groups/members.html', a='g',
                           members=members, search_form=search_form,
                           add_form=add_form, group=group,
                           title=group.name + '-' + group.course_code,
                           search_results=users_search_results)


@bp.route('/groups/<int:group_id>/members/<int:member_id>/remove')
@login_required
def remove_member(group_id, member_id):
    group = Group.query.get_or_404(group_id)
    member = group.get_members().filter_by(id=member_id).first()
    if member is None:
        return render_template('errors/404.html'), 404

    def redirect_back():
        return redirect(url_for('groups.get_members', id=group_id))

    if member == group.admin:
        flash('Admin can not be removed!')
        return redirect_back()

    group.remove(member)
    db.session.commit()
    flash('{} removed from the Group!'.format(member.username))

    return redirect_back()


@bp.route('/groups/<int:group_id>/members/<int:user_id>/add')
@login_required
def add_member(group_id, user_id):
    group = Group.query.get_or_404(group_id)
    user = group.get_members().filter_by(id=user_id).first()

    def redirect_back():
        return redirect(url_for('groups.get_members', id=group_id))

    if user is not None:
        flash('User is already a member')
        return redirect_back()

    user = User.query.get_or_404(user_id)

    group.add(user)
    db.session.commit()
    flash('{} is added to the Group!'.format(user.username))

    return redirect_back()
