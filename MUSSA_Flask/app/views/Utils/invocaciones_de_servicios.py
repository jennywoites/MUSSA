import logging
import requests
from app.API_Rest.services import *
import json


def escribir_resultado_servicio(nombre_servicio, response):
    logging.info('Servicio {} result: {} - {}'.format(nombre_servicio, response, response.text))


def invocar_guardar_horarios_desde_PDF(csrf_token, cookie, ruta, anio, cuatrimestre):
    parametros = {}
    parametros["ruta"] = ruta
    parametros["anio"] = anio
    parametros["cuatrimestre"] = cuatrimestre

    horarios_response = requests.post(GUARDAR_HORARIOS_DESDE_ARCHIVO_PDF_SERVICE,
                                      data=parametros, cookies=cookie, headers={"X-CSRFToken": csrf_token})

    escribir_resultado_servicio('Guardar Horarios desde PDF', horarios_response)
    return json.loads(horarios_response.text)


def invocar_eliminar_materia_alumno(csrf_token, cookie, id_materia):
    parametros = {}
    parametros["id_materia"] = id_materia

    eliminar_materia_response = requests.post(ELIMINAR_MATERIA_ALUMNO_SERVICE, data=parametros,
                                              cookies=cookie, headers={"X-CSRFToken": csrf_token})
    escribir_resultado_servicio('Eliminar Materia Alumno', eliminar_materia_response)
    return json.loads(eliminar_materia_response.text)


def invocar_agregar_materia_alumno(csrf_token, cookie, parametros):
    agregar_materia_alumno_response = requests.post(AGREGAR_MATERIA_ALUMNO_SERVICE, data=parametros,
                                                    cookies=cookie, headers={"X-CSRFToken": csrf_token})
    escribir_resultado_servicio('Agregar Materia Alumno', agregar_materia_alumno_response)
    return json.loads(agregar_materia_alumno_response.text)
