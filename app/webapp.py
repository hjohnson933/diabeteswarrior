"""Blueprint for Flask routes."""
import os

from flask import Blueprint, redirect, render_template, url_for, send_from_directory, request, flash
from flask_login import current_user, login_required, logout_user, login_user
from werkzeug.urls import url_parse

# from app.extensions import db
from app.forms import RegistrationForm, LoginForm
from app.models import User

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
    fields = ['username', 'password']

    if form.validate_on_submit():
        if form.username.data == 'admin' or form.username.data == 'a@dw.com':
            if form.password.data == 'pass':
                flash('Login successful', 'success')
                return redirect(url_for('main.index'))
            flash('Login failed', 'danger')
    #     user = User.query.filter_by(username=form.username.data).first()
    #     if user is None or not user.check_password(form.password.data):
    #         error = 'Invalid username or password'
    #         return render_template('login.html', error=error, form=form)

    #     login_user(user, remember=form.remember_me.data)
    #     next_page = request.args.get('next')
    #     if not next_page or url_parse(next_page).netloc != '':
    #         next_page = url_for('main.index')
    #     return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form, fields=fields)


@server_bp.route('/register/', methods=['GET', 'POST'])
def register() -> object:
    """Route to the registration form."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    fields = ['username', 'password', 'confirm', 'email', 'chart_min', 'chart_max', 'limit_min', 'limit_max', 'target_min', 'target_max', 'my_target_min', 'my_target_max', 'meal_ideal', 'meal_good', 'meal_bad', 'my_target_weight', 'my_target_bmi']

    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('main.index'))

    return render_template('register.html', title='Register', form=form, fields=fields)


@server_bp.route('/favicon.ico')
def favicon():
    """Add a route to the favicon for the application."""
    return send_from_directory(os.path.join(server_bp.root_path, 'static'), 'favicon.icon', mime='image/vnd.microsoft.icon')


@server_bp.route('/main.css')
def main_css():
    """Add route to css main """
    return send_from_directory(os.path.join(server_bp.root_path, 'static'), 'main.css', mime='text/css')


@server_bp.route('/bootstrap.css')
def bootstrap_css():
    """Add route to css main """
    return send_from_directory(os.path.join(server_bp.root_path, 'static'), 'bootstrap.css', mime='text/css')


@server_bp.route('/utilities.css')
def utilities_css():
    """Add route to css main """
    return send_from_directory(os.path.join(server_bp.root_path, 'static'), 'utilities.css', mime='text/css')
