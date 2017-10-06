from app.views.base_view import main_blueprint

from flask import redirect, render_template
from flask import request, url_for

from app.models.carreras_models import Carrera

@main_blueprint.route('/')
def home_page():
    return render_template('pages/home_page.html')


@main_blueprint.route('/buscar_materias')
def buscar_materias_page():
    carreras = Carrera.query.all()
    return render_template('pages/buscar_materias_page.html',
                           carreras=carreras)

@main_blueprint.route('/contacto')
def contacto_page():
    return render_template('pages/contacto_page.html')


@main_blueprint.route('/preguntas_frecuentes')
def preguntas_frecuentes_page():
    return render_template('pages/preguntas_frecuentes_page.html')


@main_blueprint.route('/links_utiles')
def links_utiles_page():
    return render_template('pages/links_utiles_page.html')