from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField,
                     BooleanField, SelectField)
from wtforms.validators import (DataRequired, Length, Email, EqualTo)


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
                         choices=[(1, 'Male'), (2, 'Female'),
                                  (3, 'Others')])
    username = StringField('Username',
                           render_kw={'placeholder': 'Paphra'},
                           validators=[DataRequired(), Length(min=4, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Choose a Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password',
                              validators=[DataRequired(),
                                          EqualTo('password')])
    register = SubmitField('Register')
