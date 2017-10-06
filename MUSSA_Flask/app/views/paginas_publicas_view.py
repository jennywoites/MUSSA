from app.views.base_view import main_blueprint

from flask import redirect, render_template
from flask import request, url_for

import requests

from app.models.carreras_models import Carrera, Materia


@main_blueprint.route('/')
def home_page():
    return render_template('pages/home_page.html')


@main_blueprint.route('/buscar_materias', methods=['GET'])
def buscar_materias_page():
    #carreras_response = requests.get('http://localhost:5000/api/BuscarCarreras')
    #print(carreras_response)
    carreras = Carrera.query.all()

    materias = []

    #Ver como saber si esta o no el form con datos
    if request.form:
        print(request.form["codigo_materia"])
    show = True

    if show:
        q_codigo = "7540"
        q_nombre = ""
        q_carreras = ["10"]

        query = Materia.query
        if q_codigo: query = query.filter_by(codigo = q_codigo)
        if q_nombre: query = query.filter_by(nombre = Materia.nombre.like("%" + q_nombre + "%"))

        materias = query.order_by(Materia.codigo.asc()).all()
    
    return render_template('pages/buscar_materias_page.html',
                show_results = show,
                carreras= carreras,
                materias = materias)


@main_blueprint.route('/contacto')
def contacto_page():
    return render_template('pages/contacto_page.html')


@main_blueprint.route('/preguntas_frecuentes')
def preguntas_frecuentes_page():
    return render_template('pages/preguntas_frecuentes_page.html')


@main_blueprint.route('/links_utiles')
def links_utiles_page():
    return render_template('pages/links_utiles_page.html')