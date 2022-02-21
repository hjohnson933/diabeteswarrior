import arrow as Arrow
from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class ScanForm(FlaskForm):
    title = StringField('Title', default=Arrow.now().format('YYYY-MM-DD HH'))
    message = SelectField('Message', choices=[('-3','Glucose Low'),('-2','Glucose Going Low'),('-1','My Low Glucose Alarm'),('0','None'),('1','My High Glucose Alarm'),('2','Glucose Going High'),('3','Glucose High')], coerce=int)
    glucose = IntegerField('Glucose', validators=[DataRequired('A glucose value is required.')])
    trend = SelectField('Trend', choices=[('-2','The arrow is pointing down.'),('-1','The arrow is pointing down and right.'),('0','The arrow is pointing right.'),('1','The arrow is point up and right.'),('2','The arrow is point up.')], coerce=int)
    notes = TextAreaField('notes')
    bolus = BooleanField('Bolus', default=False)
    bolus_u = IntegerField('Bolus', default=0)
    basal = BooleanField('Basal', default=False)
    basal_u = IntegerField('Basal', default=0)
    food = BooleanField('Food', default=False)
    food_u = IntegerField('Carbohydrates', default=0)
    medication = BooleanField('Medication', default=False)
    exercise = BooleanField('Exercise', default=False)
    lower_limit = IntegerField('Lower Limit', default=-1)
    upper_limit = IntegerField('Upper Limit', default=1)
    submit = SubmitField('Health Record')
