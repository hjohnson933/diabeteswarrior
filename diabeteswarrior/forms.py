"""Diabetes Warrior Forms"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20, message="Username must be between 2 and 20 characters!")])

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired(),])

    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired(),])

    remembered = BooleanField('Remembered')

    submit = SubmitField('Submit')


class BglForm(FlaskForm):
    chart_min = IntegerField('Chart Minimin', validators=[DataRequired(), NumberRange(min=0, max=600, message='Chart Ranges should match the lower limit of your device, 40 for the Libre2.')])

    chart_max = IntegerField('Chart Maximum', validators=[DataRequired(), NumberRange(min=0, max=600, message='Chart Ranges should match the upper limit of your device, 400 for the libre2.')])

    limit_min = IntegerField('Lower BGL limit', validators=[DataRequired(), NumberRange(min=55, max=250, message='Very Low Range from the International Consensus on Time in Range.')])

    limit_max = IntegerField('Upper BGL Limit', validators=[DataRequired(), NumberRange(min=55, max=250, message="Very High Range from the International Consensus on Time in Range.")])

    target_min = IntegerField('Lower BGL Target', validators=[DataRequired(), NumberRange(min=70, max=180, message="Clinical targets from the International Consensus on Time in Range.")])

    target_max = IntegerField('Lower BGL Target', validators=[DataRequired(), NumberRange(min=70, max=180, message="Clinical targets from the International Consensus on Time in Range.")])

    my_min = IntegerField('My Lower BGL Target', validators=[NumberRange(min=55, max=251, message="My personal target range.")])

    my_max = IntegerField('My Upper BGL Target', validators=[NumberRange(min=55, max=251, message="My personal target range.")])

    meal_ideal = IntegerField('Ideal Postprandial')

    meal_good = IntegerField('Max Postprandial')

    meal_bad = IntegerField('Never Exceed Postprandial')


class FoodForm(FlaskForm):
    domain = StringField('Domain', validators=[DataRequired(), Length(min=3, max=128, message="Domain must be between 3 and 128 characters.")])

    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=128, message="Title must be between 3 and 128 characters.")])

    portion = StringField('Portion', validators=[DataRequired(), Length(min=1, max=25, message="portion must be 1 and 25 characters.")])

    unit = StringField('Unit', validators=[DataRequired(), Length(min=1, max=25, message="unit must be 1 and 25 characters.")])

    calories = IntegerField('Calories', validators=[DataRequired(message="Calories must have a value even if it is 0.")])

    fat = IntegerField('Fat', validators=[DataRequired(message="Fat must have a value even if it is 0.")])

    cholesterol = IntegerField('Cholesterol', validators=[DataRequired(message="Cholesterol must have a value even if it is 0.")])

    sodium = IntegerField('Sodium', validators=[DataRequired(message='Sodium must have a value even if it is 0.')])

    carbohydrate = IntegerField('Carbohydrate', validators=[DataRequired(message="Carbohydrate must hav a value even if it is 0.")])

    protein = IntegerField('Protein', validators=[DataRequired(message="Protein must have a value even if it is 0.")])


class HealthForm(FlaskForm):
    po_pulse = IntegerField('Pulse', validators=[DataRequired(message="Heart rate is required.")])

    po_ox = IntegerField('Oxygen', validators=[DataRequired(message="Oxygen saturation is required.")])

    wgt = DecimalField('Weight', validators=[DataRequired(message="Your weight is required.")])

    fat = DecimalField('Body Mass Index')

    bp_pulse = IntegerField('Pulse', validators=[DataRequired(message="Heart rate from the blood pressure cuff is also required.")])

    bp_systolic = IntegerField('Systolic Pressure', validators=[DataRequired(message="Systolic pressure is required.")])

    bp_diastolic = IntegerField('Diastolic Pressure', validators=[DataRequired(message="Diastolic pressure is required.")])

    bp_ihb =  BooleanField('Irregular Heart Beat')

    bp_hypertension = IntegerField('Hypertension', validators=[DataRequired(message="Hypertension is required even if it is 0."), NumberRange(min=0, max=3, message="Hypertension must be in the range of 0 to 3.")])

    temperature = DecimalField('Temperature', validators=[DataRequired(message="Your body temperature is required.")])


class MealsForm(FlaskForm):
    servings = StringField('Servings')

    indices = StringField('Indices')


class ScanForm(FlaskForm):
    msg = IntegerField('Message', validators=[DataRequired(message="The Reader message is required."), NumberRange(min=-3, max=3, message="Message must be in the range of -3 to 3.")])

    glucose = IntegerField('Glucose', validators=[DataRequired(message="A glucose value is required.")])

    trend = IntegerField('Glucose Trend', validators=[DataRequired(message="A glucose trend is required."), NumberRange(min=-2, max=2, message="Trend must be in the range of -2 to 2.")])

    bolus_u = IntegerField('Bolus Insulin')

    basal_u = IntegerField('Basal Insulin')

    carbohydrate = IntegerField('Carbohydrate')

    notes = StringField('Notes')

    exercise = BooleanField('Exercise')

    medication = BooleanField('Medication')
