from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class MainSearchForm(FlaskForm):
    search = StringField('', validators=[DataRequired()],
                         render_kw={'placeholder': 'Search ...'})
    search_btn = SubmitField('Search')
