from flask import redirect, render_template
from flask import request, url_for

import logging

import requests

from app.API_Rest.services import *
import json


def escribir_resultado_servicio(nombre_servicio, response):
    logging.info('Servicio {} result: {} - {}'.format(nombre_servicio, response, response.text))


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


def invocar_servicio_obtener_carreras_para_una_materia(codigo):
    url = OBTENER_CARRERAS_DONDE_SE_DICTA_LA_MATERIA + "?codigo_materia=" + str(codigo)
    carreras_response = requests.get(url)
    escribir_resultado_servicio('Buscar Carreras donde se dicta una materia', carreras_response)

    carreras = json.loads(carreras_response.text)["carreras"]
    return carreras