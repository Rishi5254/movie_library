from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired,  Length
from wtforms.fields import EmailField

# WTForm


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Passowrd', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=50, message='min and max is 3-50')])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20, message='Password limit 8-20 letters')])
    submit = SubmitField('Register')


class SearchForm(FlaskForm):
    movie_name = StringField(validators=[DataRequired()])
    submit = SubmitField('Search')