"""Diabetes Management Application"""
__version__:str = '0.1.0'

import os

from flask import Flask


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    # ? a default secret that should be overridden by instance config
    app.config.from_mapping(SECRET_KEY="dev", DATABASE=os.path.join(app.instance_path, "diabeteswarrior.sqlite"),)

    # ? load the instance config, if it exists, when not testing load the test config if passed in then in the try block ensure the instance folder exists
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # ? register the database commands
    from diabeteswarrior import db

    db.init_app(app)

    # ? apply the blueprints to the app
    from diabeteswarrior import auth, blog, bgl

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(bgl.bp)

    # ? make url_for('index') == url_for('blog.index') in another app, you might define a separate main index here with app.route, while giving the blog blueprint a url_prefix, but for the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    return app
