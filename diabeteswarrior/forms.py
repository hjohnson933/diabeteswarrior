"""Diabetes Warrior Forms"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class Register(FlaskForm):
    username = StringField('Username', validators=[DataRequired('A user name is required!'), Length(min=2, max=32, message='The username must be between 2 and 32 characters long.')])

    email = StringField('Email', validators=[DataRequired('A valid email address is required!'), Email()])

    password = PasswordField('Password', validators=[DataRequired('You must provide a valid password!'), Length(min=8, max=32, message='The password must between 8 and 32 characters long.')])

    confirm = PasswordField('Confirm your Password', validators=[DataRequired('You must provide a valid password!'), Length(min=8, max=32, message='The password must between 8 and 32 characters long.'), EqualTo('password', message='The text entered does not match the password you entered!')])

    submit = SubmitField('Register')


class Login(FlaskForm):
    username = StringField('Username', validators=[DataRequired('A user name is required!'), Length(min=2, max=32, message='The username must be between 2 and 32 characters long.')])

    email = StringField('Email', validators=[DataRequired('A valid email address is required!'), Email()])

    password = PasswordField('Password', validators=[DataRequired('You must provide a valid password!'), Length(min=8, max=32, message='The password must between 8 and 32 characters long.')])

    remember = BooleanField('Remembered')

    submit = SubmitField('Login')


class Health(FlaskForm):
    ...


class Meal(FlaskForm):
    ...


class Food(FlaskForm):
    ...


class Scan(FlaskForm):
    ...


class Targets(FlaskForm):
    ...
