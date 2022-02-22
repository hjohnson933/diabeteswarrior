from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db, login

# ?pylint: disable=redefined-builtin
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id:int = db.Column(db.Integer, primary_key=True)
    username:str = db.Column(db.String(128), index=True, unique=True)
    password_hash:str = db.Column(db.String(128))

    def set_password(self, password) ->str:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) ->bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) ->str:
        return '<User {}>'.format(self.username)
