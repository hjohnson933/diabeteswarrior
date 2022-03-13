"""Reflection of OS environment variables."""
import os


def sqlalchemy_database_uri() -> str:
    """Get DATABASE_URL variable from the OS then test for database type. If it is a SQLITE database return the generated SQLALCHEMY_DATABASE_URI other wise return the SQLALCHEMY_DATABASE_URI from the variable.

    Returns:
        str: The database uri
    """
    db_url = os.environ['DATABASE_URL']
    if db_url.startswith('sqlite'):
        basedir = os.path.abspath(os.path.dirname(__file__))
        db_name = db_url.split('/')[-1]
        return F"sqlite:///{basedir}/instance/{db_name}"
    return db_url


class BaseConfig:
    """Application configuration as a class."""

    SQLALCHEMY_DATABASE_URI = sqlalchemy_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ['SECRET_KEY']
