from datetime import datetime

from flask import current_app
from flask_login import UserMixin
from itsdangerous.jws import TimedJSONWebSignatureSerializer as Serializer

from diabeteswarrior import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        #pylint: disable=bare-except
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Health(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    po_pulse = db.Column(db.Integer)
    po_ox = db.Column(db.Integer)
    weight = db.Column(db.Float)
    fat = db.Column(db.Float)
    bp_pulse = db.Column(db.Integer)
    bp_systolic = db.Column(db.Integer)
    bp_diastolic = db.Column(db.Integer)
    bp_ihb = db.Column(db.Boolean)
    bp_hypertension = db.Column(db.Integer)
    temperature = db.Column(db.Float)


class Scan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    message = db.Column(db.Integer)
    glucose_id = db.Column(db.Integer)
    trend = db.Column(db.Integer)
    notes = db.Column(db.Text)
    bolus = db.Column(db.Boolean)
    bolus_u = db.Column(db.Integer)
    basal = db.Column(db.Boolean)
    basal = db.Column(db.Integer)
    food = db.Column(db.Boolean)
    food_u = db.Column(db.Integer)
    medication = db.Column(db.Boolean)
    exercise = db.Column(db.Boolean)


class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    servings = db.Column(db.Text)
    indices = db.Column(db.Text)


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    domain = db.Column(db.String(120))
    name = db.Column(db.String(120))
    portion = db.Column(db.Integer)
    unit = db.Column(db.String(120))
    calories = db.Column(db.Integer)
    fat = db.Column(db.Integer)
    cholesterol = db.Column(db.Integer)
    sodium = db.Column(db.Integer)
    carbohydrate = db.Column(db.Integer)
    protein = db.Column(db.Integer)


class CGM(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    Device = db.Column(db.String(120))
    Number = db.Column(db.String(120))
    Type = db.Column(db.Integer)
    Scan = db.Column(db.Integer)
    NonnumericRapidActingInsulin = db.Column(db.Boolean)
    RapidActingInsulin = db.Column(db.Integer)
    NonnumericFood = db.Column(db.Boolean)
    CarbohydratesGrams = db.Column(db.Integer)
    CarbohydratesServings = db.Column(db.Integer)
    NonnumericLongActingInsulin = db.Column(db.Boolean)
    LongActingInsulin = db.Column(db.Integer)
    Notes = db.Column(db.Text)
    Strip = db.Column(db.Integer)
    Ketone = db.Column(db.Float)
    MealInsulin = db.Column(db.Integer)
    CorrectionInsulin = db.Column(db.Integer)
    UserChangeInsulin = db.Column(db.Integer)
