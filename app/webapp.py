"""Blueprint for Flask routes."""
import os

from flask import Blueprint, redirect, render_template, request, url_for, send_from_directory
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from app.extensions import authenticate
from app.forms import LoginForm, RegistrationForm
from app.models import User

server_bp = Blueprint('main', __name__)


@server_bp.route('/')
def index() -> str:
    """Home route."""
    return render_template('index.html', title='Home Page')


@server_bp.route('/login/', methods=['GET', 'POST'])
def login() -> object:
    """Login route."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            error = 'Invalid username or password'
            return render_template('login.html', error=error, form=form)

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@server_bp.route('/logout/')
@login_required
def logout() -> object:
    """Logout route."""
    logout_user()

    return redirect(url_for('main.index'))


@server_bp.route('/register/', methods=['GET', 'POST'])
def register() -> object:
    """Route to the registration form."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(password=form.password.data)
        authenticate.session.add(user)
        authenticate.session.commit()

        return redirect(url_for('main.login'))

    return render_template('register.html', title='Register', form=form)


@server_bp.route('/favicon.ico')
def favicon():
    """Add a route to the favicon for the application."""
    return send_from_directory(os.path.join(server_bp.root_path, 'static'), 'favicon.icon', mime='image/vnd.microsoft.icon')
