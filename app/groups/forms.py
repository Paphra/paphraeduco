from flask_wtf import FlaskForm
from flask_uploads import UploadSet, DOCUMENTS
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError

from app.models import Group, Post


class GroupPostForm(FlaskForm):
    topic = StringField('Topic', validators=[DataRequired()])
    body = TextAreaField('Post Body', validators=[DataRequired()],
                         render_kw={'rows': 4})
    attachment = FileField('Attachment', validators=[
        FileAllowed([
            'doc', 'docx', 'xlsx', 'xls', 'pdf', 'ppt', 'pptx', 'accdb', 'db',
            'vb', 'py', 'txt', 'java', 'cpp', 'cp', 'sav'], 'Documents Only')
    ])
    submit = SubmitField('Post')


class CreateGroupForm(FlaskForm):
    name = StringField('Name of the Group', validators=[DataRequired()],
                       render_kw={'placeholder': 'Group 1'})
    course_code = StringField('Course Code', validators=[DataRequired()],
                              render_kw={'placeholder': 'IDSK1101'})
    course_name = StringField(
        'Course Name', validators=[DataRequired()],
        render_kw={'placeholder': 'School and Society'})
    create = SubmitField('Create')


    def validate_name(self, name):
        n = self.name.data
        cn = self.course_name.data
        cd = self.course_code.data
        groups1 = Group.query.filter_by(
            name=n, course_code=cd).count()
        groups2 = Group.query.filter_by(
            name=n, course_name=cn).count()
        if groups1 or groups2:
            raise ValidationError('Group already Exists!')
        if 'group' not in n.lower():
            raise ValidationError("Group name must contain the word 'Group'")
