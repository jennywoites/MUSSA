from app.views.base_view import main_blueprint  

from flask import redirect, render_template
from flask import request, url_for

import requests

from app.views.PaginasPublicasViews.buscar_materia_page_view import buscar_materias_page
from app.views.PaginasPublicasViews.materia_page_view import materia_page

@main_blueprint.route('/')
def home_page():
    return render_template('pages/home_page.html')


@main_blueprint.route('/contacto')
def contacto_page():
    return render_template('pages/contacto_page.html')


@main_blueprint.route('/links_utiles')
def links_utiles_page():
    return render_template('pages/links_utiles_page.html')