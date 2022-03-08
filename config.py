"""Reflection of OS environment variables."""
import os


def get_sqlite_uri() -> str:
    """Get environment variables from the OS.

    Returns:
        str: The database uri
    """
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_name = os.environ['DATABASE_URL'].split('/')[-1]
    return F"sqlite:///{basedir}/{db_name}"


class BaseConfig:
    """Application configuration as a class."""

    SQLALCHEMY_DATABASE_URI = get_sqlite_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ['SECRET_KEY']
