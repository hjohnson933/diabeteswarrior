"""Blueprint for Flask routes."""
import os

import arrow
from flask import Blueprint, flash, redirect, render_template, send_from_directory, url_for  # , request
from flask_login import current_user, login_required, login_user, logout_user

from app.extensions import db
from app.forms import TargetForm, LoginForm, RegistrationForm, ScanForm
from app.models import Targets, Users, Scans

# from werkzeug.urls import url_parse


server_bp = Blueprint('main', __name__)


@server_bp.route('/')
def index() -> str:
    """Home route."""
    return render_template('index.html', title='Home Page')


@server_bp.route('/logout/')
@login_required
def logout() -> object:
    """Logout route."""
    logout_user()

    return redirect(url_for('main.index'))


@server_bp.route('/login/', methods=['GET', 'POST'])
def login() -> object:
    """Login route."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    fields = ['email', 'password']

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            error = 'Invalid email or password'
            return render_template('login.html', error=error, form=form)

        if login_user(user, remember=form.remember_me.data):
            return redirect(url_for('main.index'))

    return render_template('login.html', title='Sign In', form=form, fields=fields)


@server_bp.route('/register/', methods=['GET', 'POST'])
def register() -> object:
    """Route to the registration form."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    fields = ['username', 'email', 'password', 'confirm']

    if form.validate_on_submit():
        user = Users()
        user.username = str(form.username.data)
        user.email = str(form.email.data)
        user.password = user.set_password_hash(password=form.password.data)
        user.account_token = F"{user.username.lower()}_{user.email.lower()}"
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('main.target'))

    return render_template('register.html', title='Register', form=form, fields=fields)


@server_bp.route('/target/', methods=['GET', 'POST'])
@login_required
def target() -> object:

    form = TargetForm()
    fields = ['chart_min', 'chart_max', 'limit_min', 'limit_max', 'target_min', 'target_max', 'my_target_min', 'my_target_max', 'meal_ideal', 'meal_good', 'meal_bad', 'my_target_weight', 'my_target_bmi']

    if form.validate_on_submit():
        target = Targets()
        target.ts = arrow.now().format("YYYY-MM-DD HH:mm")
        target.user_id = current_user.id
        target.chart_min = form.chart_min.data
        target.chart_max = form.chart_max.data
        target.limit_min = form.limit_min.data
        target.limit_max = form.limit_max.data
        target.target_min = form.target_min.data
        target.target_max = form.target_max.data
        target.my_target_min = form.my_target_min.data
        target.my_target_max = form.my_target_max.data
        target.meal_ideal = form.meal_ideal.data
        target.meal_good = form.meal_good.data
        target.meal_bad = form.meal_bad.data
        target.my_target_weight = form.my_target_weight.data
        target.my_target_bmi = form.my_target_bmi.data
        db.session.add(target)
        db.session.commit()
        flash(f'Target data saved for {current_user.username}!', 'success')
        return redirect(url_for('main.index'))

    return render_template('target.html', title='Targets', form=form, fields=fields)


@server_bp.route('/scan/', methods=['GET', 'POST'])
@login_required
def scan() -> object:
    form = ScanForm()
    fields = ['message', 'notes', 'glucose', 'trend', 'bolus_u', 'basal_u', 'carbohydrates', 'medication', 'exercise']

    if form.validate_on_submit():
        scan = Scans()
        scan.bolus = False
        scan.basal = False
        scan.food = False
        scan.lower_limit = -1
        scan.upper_limit = 1
        scan.ts = arrow.now().format("YYYY-MM-DD HH:mm")
        scan.message = int(form.message.data)
        scan.notes = form.notes.data
        scan.glucose = int(form.glucose.data)
        scan.trend = int(form.trend.data)
        scan.bolus_u = int(form.bolus_u.data)
        if scan.bolus_u > 0:
            scan.bolus = True
        scan.basal_u = int(form.basal_u.data)
        if scan.basal > 0:
            scan.basal = True
        scan.carbohydrates = int(form.carbohydrates.data)
        if scan.carbohydrates > 0:
            scan.food = True
        scan.medication = form.medication.data
        scan.exercise = form.exercise.data
        if scan.trend == 2:
            scan.upper_limit = 12
            scan.lower_limit = 2
        if scan.trend == 1:
            scan.lower_limit = 1
            scan.upper_limit = 2
        if scan.trend == -1:
            scan.upper_limit = -1
            scan.lower_limit = -2
        if scan.trend == -2:
            scan.upper_limit = -2
            scan.lower_limit = -12
        db.session.add(scan)
        db.session.commit()
        flash(f'Scan data saved for {current_user.username}!', 'success')
        return redirect(url_for('main.index'))

    return render_template('scan.html', title='Scan', form=form, fields=fields)


@server_bp.route('/meal/', methods=['GET', 'POST'])
@login_required
def meal():
    ...


@server_bp.route('/health/', methods=['GET', 'POST'])
@login_required
def health():
    ...


@server_bp.route('/food/')
@login_required
def food():
    ...


@server_bp.route('/favicon.ico')
def favicon():
    """Add a route to the favicon for the application."""
    return send_from_directory(os.path.join(server_bp.root_path, 'static'), 'favicon.icon', mime='image/vnd.microsoft.icon')


@server_bp.route('/main.css')
def main_css():
    """Add route to css main """
    return send_from_directory(os.path.join(server_bp.root_path, 'static'), 'main.css', mime='text/css')
