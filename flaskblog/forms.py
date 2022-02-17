from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import BooleanField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from flaskblog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username) -> None:
        user = User.query.filter_by(username=username.data).first()
        if user :
            raise ValidationError(F"Username {username.data} is already in use. Please choose another username.")

    def validate_email(self, email) -> None:
        user = User.query.filter_by(email=email.data).first()
        if user :
            raise ValidationError(F"Email {email.data} is already in use. Please choose another email.")


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username) -> None:
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user :
                raise ValidationError(F"Username {username.data} is already in use. Please choose another username.")

    def validate_email(self, email) -> None:
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user :
                raise ValidationError(F"Email {email.data} is already in use. Please choose another email.")


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
