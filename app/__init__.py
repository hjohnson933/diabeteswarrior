"""Main Flask Application"""
import dash
import dash_bootstrap_components as dbc
from config import BaseConfig
from flask import Flask
from flask.helpers import get_root_path
from flask_login import login_required


def create_app():
    server = Flask(__name__)
    server.config.from_object(BaseConfig)

    # from app.health.callbacks import register_callbacks
    # from app.health.layout import layout
    # register_dashapps(server, 'Health', 'health', layout, register_callbacks)

    # from app.food.callbacks import register_callbacks
    # from app.food.layout import layout
    # register_dashapps(server, 'Food', 'food', layout, register_callbacks)

    from app.scan.callbacks import register_callbacks
    from app.scan.layout import layout
    register_dashapps(server, 'Scan', 'scan', layout, register_callbacks)

    register_extensions(server)
    register_blueprints(server)

    return server


def register_dashapps(app, title, base_pathname, layout, register_callbacks_func):
    meta_viewport = {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    my_dashapp = dash.Dash(__name__,
                           server=app,
                           url_base_pathname=F'/{base_pathname}/',
                           assets_folder=get_root_path(__name__) + F'/{base_pathname}/assets/',
                           meta_tags=[meta_viewport],
                           external_stylesheets=[dbc.themes.BOOTSTRAP])
    my_dashapp.enable_dev_tools()

    with app.app_context():
        my_dashapp.title = title
        my_dashapp.layout = layout
        register_callbacks_func(my_dashapp)

        _project_dashviews(my_dashapp)


def _project_dashviews(dashapp):
    for view_func in dashapp.server.view_functions:
        if view_func.startswith(dashapp.config.url_base_pathname):
            dashapp.server.view_functions[view_func] = login_required(
                dashapp.server.view_functions[view_func])


def register_extensions(server):
    from app.extensions import authenticate, login, migrate

    authenticate.init_app(server)
    login.init_app(server)
    login.login_view = 'main.login'
    migrate.init_app(server, authenticate)


def register_blueprints(server):
    from app.webapp import server_bp

    server.register_blueprint(server_bp)
