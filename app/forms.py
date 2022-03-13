"""Create the forms used by the Flask server."""
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, IntegerField, DecimalField, EmailField
from wtforms.validators import DataRequired, NumberRange, Email


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

    username = StringField('Username', validators=[DataRequired('Username is required!')])
    password = PasswordField('Password', validators=[DataRequired('Password is required!')])
    email = EmailField('Email Address', validators=[DataRequired('Email address is required!'), Email()])
    chart_min = IntegerField('Lowest Chart Value', default=40, validators=[NumberRange(min=10, max=2656)])
    chart_max = IntegerField('Highest Chart Value', default=400, validators=[NumberRange(min=10, max=2656)])
    limit_min = IntegerField('Lowest Acceptable Value', default=55, validators=[NumberRange(min=21, max=70)])
    limit_max = IntegerField('Highest Acceptable Value', default=250, validators=[NumberRange(min=180, max=250)])
    target_min = IntegerField('Lower Target Value', default=70)
    target_max = IntegerField('Upper Target Value', default=180)
    my_target_min = IntegerField('My Lower Fasting Target Value', validators=[NumberRange(min=70, max=180)])
    my_target_max = IntegerField('My Upper Fasting Target Value', validators=[NumberRange(min=70, max=180)])
    meal_ideal = IntegerField('IDEAL Postprandial Glucose', default=180)
    meal_good = IntegerField('OK Postprandial Glucose', default=250)
    meal_bad = IntegerField('BAD Postprandial Glucose', default=270)
    my_target_weight = DecimalField('Your Target Weight')
    my_target_bmi = DecimalField('Your Target Body Mass Index')
    submit = SubmitField('Register')
