"""Blueprint for Flask routes."""
import os

import arrow
from flask import (Blueprint, flash, make_response, redirect, render_template,
                   send_from_directory, url_for)
from flask.wrappers import Response
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.exceptions import HTTPException

from app.extensions import db
from app.forms import (FoodForm, HealthForm, LoginForm, MealForm, RegistrationForm, ScanForm, TargetForm)
from app.models import Foods, Healths, Meals, Scans, Targets, Users


# * The Errors Blueprint
errors_bp = Blueprint('errors', __name__)


@errors_bp.app_errorhandler(HTTPException)
def errors(error: HTTPException) -> Response:
    """Error handler."""
    return render_template('/error.html', title='Error', error=error), error.code


# * The Server Blueprint
server_bp = Blueprint('main', __name__)


# * Unsecured Routes
@server_bp.route('/')
def index() -> str:
    """Landing page."""
    return render_template('base.html', title='Index')


@server_bp.route('/main.css')
def main_css():
    """Add route to css main """
    return send_from_directory(os.path.join(server_bp.root_path, 'static'), 'main.css', mime='text/css')


@server_bp.route('/favicon.ico')
def favicon() -> Response:
    """Add a route to the favicon for the application."""
    return send_from_directory(os.path.join(server_bp.root_path, 'static'), 'favicon.icon', mime='image/vnd.microsoft.icon')


@server_bp.route('/login/', methods=['GET', 'POST'])
def login() -> object:
    """Login route."""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    fields = ['email', 'password']

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            error = 'Invalid email or password'
            return render_template('login.html', title='Sign In', error=error, form=form)

        if login_user(user, remember=form.remember_me.data):
            return redirect(url_for('main.home', rid=0))

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
        user.account_token = F"{user.username.lower()}_{user.email.lower()}"
        user.set_password_hash(password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('main.target_data'))

    return render_template('register.html', title='Register', form=form, fields=fields)


# * Secured Routes
@server_bp.route("/home/<int:rid>")
@login_required
def home(rid: int) -> Response:
    """Home page."""
    resp = make_response(render_template('home.html', title=current_user.username, id=current_user.id, rid=rid))
    b = str(current_user.id)

    resp.set_cookie('userID', b)
    return resp


@server_bp.route('/logout/')
@login_required
def logout() -> object:
    """Logout route."""
    logout_user()

    return redirect(url_for('main.index'))


@server_bp.route('/target/', methods=['GET', 'POST'])
@login_required
def target_data() -> object:

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
def scan_data() -> object:
    form = ScanForm()
    fields = ['message', 'notes', 'glucose', 'trend', 'bolus_u', 'basal_u', 'carbohydrates', 'medication', 'exercise']

    if form.validate_on_submit():
        scan = Scans()
        scan.bolus = False
        scan.bolus_u = 0
        scan.basal = False
        scan.basal_u = 0
        scan.food = False
        scan.carbohydrates = 0
        scan.lower_limit = -1
        scan.upper_limit = 1
        scan.ts = arrow.now().format("YYYY-MM-DD HH:mm")
        scan.user_id = current_user.id
        scan.message = int(form.message.data)
        scan.notes = form.notes.data
        scan.glucose = int(form.glucose.data)
        scan.trend = int(form.trend.data)
        if int(form.bolus_u.data) > 0:
            scan.bolus_u = int(form.bolus_u.data)
            scan.bolus = True
        if int(form.basal_u.data) > 0:
            scan.basal_u = int(form.basal_u.data)
            scan.basal = True
        if int(form.carbohydrates.data) > 0:
            scan.carbohydrate = int(form.carbohydrates.data)
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
        return redirect(url_for('main.home', rid=1))

    return render_template('new.html', title='Scan', form=form, fields=fields)


@server_bp.route('/health/', methods=['GET', 'POST'])
@login_required
def health_data() -> object:
    form = HealthForm()
    fields = ['po_pulse', 'po_ox', 'weight', 'fat', 'bpc_pulse', 'bpc_systolic', 'bpc_diastolic', 'bpc_ihb', 'bpc_hypertension', 'temperature']

    if form.validate_on_submit():
        health = Healths()
        health.ts = arrow.now().format("YYYY-MM-DD HH:mm")
        health.user_id = current_user.id
        health.po_pulse = form.po_pulse.data
        health.po_ox = form.po_ox.data
        health.weight = form.weight.data
        health.fat = form.fat.data
        health.bpc_pulse = form.bpc_pulse.data
        health.bpc_systolic = form.bpc_systolic.data
        health.bpc_diastolic = form.bpc_diastolic.data
        health.bpc_ihb = form.bpc_ihb.data
        health.bpc_hypertension = form.bpc_hypertension.data
        health.temperature = form.temperature.data
        db.session.add(health)
        db.session.commit()
        flash(f'Health data saved for {current_user.username}!', 'success')
        return redirect(url_for('main.home', rid=2))

    return render_template('new.html', title='Health', form=form, fields=fields)


@server_bp.route('/food/', methods=['GET', 'POST'])
@login_required
def food_data() -> object:
    form = FoodForm()
    fields = ['domain', 'name', 'portion', 'unit', 'calories', 'fat', 'cholesterol', 'sodium', 'carbohydrate', 'protein']

    if form.validate_on_submit():
        food = Foods()
        food.ts = arrow.now().format("YYYY-MM-DD HH:mm")
        food.user_id = current_user.id
        food.domain = form.domain.data
        food.name = form.name.data
        food.portion = form.portion.data
        food.unit = form.unit.data
        food.calories = form.calories.data
        food.fat = form.fat.data
        food.cholesterol = form.cholesterol.data
        food.sodium = form.sodium.data
        food.carbohydrate = form.carbohydrate.data
        food.protein = form.protein.data
        db.session.add(food)
        db.session.commit()
        flash(f'Food data saved for {current_user.username}!', 'success')
        return redirect(url_for('main.home', rid=3))

    return render_template('new.html', title='Food', form=form, fields=fields)


@server_bp.route('/meal/', methods=['GET', 'POST'])
@login_required
def meal_data() -> object:
    form = MealForm()
    fields = ['calories', 'fat', 'cholesterol', 'sodium', 'carbohydrate', 'protein', 'serving', 'indices']

    if form.validate_on_submit():
        meal = Meals()
        meal.ts = arrow.now().format("YYYY-MM-DD HH:mm")
        meal.user_id = current_user.id
        meal.calories = form.calories.data
        meal.fat = form.fat.data
        meal.cholesterol = form.cholesterol.data
        meal.sodium = form.sodium.data
        meal.carbohydrate = form.carbohydrate.data
        meal.protein = form.protein.data
        meal.serving = form.serving.data
        meal.indices = form.indices.data
        db.session.add(meal)
        db.session.commit()
        flash(f'Meal data saved for {current_user.username}!', 'success')
        return redirect(url_for('main.home'))

    return render_template('new.html', title='Meal', form=form, fields=fields)
