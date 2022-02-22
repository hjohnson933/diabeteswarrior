from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Username is required!')])
    password = PasswordField('Password', validators=[DataRequired('Password is required!')])
    submit = SubmitField('Login')
    remember_me = BooleanField('Remember Me')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Username is required!')])
    password = PasswordField('Password', validators=[DataRequired('Password is required!')])
    submit = SubmitField('Register')
