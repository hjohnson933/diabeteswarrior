"""Database models for authentication."""
# todo add database authorization model.
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import authenticate, login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, authenticate.Model):
    id: int = authenticate.Column(authenticate.Integer, primary_key=True)
    username: str = authenticate.Column(authenticate.String(64), index=True, unique=True)
    password_hash: str = authenticate.Column(authenticate.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return F'<User {self.username}>'
