import os
from app import app, db, lm
from flask import render_template, flash, redirect, request, session, abort, url_for, g
from flask_login import login_user, logout_user, current_user, login_required

from ..Models.user import User

import bcrypt


@app.route('/login')
def login():
    if not session.get('logged_in'):
        return render_template('login.html')
    
    return "Ya estas logueado"


SALT_ROUNDS = 14
@app.route('/login', methods=['POST'])
def do_admin_login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
 
    if not POST_PASSWORD or not POST_USERNAME:
        flash("Debe ingresar un nombre de usuario y contraseña")
        return login()

    error_msj = "Contraseña incorrecta"
    user = User.query.filter_by(username=POST_USERNAME).first()

    if not user: #Solo para agregarlo ahora...
        error_msj = "El usuario no existe"
        hashed = bcrypt.hashpw(POST_PASSWORD.encode(), bcrypt.gensalt(SALT_ROUNDS))
        nuevo = User(username=POST_USERNAME, password=hashed)
        db.session.add(nuevo)
        db.session.commit()

    if user and (user.username==POST_USERNAME) and (bcrypt.hashpw(POST_PASSWORD.encode(), user.password) == user.password):
        session['logged_in'] = True
        return redirect('home')

    flash(error_msj)
    return login()


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect('home')


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user