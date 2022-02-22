import dash
from flask import Flask
from flask.helpers import get_root_path
from flask_login import login_required

from config import BaseConfig


def create_app():
    server = Flask(__name__)
    server.config.from_object(BaseConfig)

    from app.health.layout import layout as layout1
    from app.health.callbacks import register_callbacks as register_callbacks1
    register_dashapps(server, 'Health', 'health', layout1, register_callbacks1)

    from app.scan.layout import layout as layout2
    from app.scan.callbacks import register_callbacks as register_callbacks2
    register_dashapps(server, 'Scan', 'scan', layout2, register_callbacks2)

    register_extensions(server)
    register_blueprints(server)

    return server


def register_dashapps(app, title, base_pathname, layout, register_callbacks_fun):
    meta_viewport = {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    my_dashapp = dash.Dash(__name__,
                           server=app,
                           url_base_pathname=F'/{base_pathname}/',
                           assets_folder=get_root_path(__name__) + F'/{base_pathname}/assets/',
                           meta_tags=[meta_viewport])

    with app.app_context():
        my_dashapp.title = title
        my_dashapp.layout = layout
        register_callbacks_fun(my_dashapp)

        _project_dashviews(my_dashapp)


def _project_dashviews(dashapp):
    for view_func in dashapp.server.view_functions:
        if view_func.startswith(dashapp.config.url_base_pathname):
            dashapp.server.view_functions[view_func] = login_required(dashapp.server.view_functions[view_func])


def register_extensions(server):
    from app.extensions import db
    from app.extensions import login
    from app.extensions import migrate

    db.init_app(server)
    login.init_app(server)
    login.login_view = 'main.login'
    migrate.init_app(server, db)


def register_blueprints(server):
    from app.webapp import server_bp

    server.register_blueprint(server_bp)
