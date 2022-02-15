"""Diabetes Warrior Application"""
from flask import Flask, render_template

app = Flask(__name__)

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
