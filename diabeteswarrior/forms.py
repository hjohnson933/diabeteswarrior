"""Diabetes Warrior Forms"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange


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
    po_pulse = IntegerField('Pulse from pulseoximeter', validators=[DataRequired('A heart rate is required.')])

    po_ox = IntegerField('Oxygen Saturation', validators=[DataRequired('A oxygen saturation level is required.')])

    wgt = FloatField('Weight', validators=[DataRequired('Weight is required.')])

    fat = FloatField('Body Fat Percentage', validators=[DataRequired('The BMI provided by the Tanita scale is required.')])

    bp_pulse = IntegerField('Blood Pressure Cuff Heart Rate', validators=[DataRequired('A heart rate is required.')])

    bp_systolic = IntegerField('Systolic Blood Pressure', validators=[DataRequired('A systolic blood pressure is required.')])

    bp_diastolic = IntegerField('Diastolic Blood Pressure', validators=[DataRequired('A diastolic blood pressure is required.')])

    bp_ihb = BooleanField('Irregular Heart Beat', default=False)

    bp_hypertension = IntegerField('Hypertension Stage', validators=[NumberRange(min=0, max=3, message='Hypertension stage must be in the range of 0 to 3.')], default=0)


class Meal(FlaskForm):
    servings = TextAreaField('Serving for each food item.')

    indices = TextAreaField('Index for each food item.')


class Food(FlaskForm):
    domain = StringField('Domain', validators=[DataRequired('The distributor or manufacture name.'), Length(max=128, message='The domain should be less than 128 characters.')])

    title = StringField('Name', validators=[DataRequired('The name of the food item is required.'), Length(max=128, message='The name of the food item should be less than 128 characters.')])

    portion = StringField('Portion', validators=[DataRequired('A food item must have a protion.'), Length(max=32, message='The portion description should be less than 32 characters.')])

    unit = StringField('Unit', validators=[DataRequired('A food item must have a unit of measure.'), Length(max=32, message='The unit description should be less than 32 characters.')])

    calories = IntegerField('Calories', validators=[DataRequired('A food must have calories.')])

    fat = IntegerField('Fat', validators=[DataRequired('A food must have a fat value.')])

    cholesterol = IntegerField('cholesterol', validators=[DataRequired('A food must have a cholesterol value.')])

    sodium = IntegerField('Sodium', validators=[DataRequired('A food must have a sodium value.')])

    carbohydrate = IntegerField('Carbohydrate', validators=[DataRequired('A food must have a carbohydrate value.')])

    protein = IntegerField('Protein', validators=[DataRequired('A food must have a protein value.')])


class Scan(FlaskForm):
    msg = IntegerField('Message', validators=[DataRequired('The message displayed on the reader.'), NumberRange(min=-3, max=3, message='Message must be in the range of -3 to 3.')], default=0)

    glucose = IntegerField('Glucose', validators=[DataRequired('A glucose value is required.')])

    trend = IntegerField('Trend', validators=[DataRequired('A trend is required'), NumberRange(min=-2, max=2, message='The trend value must be in the rage of -2 to 2.')], default=0)

    bolus = BooleanField('Bolus Insulin', default=False)

    bolus_u = IntegerField('Bolus Insulin units', default=0)

    basal = BooleanField('Basal Insulin', default=False)

    basal_u = IntegerField('Basal Insulin units', default=0)

    food = BooleanField('Food', default=False)

    carbohydrate = IntegerField('Carbohydrate', default=0)

    exercise = BooleanField('Exercise Event', default=False)

    medication = BooleanField('Medication Event', default=False)

    note = TextAreaField('Note')


class Targets(FlaskForm):
    chart_min = IntegerField('Chart Minimum', validators=[DataRequired('A lower chart limit is required and should match your reader or meter.')], default=40)

    chart_max = IntegerField('Chart Maximum', validators=[DataRequired('A upper chart limit is required and should match your reader or meter.')], default=400)

    limit_min = IntegerField('Lower Safe Limit', validators=[DataRequired('A lower safe limit is required.')],default=55)

    limit_max = IntegerField('Upper Safe Limit', validators=[DataRequired('A upper safe limit is required.')], default=250)

    target_min = IntegerField('Lower Target', validators=[DataRequired('A lower clinical target is required.')], default=70)

    target_max = IntegerField('Upper Target', validators=[DataRequired('A upper clinical target is required.')], default=180)

    my_min = IntegerField('My lower Target')

    my_max = IntegerField('My Upper Targer')

    meal_ideal = IntegerField('Ideal Post Prandial', validators=[DataRequired('A after meal ideal maximum value is required.')], default=180)

    meal_good = IntegerField('Good Post Prandial', validators=[DataRequired('A OK after meal maximum value is required.')], default=250)

    meal_bad = IntegerField('Never Exceed Post Prandial', validators=[DataRequired('A never execeed post prandial value.')], default=270)
