from app.views.base_view import main_blueprint  

from flask import redirect, render_template
from flask import request, url_for

import logging

import requests

from app.models.carreras_models import Carrera, Materia

from app.API_Rest.services import *
import json

@main_blueprint.route('/')
def home_page():
    return render_template('pages/home_page.html')


@main_blueprint.route('/buscar_materias', methods=['GET'])
def buscar_materias_page():
    carreras = invocar_servicio_buscar_carreras()
    return render_template('pages/buscar_materias_page.html',
                carreras= carreras)


@main_blueprint.route('/materias/<int:idMateria>', methods=['GET'])
def materia_page(idMateria):
    materia = invocar_servicio_obtener_materia(idMateria)

    carreras = [{'id': 9, 'nombre': 'Licenciatura cuack :P', 'link': '/materias/2'}]

    correlativas = invocar_servicio_obtener_correlativas(idMateria)

    return render_template('pages/materia_page.html',
                materia=materia,
                carreras=carreras,
                correlativas = correlativas)


@main_blueprint.route('/contacto')
def contacto_page():
    return render_template('pages/contacto_page.html')


@main_blueprint.route('/preguntas_frecuentes')
def preguntas_frecuentes_page():
    return render_template('pages/preguntas_frecuentes_page.html')


@main_blueprint.route('/links_utiles')
def links_utiles_page():
    return render_template('pages/links_utiles_page.html')


def invocar_servicio_buscar_carreras():
    carreras_response = requests.get(BUSCAR_CARRERAS_SERVICE)
    escribir_resultado_servicio('Buscar Carreras', carreras_response)

    carreras = json.loads(carreras_response.text)["carreras"]
    return carreras   


def invocar_servicio_obtener_materia(idMateria):
    url = OBTENER_MATERIA_SERVICE + "?id_materia=" + str(idMateria)
    materia_response = requests.get(url)
    escribir_resultado_servicio('Obtener Materia', materia_response)

    materia = json.loads(materia_response.text)["materia"]
    return materia


def invocar_servicio_obtener_correlativas(idMateria):
    url = OBTENER_MATERIAS_CORRELATIVAS_SERVICE + "?id_materia=" + str(idMateria)
    correlativas_response = requests.get(url)
    escribir_resultado_servicio('Obtener Materias Correlativas', correlativas_response)

    correlativas = json.loads(correlativas_response.text)["correlativas"]
    return correlativas


def escribir_resultado_servicio(nombre_servicio, response):
    logging.info('Servicio {} result: {} - {}'.format(nombre_servicio, response, response.text))