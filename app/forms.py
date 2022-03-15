"""Create the forms used by the Flask server."""
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, IntegerField, DecimalField
from wtforms.validators import DataRequired, NumberRange, Length, Email, EqualTo


class LoginForm(FlaskForm):
    """Create the class with the login data.

    Args:
        FlaskForm (object): Forms base class.
    """

    username = StringField('Username', validators=[DataRequired('You must provide your username.')])
    email = StringField('Email', validators=[DataRequired('You must provide your email address.')])
    password = PasswordField('Password', validators=[DataRequired('You must provide your password.')])
    submit = SubmitField('Login')
    remember_me = BooleanField('Remember Me')


class RegistrationForm(FlaskForm):
    """Create the class with the registration data.

    Args:
        FlaskForm (object): Forms base class.

    @param chart_min Bottom edge of the chart, also the minimum value I found for life
    @param chart_max Top edge of the chart, also the maximum value I found for life
    @param limit_min The minimum acceptable blood glucose value
    @param limit_max The maximum acceptable blood glucose value
    @param target_min The minimum ideal blood glucose
    @param target_max The maximum ideal blood glucose
    @param my_target_min my fasting lower target
    @param my_target_max my fasting upper target
    @param meal_ideal The ideal value after a meal
    @param meal_good A value that is OK every once in a while.
    @param meal_bad A value that you should never execede
    @param my_target_weight The weight I would like to matain
    @param my_target_bmi The body mass index I would like to matain

    """

    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=32, message='Username is required! and must be between 3 and 32 characters long')])
    password = PasswordField('Password', validators=[DataRequired('Password is required!')])
    confirm = PasswordField('Confirm Password', validators=[DataRequired('Password is required!'), EqualTo('password')])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(min=6, max=128, message='Email address is required! and must be between 6 and 128 characters long')])
    submit = SubmitField('Register')


class AccountForm(FlaskForm):
    """User Target Data"""

    chart_min = IntegerField('Chart Low', default=40, validators=[NumberRange(min=10, max=2656)])
    chart_max = IntegerField('Chart High', default=400, validators=[NumberRange(min=10, max=2656)])
    limit_min = IntegerField('Acceptable Low', default=55, validators=[NumberRange(min=21, max=70)])
    limit_max = IntegerField('Acceptable High', default=250, validators=[NumberRange(min=180, max=250)])
    target_min = IntegerField('Target Low', default=70)
    target_max = IntegerField('Target High', default=180)
    my_target_min = IntegerField('Fasting Target Low', validators=[NumberRange(min=70, max=180)])
    my_target_max = IntegerField('Fasting Target High', validators=[NumberRange(min=70, max=180)])
    meal_ideal = IntegerField('IDEAL Meal Glucose', default=180)
    meal_good = IntegerField('OK Meal Glucose', default=250)
    meal_bad = IntegerField('BAD Meal Glucose', default=270)
    my_target_weight = DecimalField('Target Body Weight')
    my_target_bmi = DecimalField('Target Body Mass Index')
    submit = SubmitField('Register')
