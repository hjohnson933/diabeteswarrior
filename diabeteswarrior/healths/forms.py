import arrow as Arrow
from flask_wtf import FlaskForm
from wtforms import BooleanField, DecimalField, IntegerField, SelectField, StringField, SubmitField


class HealthForm(FlaskForm):
    title = StringField('Title', default=Arrow.now().format('YYYY-MM-DD HH'))
    po_pulse = IntegerField('Pulse form pulseoximeter')
    po_ox = IntegerField('Oxygen')
    weight = DecimalField('Weight')
    fat = DecimalField('Fat')
    bp_pulse = IntegerField('Pulse from BP cuff')
    bp_systolic = IntegerField('Systolic Pressure')
    bp_diastolic = IntegerField('Diastolic Pressure')
    bp_ihb = BooleanField('Irregular Heart Beat', default=False)
    bp_hypertension = SelectField('Hypertension Stage', choices=[('0','No'),('1','pre'),('2','Stage I'),('3','Stage II')], coerce=int)
    temperature = DecimalField('Temperature')
    submit = SubmitField('Health Record')
