from app.views.base_view import main_blueprint

from flask import render_template

from app.views.PaginasPublicasViews.buscar_materia_page_view import buscar_materias_page
from app.views.PaginasPublicasViews.materia_page_view import materia_page
from app.views.PaginasPublicasViews.comisiones_por_carrera_view import comisiones_por_carrera_page
from app.views.PaginasPublicasViews.links_utiles_view import links_utiles_page
from app.views.PaginasPublicasViews.resultados_encuestas_view import *


@main_blueprint.route('/')
def home_page():
    return render_template('pages/home_page.html')


@main_blueprint.route('/contacto')
def contacto_page():
    return render_template('pages/contacto_page.html')
