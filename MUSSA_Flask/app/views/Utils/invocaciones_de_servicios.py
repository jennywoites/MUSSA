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

    return json.loads(carreras_response.text)["carreras"]


def invocar_servicio_obtener_materia(idMateria):
    url = OBTENER_MATERIA_SERVICE + "?id_materia=" + str(idMateria)
    materia_response = requests.get(url)
    escribir_resultado_servicio('Obtener Materia', materia_response)

    return json.loads(materia_response.text)["materia"]


def invocar_servicio_obtener_correlativas(idMateria):
    url = OBTENER_MATERIAS_CORRELATIVAS_SERVICE + "?id_materia=" + str(idMateria)
    correlativas_response = requests.get(url)
    escribir_resultado_servicio('Obtener Materias Correlativas', correlativas_response)

    return json.loads(correlativas_response.text)["correlativas"]


def invocar_servicio_obtener_carreras_para_una_materia(codigo):
    url = OBTENER_CARRERAS_DONDE_SE_DICTA_LA_MATERIA_SERVICE + "?codigo_materia=" + str(codigo)
    carreras_response = requests.get(url)
    escribir_resultado_servicio('Buscar Carreras donde se dicta una materia', carreras_response)

    return json.loads(carreras_response.text)["carreras"]


def invocar_guardar_horarios_desde_PDF(ruta, cuatrimestre):
    parametros = "ruta=" + ruta + "&cuatrimestre=" + str(cuatrimestre)
    url = GUARDAR_HORARIOS_DESDE_ARCHIVO_PDF_SERVICE + "?" + parametros
    horarios_response = requests.get(url)
    escribir_resultado_servicio('Guardar Horarios desde PDF', horarios_response)


def invocar_buscar_cursos(codigo_materia='', nombre_curso=''):
    parametros = "codigo_materia=" + str(codigo_materia) if codigo_materia else ""
    parametros = parametros + "&" if parametros and nombre_curso else parametros
    parametros = parametros + "nombre_curso=" + str(nombre_curso) if nombre_curso else parametros

    url = BUSCAR_CURSOS_SERVICE + "?" + parametros
    cursos_response = requests.get(url)
    escribir_resultado_servicio('Buscar Cursos', cursos_response)
    return json.loads(cursos_response.text)["cursos"]
