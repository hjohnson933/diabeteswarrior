"""Main Flask Application."""
import dash
import dash_bootstrap_components as dbc
from config import BaseConfig
from flask import Flask
from flask.helpers import get_root_path
from flask_login import login_required


def create_app() -> object:
    """Configure the Flask server and register the blueprints.

    Returns:
        object: flask server instance.
    """
    server = Flask(__name__)
    server.config.from_object(BaseConfig)

    from app.meal.callbacks import register_callbacks
    from app.meal.layout import layout
    register_dashapps(server, 'Meal', 'meal', layout, register_callbacks)

    from app.food.callbacks import register_callbacks
    from app.food.layout import layout
    register_dashapps(server, 'Food', 'food', layout, register_callbacks)

    from app.health.callbacks import register_callbacks
    from app.health.layout import layout
    register_dashapps(server, 'Health', 'health', layout, register_callbacks)

    from app.scan.callbacks import register_callbacks
    from app.scan.layout import layout
    register_dashapps(server, 'Scan', 'scan', layout, register_callbacks)

    register_extensions(server)
    register_blueprints(server)

    return server


def register_dashapps(app: str, title: str, base_pathname: str, layout: str, register_callbacks_func: str) -> None:
    """Register the Dash application in the flask server.

    Args:
        app (str): The name of the Flask server.
        title (str): The name of the Dash application.
        base_pathname (str): The root file path of the Dash application.
        layout (str): The file name of the Dash layout.
        register_callbacks_func (str): The file name of the Dash callbacks.
    """
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

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


def _project_dashviews(dashapp: object) -> None:
    """Ensure authentication for the dash routes."""
    for view_func in dashapp.server.view_functions:
        if view_func.startswith(dashapp.config.url_base_pathname):
            dashapp.server.view_functions[view_func] = login_required(dashapp.server.view_functions[view_func])


def register_extensions(server: object) -> None:
    """Initialize the Flask extensions to the server instance.

    Args:
        server (object): Flask server instance.
    """
    from app.extensions import authenticate, login, migrate

    authenticate.init_app(server)
    login.init_app(server)
    login.login_view = 'main.login'
    migrate.init_app(server, authenticate)


def register_blueprints(server: object) -> None:
    """Register the blueprints to the Flask server instance.

    Args:
        server (object): The flask server instance.
    """
    from app.webapp import server_bp

    server.register_blueprint(server_bp)
