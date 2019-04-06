from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class GroupPostForm(FlaskForm):
    post = StringField('Say Something', validators=[DataRequired()])
    submit = SubmitField('Post')
