from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, BooleanField, SelectField, DecimalField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    po_pulse = IntegerField('Pulseoximeter Pulse')
    po_ox = IntegerField('Oxygen Saturation')
    weight = DecimalField('Weight')
    fat = DecimalField('Body Mass Index')
    bp_pulse = IntegerField('Blood Pressure Cuff Pulse')
    bp_systolic = IntegerField('Systolic Pressure')
    bp_diastolic = IntegerField('Diastolic Pressure')
    bp_ihb = BooleanField('Irregular Heart Beat')
    bp_hypertension = SelectField('Hypertension Stage')
    temperature = DecimalField('Temperature')
    submit = SubmitField('Health')
