import os
from app import app, db
from flask import render_template, redirect


@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route("/signin/do_registrarse", methods=['POST'])
def do_registrarse():
    return "Hola?"
