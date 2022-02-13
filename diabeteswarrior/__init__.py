"""Diabetes Management Application"""
__version__:str = '0.1.0'

import os

from flask import Flask

from diabeteswarrior import auth, db, dwarrior


def create_app(test_config=None) -> object:
    """Create and configure an instance of the Flask application."""

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY="dev", DATABASE=os.path.join(app.instance_path, "diabeteswarrior.sqlite"))

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello() -> str:
        return "<h1>Hello, World!</h1>"

    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(dwarrior.bp)
    app.add_url_rule("/", endpoint="index")

    return app
