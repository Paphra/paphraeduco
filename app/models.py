from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import (generate_password_hash, check_password_hash)

from app import db, login_manager


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


members = db.Table(
    'members',
    db.Column('group_id', db.Integer, db.ForeignKey('group.id')),
    db.Column('member_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(30), index=True)
    gender = db.Column(db.String(10))
    username = db.Column(db.String(15), index=True, unique=True)
    email = db.Column(db.String(100), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(1000))
    date_of_birth = db.Column(db.DateTime)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    register_on = db.Column(db.DateTime, default=datetime.utcnow)

    groups_created = db.relationship(
        'Group', backref='admin',lazy='dynamic',
        foreign_keys='Group.created_by')
    posts = db.relationship(
        'Post', backref='author', lazy='dynamic',
        foreign_keys='Post.posted_by')
    groups = db.relationship(
        'Group', secondary=members,
        primaryjoin=(members.c.member_id == id),
        backref=db.backref('groups', lazy='dynamic'),
        lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_groups(self):
        combination = self.groups.union(Group.query.filter_by(admin=self))
        return combination


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(10), index=True)
    course_name = db.Column(db.String(100), index=True)
    name = db.Column(db.String(10), index=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    members = db.relationship(
        'User', secondary=members,
        primaryjoin=(members.c.group_id == id),
        backref=db.backref('members', lazy='dynamic'),
        lazy='dynamic')

    posts = db.relationship(
        'Post', backref='group', foreign_keys='Post.to_group', lazy='dynamic')

    def __repr__(self):
        return '<Group {}>'.format(self.name)

    def is_member(self, user):
        combination = self.members.union(
            User.query.filter_by(id=self.created_by)).all()
        return user in combination

    def is_admin(self, user):
        return self.created_by == user.id

    def add(self, user):
        if not self.is_member(user):
            self.members.append(user)

    def remove(self, user):
        if self.is_member(user):
            self.members.remove(user)

    def get_members(self):
        combination = self.members.union(
            User.query.filter_by(id=self.created_by))
        return combination

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(100), index=True)
    body = db.Column(db.String(1000), index=True)
    attachment = db.Column(db.String(50))
    posted_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    to_group = db.Column(db.Integer, db.ForeignKey('group.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    published = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Post {}>'.format(self.topic)

    def publish(self):
        self.published = 1

    def is_published(self):
        return self.published > 0

    def unpublish(self):
        self.published = 0
