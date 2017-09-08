import os

from app import app, db
from flask import render_template, flash, redirect, request, session, abort, url_for, g
from sqlalchemy import or_

from ..Models.user import User
from ..Models.alumno import Alumno


import bcrypt
SALT_ROUNDS = 14

@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route("/signin/do_registrarse", methods=['POST'])
def do_registrarse():
    if request.form['btn_registrarse']:
        return on_btn_registrarse()

    return render_template('signin.html')


def on_btn_registrarse():
    POST_apellido = str(request.form['apellido'])
    POST_nombre = str(request.form['nombre'])
    POST_DNI = str(request.form['DNI'])
    POST_email = str(request.form['email'])
    POST_padron = str(request.form['padron'])
    POST_usuario = str(request.form['username']) 
    POST_password = str(request.form['password'])
    POST_repetir_password = str(request.form['repetir_password'])

    if not POST_apellido or not POST_nombre or not POST_DNI or not POST_email:
        flash("Por favor complete todos los campos obligatorios.")
        return redirect('signin')

    if not usuario_es_valido(POST_usuario) or not password_es_valida(POST_password, POST_repetir_password):
        return redirect('signin')

    if campos_son_invalidos(POST_DNI, POST_email, POST_padron):
        return redirect('signin')

    hashed = bcrypt.hashpw(POST_password.encode(), bcrypt.gensalt(SALT_ROUNDS))
    usuario = User(username=POST_usuario, password=hashed)

    alumno = Alumno(apellido=POST_apellido, nombre=POST_nombre, dni=POST_DNI, email=POST_email, padron=POST_padron)
    usuario.alumno = alumno

    db.session.add(usuario)
    db.session.add(alumno)

    db.session.commit()

    return "Se creo el usuario!"


def password_es_valida(POST_password, POST_repetir_password):
    #TODO
    return True


def usuario_es_valido(POST_usuario):
    """
    Verifica que el nombre de usuario no se encuentre ya en la base de datos
    """
    if User.query.filter_by(username=POST_usuario).first():
        flash("El nombre de usuario no está disponible.")
        return False

    return True    


def campos_son_invalidos(POST_DNI, POST_email, POST_padron):
    """
    Verifica que los campos que deben ser unicos (DNI, email y padron) no existan
    en la base para otro usuario
    """
    error = False

    if Alumno.query.filter_by(dni=POST_DNI).first():
        flash("El DNI ya se encuentra registrado para otro usuario.")
        error = True
    
    if Alumno.query.filter_by(dni=POST_email).first():
        flash("El e-mail ya se encuentra registrado para otro usuario.")
        error = True

    if POST_padron and Alumno.query.filter_by(dni=POST_padron).first():
        flash("El padrón ya se encuentra registrado para otro usuario.")
        error = True

    return error