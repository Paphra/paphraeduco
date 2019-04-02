from flask_wtf import FlaskForm

class GroupSearchForm(FlaskForm):
    search = StringField()
