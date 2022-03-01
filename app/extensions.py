"""Initiating Flask Extensions"""
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

authenticate = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
