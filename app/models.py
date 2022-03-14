"""Database models for authentication and authorization."""

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import login, db


@login.user_loader
def load_user(id) -> int:
    """Return the current users id number."""
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    """A model of the user.

    Args:
        UserMixin (object): User base class.
        authenticate (object): ORM used to authencate the user.

    Returns:
        [bool, str]: Returns a boolean value indicating whether the user password is correct. Returns the user name.
    """

    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(32), index=True, unique=True)
    email: str = db.Column(db.String(128), index=True, unique=True)
    password_hash: str = db.Column(db.String(128))
    chart_min: int = db.Column(db.Integer)
    chart_max: int = db.Column(db.Integer)
    limit_min: int = db.Column(db.Integer)
    limit_max: int = db.Column(db.Integer)
    target_min: int = db.Column(db.Integer)
    target_max: int = db.Column(db.Integer)
    my_target_min: int = db.Column(db.Integer)
    my_target_max: int = db.Column(db.Integer)
    meal_ideal: int = db.Column(db.Integer)
    meal_good: int = db.Column(db.Integer)
    meal_bad: int = db.Column(db.Integer)
    my_target_weight: float = db.Column(db.Numeric)
    my_target_bmi: float = db.Column(db.Numeric)
    scan = db.relationship('Scans', backref='active_user', lazy=True)
    food = db.relationship('Foods', backref='active_user', lazy=True)
    meal = db.relationship('Meals', backref='active_user', lazy=True)
    health = db.relationship('Healths', backref='active_user', lazy=True)

    def set_password(self, password) -> None:
        """Generate a hash of the password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        """Return True if the hashes of the entered password and stored password match."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        """Return a string representation of the user."""
        return F'<User {self.username}>'


class Healths(db.Model):
    """Health data model."""

    index = db.Column(db.Integer, primary_key=True)
    ts = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    po_pulse = db.Column(db.Integer)
    po_ox = db.Column(db.Integer)
    weight = db.Column(db.REAL)
    fat = db.Column(db.REAL)
    bpc_pulse = db.Column(db.Integer)
    bpc_systolic = db.Column(db.Integer)
    bpc_diastolic = db.Column(db.Integer)
    bpc_ihb = db.Column(db.Boolean)
    bpc_hypertension = db.Column(db.Integer, default=0)
    temperature = db.Column(db.REAL)


class Meals(db.Model):
    """Meal Model."""

    index = db.Column(db.Integer, primary_key=True)
    ts = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    calories = db.Column(db.REAL)
    fat = db.Column(db.REAL)
    cholesterol = db.Column(db.REAL)
    sodium = db.Column(db.REAL)
    carbohydrate = db.Column(db.REAL)
    protein = db.Column(db.REAL)
    serving = db.Column(db.TEXT)
    indices = db.Column(db.TEXT)


class Foods(db.Model):
    """Food Model."""

    index = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ts = db.Column(db.DateTime)
    domain = db.Column(db.TEXT)
    name = db.Column(db.TEXT)
    portion = db.Column(db.TEXT)
    unit = db.Column(db.TEXT)
    calories = db.Column(db.Integer)
    fat = db.Column(db.Integer)
    cholesterol = db.Column(db.Integer)
    sodium = db.Column(db.Integer)
    carbohydrate = db.Column(db.Integer)
    protein = db.Column(db.Integer)


class Scans(db.Model):
    """Scan data models."""

    index = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ts = db.Column(db.DateTime)
    message = db.Column(db.Integer)
    notes = db.Column(db.Text)
    glucose = db.Column(db.Integer)
    trend = db.Column(db.Integer)
    bolus = db.Column(db.Boolean)
    bolus_u = db.Column(db.Integer)
    basal = db.Column(db.Boolean)
    basal_u = db.Column(db.Integer)
    food = db.Column(db.Boolean)
    carbohydrate = db.Column(db.Integer)
    medication = db.Column(db.Boolean)
    exercise = db.Column(db.Boolean)
    lower_limit = db.Column(db.REAL)
    upper_limit = db.Column(db.REAL)
