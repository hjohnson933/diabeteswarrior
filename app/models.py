"""Database models for authentication, authorization & user data."""

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import login, db


@login.user_loader
def load_user(uid) -> int:
    """Return the current users id number."""
    return Users.query.get(int(uid))


class Users(db.Model, UserMixin):
    """The User Model.

    Attributes
    ----------
    id : int
        Users id number.
    username : str
         Required. The user's chosen username.
    email : str
        Required. The user's email address
    account_token : str
        Calculated field to ensure uniqueness.
    password_hash : str
        Your password stored in the database as a hash.

    Methods
    -------
    set_password_hash(self, password):
        Calculates and stores the hashed password.
    check_password_hash(self, password):
        Verifies the stored and entered passwords are the same.
    __repr__(self):
        Returns the username.
    """

    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(32), index=True, nullable=False)
    email: str = db.Column(db.String(128), index=True, nullable=False)
    account_token = db.Column(db.String(128), index=True, nullable=False, unique=True)
    password_hash: str = db.Column(db.String(128), index=True)
    target = db.relationship('Targets', backref='active_user', lazy=True)
    scan = db.relationship('Scans', backref='active_user', lazy=True)
    food = db.relationship('Foods', backref='active_user', lazy=True)
    meal = db.relationship('Meals', backref='active_user', lazy=True)
    health = db.relationship('Healths', backref='active_user', lazy=True)

    def set_password_hash(self, password) -> None:
        """Generate a hash of the username, email and password.

                Parameters:
                    self (object): This class
                    password (str): The password
                Returns:
                    Nothing
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        """Return True if the hashes of the entered password and stored password match.
                Parameters:
                    self (object): This class
                    password (str): The password
                Returns:
                    Users (bool): True if the entered and stored hasshes match
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        """Return a string representation of the user.
                Parameters:
                    self (object): This class
                Returns:
                    Users (str): A string representation of the user
        """
        return F'<User {self.username}>'


class Scans(db.Model):
    """The Users Scans Models.

        Attributes:
            -----------
            index: int
                calculate the record index
            ts: datetime
                The timestamp of the record being stored
            user_id: int
                The user identifier for the record being stored
            message: int
                The message from the top left of the Freestyle reader
            notes: str
                Additional notes you would like to add.
            glucose: int
                Your current glucose reading
            trend: int
                Your current trend from the Freestyle reader
            bolus: bool
                True if you entered an amount of bolus insulin
            bolus_u: int
                The amount of bolus insulin you used
            basal: bool
                True if you entered a amount of basal insulin
            basal_u: int
                The amount of basal insulin you used
            food: bool
                True if you entered an amount of carbohydrates
            carbohydrate: int
                The amount of carbohydrates ingested
            medication: bool
                Set to true if you took your medication
            exercise: bool
                Set to true if you exercised
            lower_limit: float
                Calculated, used for graphing
            upper_limit: float
                Calculated, used for graphing

        Methods:
        --------
    """

    index = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
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


class Healths(db.Model):
    """Health data model.

        Attributes:
        -----------
        index: int
            calculate the record index
        ts: datetime
            The timestamp of the record being stored
        user_id: int
            The user identifier for the record being stored
        po_pulse: int
            Heart rate from the pulseoximeter
        po_ox: int
            Oxygen saturation from the pulseoximeter
        weight: float
            Body weight from you scale
        fat:
            Body Mass Index from you scale if you have one that provides this information
        bpc_pulse:
            Heart rate from the blood pressure cuff
        bpc_systolic: int
            Systolic pressure from the blood pressure cuff
        bpc_diastolic: int
            Diastolic pressure from the blood pressure cuff
        bpc_ihb: bool
            Irregular heart beat indicator from the blood pressure cuff
        bpc_hypertension: int
            Current stage of hypertension from the blood pressure cuff
        temperature: float
            Your current body temperature

        Methods:
        --------
    """

    index = db.Column(db.Integer, primary_key=True)
    ts = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
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
    """The Users Meals Model.

        Attributes:
            -----------
            index: int
                calculate the record index
            ts: datetime
                The timestamp of the record being stored
            user_id: int
                The user identifier for the record being stored
            fat: float
                total amount of fat in this meal
            cholesterol: float
                total amount of cholesterol in this meal
            sodium: float
                total amount of sodium in this meal
            carbohydrate: float
                total amount of carbohydrates in this meal
            protein: float
                total amount of protein in this meal
            servings: list
                number of servings for each item in this meal
            indices: list
                the food index of each item in this meal

        Methods:
        -------

    """

    index = db.Column(db.Integer, primary_key=True)
    ts = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    calories = db.Column(db.REAL)
    fat = db.Column(db.REAL)
    cholesterol = db.Column(db.REAL)
    sodium = db.Column(db.REAL)
    carbohydrate = db.Column(db.REAL)
    protein = db.Column(db.REAL)
    serving = db.Column(db.TEXT)
    indices = db.Column(db.TEXT)


class Foods(db.Model):
    """The Users Foods Model.

        Attributes:
            -----------
            index: int
                calculate the record index
            ts: datetime
                The timestamp of the record being stored
            user_id: int
                The user identifier for the record being stored
            domain: string
                The manufacturer, cook or distributor of the food
            name: string
                The name of the food
            portion: str
                The amount that makes up the whole serving
            unit: str
                The name of the unit the food is recorded in
            calories: int
                The number of calories in the food
            fat: int
                The amount of fat in the food
            cholesterol: int
                The amount of cholesterol in the food
            sodium: int
                The amount of sodium in the food
            carbohydrate: int
                The amount of carbohydrates in the food
            protein: int
                The amount of protein in the food

        Methods:
        --------
    """

    index = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
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


class Targets(db.Model):
    """The Users Targets Model

        Attributes:
        -----------
        index: int
            calculate the record index
        ts: datetime
            The timestamp of the record being stored
        user_id: int
            The user identifier for the record being stored
        chart_min: int
            The lower limit of the chart
        chart_max: int
            the upper limit of the chart
        limit_min: int
            the lowest value your meter gives a number for
        limit_max: int
            the highest value your meter gives a number for
        target_min: int
            the lowest value the ADA or your doctor recemends
        target_max: int
            the highest value the ADA or your doctor recemends
        my_target_min: int
            the fasting value you would like to not go below
        my_target_max: int
            the fasting value you would like to not go above
        meal_ideal: int
            your post meal value that you would like
        meal_good: int
            your post meal value that you will accept occasionally
        meal_bad: int
            your post meal value that you you should never exceed
        my_target_weight: float
            the goal of you body weight
        my_target_bmi: float
            the goal of your body mass index

        Methods:
        --------
    """

    index = db.Column(db.Integer, primary_key=True)
    ts = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
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
