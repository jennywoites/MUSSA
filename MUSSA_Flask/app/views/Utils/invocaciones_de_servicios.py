from flask import redirect, render_template
from flask import request, url_for

import logging

import requests

from app.API_Rest.services import *
import json


def escribir_resultado_servicio(nombre_servicio, response):
    logging.info('Servicio {} result: {} - {}'.format(nombre_servicio, response, response.text))


def invocar_servicio_buscar_carreras(cookie):
    carreras_response = requests.get(BUSCAR_CARRERAS_SERVICE, cookies=cookie)
    escribir_resultado_servicio('Buscar Carreras', carreras_response)

    return json.loads(carreras_response.text)["carreras"]


def invocar_servicio_obtener_materia(cookie, idMateria):
    parametros = {}
    parametros["id_materia"] = idMateria

    materia_response = requests.get(OBTENER_MATERIA_SERVICE, params=parametros, cookies=cookie)
    escribir_resultado_servicio('Obtener Materia', materia_response)

    return json.loads(materia_response.text)["materia"]


def invocar_servicio_obtener_correlativas(cookie, idMateria):
    parametros = {}
    parametros["id_materia"] = idMateria

    correlativas_response = requests.get(OBTENER_MATERIAS_CORRELATIVAS_SERVICE, params=parametros, cookies=cookie)
    escribir_resultado_servicio('Obtener Materias Correlativas', correlativas_response)

    return json.loads(correlativas_response.text)["correlativas"]


def invocar_servicio_obtener_carreras_para_una_materia(cookie, codigo):
    parametros = {}
    parametros["codigo_materia"] = codigo

    carreras_response = requests.get(OBTENER_CARRERAS_DONDE_SE_DICTA_LA_MATERIA_SERVICE, params=parametros, cookies=cookie)
    escribir_resultado_servicio('Buscar Carreras donde se dicta una materia', carreras_response)

    return json.loads(carreras_response.text)["carreras"]


def invocar_guardar_horarios_desde_PDF(cookie, ruta, anio, cuatrimestre):
    parametros = {}
    parametros["ruta"] = ruta
    parametros["anio"] = anio
    parametros["cuatrimestre"] = cuatrimestre

    horarios_response = requests.get(GUARDAR_HORARIOS_DESDE_ARCHIVO_PDF_SERVICE, params=parametros, cookies=cookie)
    print(horarios_response)

    escribir_resultado_servicio('Guardar Horarios desde PDF', horarios_response)
    return json.loads(horarios_response.text)


def invocar_buscar_cursos(cookie, codigo_materia='', nombre_curso=''):
    parametros = {}
    if codigo_materia: parametros["codigo_materia"] = codigo_materia
    if nombre_curso: parametros["nombre_curso"] = nombre_curso

    cursos_response = requests.get(BUSCAR_CURSOS_SERVICE, params=parametros, cookies=cookie)
    escribir_resultado_servicio('Buscar Cursos', cursos_response)
    return json.loads(cursos_response.text)["cursos"]


def invocar_servicio_obtener_curso(cookie, codigo_materia, id_carrera):
    parametros = {}
    parametros["codigo_materia"] = codigo_materia
    parametros["id_carrera"] = id_carrera

    cursos_response = requests.get(BUSCAR_CURSOS_SERVICE, params=parametros, cookies=cookie)
    escribir_resultado_servicio('Buscar Cursos', cursos_response)
    return json.loads(cursos_response.text)["cursos"]    

