"""Create the forms used by the Flask server."""
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """Create the class with the login data.

    Args:
        FlaskForm (object): Forms base class.
    """

    username = StringField('Username', validators=[DataRequired('Username is required!')])
    password = PasswordField('Password', validators=[DataRequired('Password is required!')])
    submit = SubmitField('Login')
    remember_me = BooleanField('Remember Me')


class RegistrationForm(FlaskForm):
    """Create the class with the registration data.

    Args:
        FlaskForm (object): Forms base class.
    """

    username = StringField('Username', validators=[DataRequired('Username is required!')])
    password = PasswordField('Password', validators=[DataRequired('Password is required!')])
    submit = SubmitField('Register')
