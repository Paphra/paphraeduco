from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField,
                     BooleanField, SelectField)
from wtforms.validators import (DataRequired, Length, Email, EqualTo,
                                ValidationError)

from app.models import (User)


class LoginForm(FlaskForm):
    username = StringField('Username/Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    login = SubmitField('Login')


class RegisterForm(FlaskForm):
    fullname = StringField('Full Name',
                           render_kw={'placeholder': 'John Smith'},
                           validators=[DataRequired(), Length(min=6, max=30)])
    gender = SelectField('Gender', validators=[DataRequired()],
                         choices=[('Male', 'Male'), ('Female', 'Female'),
                                  ('Others', 'Others')])
    username = StringField('Username',
                           render_kw={'placeholder': 'Paphra'},
                           validators=[DataRequired(), Length(min=4, max=15)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Create a Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password',
                              validators=[DataRequired(),
                                          EqualTo('password')])
    register = SubmitField('Register')

    def validate_username(self, username):
        user = None
        users = User.query.all()
        for u in users:
            if u.username.lower() == username.data.lower():
                user = u

        if user is not None:
            raise ValidationError('Username Already Taken!')

    def validate_email(self, email):
        user = None
        users = User.query.all()
        for u in users:
            if u.email.lower() == email.data.lower():
                user = u

        if user is not None:
            raise ValidationError('An Account with this Email Address'
                                  'already exits!')
