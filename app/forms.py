"""Create the forms used by the Flask server."""
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, IntegerField, DecimalField, TextAreaField, RadioField  # , SelectField
from wtforms.validators import DataRequired, NumberRange, Length, Email, EqualTo


class LoginForm(FlaskForm):
    """Create the class with the login data.

        Attributes:
        -----------
        email: str
            The email address you registered with.
        password: str
            Your password.
        submit: bool
            Triggers the application to verify your credentials and allow access to your information.
    """

    email = StringField('Email', validators=[DataRequired('You must provide your email address.')])
    password = PasswordField('Password', validators=[DataRequired('You must provide your password.')])
    submit = SubmitField('Login')
    remember_me = BooleanField('Remember Me')


class RegistrationForm(FlaskForm):
    """Create the class with the registration data.

        Attributes:
        -----------
        username: str
            The name you would like application to call you.
        password: str
            The password or phrase you want to use for identification.
        confirm: str
            Verify you entered the password or phrase correctly.
        email: str
            The email address you want notifications sent to, you don't have to enter a real email address
            be aware that if you don't you cannot change your password.
        submit: bool
            Triggers the application to store the data in the data base and send you to the next page.
    """

    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=32, message='Username is required! and must be between 3 and 32 characters long')])
    password = PasswordField('Password', validators=[DataRequired('Password is required!')])
    confirm = PasswordField('Confirm Password', validators=[DataRequired('Password is required!'), EqualTo('password')])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(min=6, max=128, message='Email address is required! and must be between 6 and 128 characters long')])
    submit = SubmitField('Register')


class TargetForm(FlaskForm):
    """User Target Data

        Attributes:
        -----------
        chart_min: int
            Bottom edge of the chart, also the minimum value I found for life
        chart_max: int
            Top edge of the chart, also the maximum value I found for life
        limit_min: int
            The minimum acceptable blood glucose value
        limit_max: int
            The maximum acceptable blood glucose value
        target_min: int
            The minimum ideal blood glucose
        target_max: int
            The maximum ideal blood glucose
        my_target_min: int
            my fasting lower target
        my_target_max: int
            my fasting upper target
        meal_ideal: int
            The ideal value after a meal
        meal_good: int
            A value that is OK every once in a while.
        meal_bad: int
            A value that you should never execede
        my_target_weight: float
            The weight I would like to matain
        my_target_bmi: float
            The body mass index I would like to matain
        submit: bool
            Triggers the application to store the data in the data base and send you to the next page.
    """

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
    submit = SubmitField('Save Targets')


class ScanForm(FlaskForm):
    """User Scan Data

        Attributes:
        -----------
        message: int
            Index of the current message from the Freestyle reader
        notes: str
            Additional notes you would like to add to the record
        glucose: int
            Current glucose value
        trend: int
            Index of the current glucose trend from the Freestyle reader
        bolus_u: int
            The amount of insulin you have taken for this scan
        basal_u: int
            The amount of basal insulin you have taken for this scan
        carbohydrates: int
            The number of carbohydrates you have ingested for this scan
        medication: bool
            Set to true if you have taken medication for this scan
        exercise: bool
            Set to true if you have exercised for this scan
        submit: bool
            Triggers the application to store the data in the data base and send you to the next page.
    """

    message = RadioField('Message', choices=[(3, 'Glucose High'), (2, 'Glucose Going High'), (1, 'My High Glucose Alert'), (0, 'None'), (-1, 'My Low Glucose Alert'), (-2, 'Glucose Going Low'), (-3, 'Glucose Low')], default=0)
    notes = TextAreaField('Notes')
    glucose = IntegerField('Glucose', validators=[DataRequired('A glucose value is required.')])
    trend = RadioField('Trend', choices=[(2, 'Up'), (1, 'Up and right'), (0, 'Right'), (-1, 'Down and right'), (2, 'Down')], default=0)
    bolus_u = IntegerField('Amount of bolus insulin taken', default=0)
    basal_u = IntegerField('Amount of basal insulin taken', default=0)
    carbohydrates = IntegerField('Carbohydrates', default=0)
    medication = BooleanField('Medication')
    exercise = BooleanField('Execrise')
    submit = SubmitField('Save Scan')
