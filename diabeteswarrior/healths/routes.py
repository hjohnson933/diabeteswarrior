import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html
from diabeteswarrior import db, server
from diabeteswarrior.healths.forms import HealthForm
from diabeteswarrior.models import Health
from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required

healths = Blueprint('healths', __name__)

@healths.route('/health')
def home():
    df = pd.DataFrame({"Fruit":["Apples","Oranges","Bananas","Apples","Oranges","Bananas"],"Amount":[4,1,2,2,4,5],"City":["SF","SF","SF","Montreal","Montreal","Montreal"]})

    app = dash.Dash(server=server)

    fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

    app.layout = html.Div(children=[html.H1(children='Hello Dash'),html.Div(children='Dash: A web application framework for your data.'),dcc.Graph(id='example-graph',figure=fig)])

    return render_template('home.html', dashboard=dcc.Graph)

# @healths.route("/health")
# def home():
#     return render_template('healths/home.html')

# @healths.route('/health/new', methods=['GET', 'POST'])
# @login_required
# def new_health():
#     form = HealthForm()
#     if form.validate_on_submit():
#         # pylint: disable=redefined-outer-name
#         health = Health(author=current_user, po_pulse=form.po_pulse.data, po_ox=form.po_ox.data, weight=form.weight.data, fat=form.fat.data, bp_pulse=form.bp_pulse.data, bp_systolic=form.bp_systolic.data, bp_diastolic=form.bp_diastolic.data, bp_ihb=form.bp_ihb.data, bp_hypertension=form.bp_hypertension.data, temperature=form.temperature.data)
#         db.session.add(health)
#         db.session.commit()
#         flash('Your health record has been created!', 'success')
#         return redirect(url_for('healths.home'))
#     return render_template('healths/create_health.html', title='New Health Record', form=form, legend='New Health Record')

# @healths.route('/health/<int:health_id>')
# def health(health_id):
#     # pylint: disable=redefined-outer-name
#     health = Health.query.get_or_404(health_id)
#     return render_template('healths/health.html', title=health.title, health=health)

# @healths.route('/health/<int:health_id>/update', methods=['GET', 'POST'])
# @login_required
# def update_health(health_id):
#     # pylint: disable=redefined-outer-name
#     health = Health.query.get_or_404(health_id)
#     if health.author != current_user:
#         abort(403)
#     form = HealthForm()
#     if form.validate_on_submit():
#         health.title = form.title.data
#         health.po_pulse = form.po_pulse.data
#         health.po_ox = form.po_ox.data
#         health.weight = form.weight.data
#         health.fat = form.fat.data
#         health.bp_pulse = form.bp_pulse.data
#         health.bp_systolic = form.bp_systolic.data
#         health.bp_diastolic = form.bp_diastolic.data
#         health.bp_ihb = form.bp_ihb.data
#         health.bp_hypertension = form.bp_hypertension.data
#         health.temperature = form.temperature.data
#         db.session.commit()
#         flash('Your health record has been updated!', 'success')
#     elif request.method == 'GET':
#         form.title.data = health.title
#         form.po_pulse.data = health.po_pulse
#         form.po_ox.data = health.po_ox
#         form.weight.data = health.weight
#         form.fat.data = health.fat
#         form.bp_pulse.data = health.bp_pulse
#         form.bp_systolic.data = health.bp_systolic
#         form.bp_diastolic.data = health.bp_diastolic
#         form.bp_ihb.data = health.bp_ihb
#         form.bp_hypertension.data = health.bp_hypertension
#         form.temperature = health.temperature
#     return render_template('healths/create_health.html', title='Update Post', form=form, legend='Update Post')

# @healths.route('/health/<int:health_id>/delete', methods=['POST'])
# @login_required
# def delete_health(health_id):
#     # pylint: disable=redefined-outer-name
#     health = Health.query.get_or_404(health_id)
#     if health.author != current_user:
#         abort(403)
#     db.session.delete(health)
#     db.session.commit()
#     flash('You health record has been deleted!', 'success')
#     return redirect(url_for('healths.home'))
