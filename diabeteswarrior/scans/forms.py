import arrow as Arrow
from flask_wtf import FlaskForm
from wtforms import BooleanField, DecimalField, IntegerField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class ScanForm(FlaskForm):
    title = StringField('Title', default=Arrow.now().format('YYYY-MM-DD HH'))
    message = IntegerField('Message', default=0)
    glucose = IntegerField('Glucose', validators=[DataRequired('A glucose value is required.')])
    trend = IntegerField('Trend', default=0)
    notes = TextAreaField('notes')
    bolus = BooleanField('Bolus', default=False)
    bolus_u = IntegerField('Bolus', default=0)
    basal = BooleanField('Basal', default=False)
    basal_u = IntegerField('Basal', default=0)
    food = BooleanField('Food', default=False)
    food_u = IntegerField('Carbohydrates', default=0)
    medication = BooleanField('Medication', default=False)
    exercise = BooleanField('Exercise', default=False)
    submit = SubmitField('Health Record')
