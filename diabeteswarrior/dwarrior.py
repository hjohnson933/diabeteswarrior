"""Diabetes Warrior Application"""
from flask import Flask, render_template, url_for, flash, redirect
from .forms import Register, Login

app = Flask(__name__)
app.config['SECRET_KEY'] = '..72:products:CHILDREN:coast:72..'

posts = [
    {'id':0,'author_id':0,'created':'2022-02-14 00:00:00','title':'Test post 0','body':'Test post'},
    {'id':1,'author_id':0,'created':'2022-02-14 00:01:00','title':'Test post 1','body':'Test post'},
    {'id':2,'author_id':0,'created':'2022-02-14 00:02:00','title':'Test post 2','body':'Test post'}
]

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', page='About')

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = Register()
    if form.validate_on_submit():
        flash(F"Account registered for {form.username.data}.", "success")
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = Login()
    return render_template('login.html', title='Login', form=form)
