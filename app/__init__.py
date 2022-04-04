"""Main Flask Application."""

from typing import Callable, Any
import dash
from flask import Flask
from flask.helpers import get_root_path
from flask_login import login_required

from config import BaseConfig


def create_app() -> object:
    """Configure the Flask server and register the blueprints.

    Returns:
        object: flask server instance.
    """

    server = Flask(__name__, instance_relative_config=True)
    server.config.from_object(BaseConfig)

    from app.scans.callbacks import register_callbacks
    from app.scans.layout import layout
    register_dashapps(server, 'Scan', 'scans', layout, register_callbacks)

    from app.healths.callbacks import register_callbacks
    from app.healths.layout import layout
    register_dashapps(server, 'Health', 'healths', layout, register_callbacks)

    # from app.foods.callbacks import register_callbacks
    # from app.foods.layout import layout
    # register_dashapps(server, 'Food', 'foods', layout, register_callbacks)

    # # from app.meal.callbacks import register_callbacks
    # from app.meal.layout import layout
    # register_dashapps(server, 'Meal', 'meal', layout, register_callbacks)

    register_extensions(server)
    register_blueprints(server)

    return server


def register_dashapps(app: Flask, title: str, base_pathname: str, layout: str, register_callbacks_func: Callable[[Any], Any]) -> None:
    """Register the Dash application in the flask server.

    Args:
        app (str): The name of the Flask server.
        title (str): The name of the Dash application.
        base_pathname (str): The root file path of the Dash application.
        layout (str): The file name of the Dash layout.
        register_callbacks_func (str): The file name of the Dash callbacks.
    """
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    #    removed from my_dashapp for testing external_stylesheets=[dbc.themes.BOOTSTRAP])
    my_dashapp = dash.Dash(__name__,
                           server=app,
                           url_base_pathname=F'/{base_pathname}/',
                           assets_folder=get_root_path(__name__) + F'/{base_pathname}/assets/',
                           meta_tags=[meta_viewport],
                           external_stylesheets=["https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"],
                           external_scripts=[{"src": "https://kit.fontawesome.com/3aad6a615d.js", "crossorigin": "anonymous"},
                               {"src": "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.min.js", "integrity": "sha384-QJHtvGhmr9XOIpI6YVutG+2QOK9T+ZnN4kzFN1RtK3zEFEIsxhlmWl5/YESvpZ13", "crossorigin": "anonymous"},
                               {"src": "https://code.jquery.com/jquery-3.6.0.min.js", "integrity": "sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=", "crossorigin": "anonymous"},
                               {"src": "https://cdnjs.cloudflare.com/ajax/libs/popper.js/2.11.4/umd/popper.min.js", "integrity": "sha512-+Tn2V/oN9O/kiaJg/1o5bETqyS35pMDJzkhkf8uvCzxmRox69AsWkSpBSMEGEe4EZp07Nunw712J3Xvh5Tti0w==", "crossorigin": "anonymous", "referrerpolicy": "no-referrer"}],
                           suppress_callback_exceptions=True
                           )
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
    from app.extensions import db, login, migrate

    login.init_app(server)
    login.login_view = 'main.login'
    migrate.init_app(server, db)
    db.init_app(server)


def register_blueprints(server: object) -> None:
    """Register the blueprints to the Flask server instance.

    Args:
        server (object): The flask server instance.
    """
    from app.webapp import server_bp

    server.register_blueprint(server_bp)
