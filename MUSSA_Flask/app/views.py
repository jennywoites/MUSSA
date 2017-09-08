from flask import render_template

from .Views.Login import *
from .Views.Signin import *


@app.route('/')
@app.route('/home')
def home():
    return "Esto es el home"


@app.route('/index')
def index():
    return render_template('index.html')