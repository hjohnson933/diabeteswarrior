"""Database models for authentication and authorization."""
# todo add database authorization model.
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import authenticate, login


@login.user_loader
def load_user(id) -> int:
    """Return the current users id number."""
    return User.query.get(int(id))


class User(UserMixin, authenticate.Model):
    """A model to the user.

    Args:
        UserMixin (object): User base class.
        authenticate (object): ORM used to authencate the user.

    Returns:
        [bool, str]: Returns a boolean value indicating whether the user password is correct. Returns the user name.
    """

    id: int = authenticate.Column(authenticate.Integer, primary_key=True)
    username: str = authenticate.Column(authenticate.String(64), index=True, unique=True)
    password_hash: str = authenticate.Column(authenticate.String(128))

    def set_password(self, password) -> None:
        """Generate a hash of the password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        """Return True if the hashes of the entered password and sotred password match."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        """Return a string representation of the user."""
        return F'<User {self.username}>'
