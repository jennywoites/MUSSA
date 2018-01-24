import logging
import requests
from app.API_Rest.services import *
import json


def invocar_guardar_horarios_desde_PDF(csrf_token, cookie, ruta, anio, cuatrimestre):
    parametros = {}
    parametros["ruta"] = ruta
    parametros["anio"] = anio
    parametros["cuatrimestre"] = cuatrimestre

    horarios_response = requests.post(GUARDAR_HORARIOS_DESDE_ARCHIVO_PDF_SERVICE,
                                      data=parametros, cookies=cookie, headers={"X-CSRFToken": csrf_token})

    return json.loads(horarios_response.text)


def invocar_agregar_materia_alumno(csrf_token, cookie, parametros):
    agregar_materia_alumno_response = requests.post(AGREGAR_MATERIA_ALUMNO_SERVICE, data=parametros,
                                                    cookies=cookie, headers={"X-CSRFToken": csrf_token})
    return json.loads(agregar_materia_alumno_response.text)
