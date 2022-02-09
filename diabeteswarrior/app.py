from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import Email, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = "this is a secret, don't do this!"
Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    email = db.Column(db.String(128), primary_key=True)
    password = db.Column(db.String(128))


class LoginForm(FlaskForm):
    email = StringField('email', validators=[Email()])
    password = PasswordField('password', validators=[Length(min=5)])


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[Email()])
    password = PasswordField('password', validators=[Length(min=5)])
    verify_password = PasswordField('verified_password', validators=[Length(min=5)])


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        return "It's valid."

    return render_template('login.html',form=form)

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        return "It's valid."

    return render_template('register.html',form=form)

if __name__ == '__main__':
    app.run(debug=True)
