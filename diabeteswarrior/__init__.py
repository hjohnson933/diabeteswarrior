from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from diabeteswarrior.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


#pylint: disable=import-outside-toplevel
def create_app(config_class=Config):
    server = Flask(__name__, instance_relative_config=True)
    server.config.from_object(Config)

    db.init_app(server)
    bcrypt.init_app(server)
    login_manager.init_app(server)
    mail.init_app(server)

    from diabeteswarrior.scans.routes import scans
    from diabeteswarrior.healths.routes import healths
    from diabeteswarrior.users.routes import users
    from diabeteswarrior.posts.routes import posts
    from diabeteswarrior.main.routes import main
    from diabeteswarrior.errors.handlers import errors
    server.register_blueprint(scans)
    server.register_blueprint(healths)
    server.register_blueprint(users)
    server.register_blueprint(posts)
    server.register_blueprint(main)
    server.register_blueprint(errors)

    return server
