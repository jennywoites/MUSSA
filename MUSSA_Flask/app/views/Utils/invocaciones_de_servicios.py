import logging
import requests
from app.API_Rest.services import *
import json
from app.DAO.EncuestasDAO import *


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


def invocar_obtener_respuestas_encuesta_alumno(cookie, id_encuesta, preguntas):
    parametros = {}
    parametros["id_encuesta"] = id_encuesta

    ids_preguntas = ""
    for pregunta in preguntas:
        ids_preguntas += str(pregunta["pregunta_id"]) + ";"
        if pregunta["tipo_num"] == SI_NO:
            for subpregunta in (pregunta["rta_si"] + pregunta["rta_no"]):
                ids_preguntas += str(subpregunta["pregunta_id"]) + ";"
    parametros["ids_preguntas"] = ids_preguntas[:-1]

    respuestas_response = requests.get(OBTENER_RESPUESTAS_ALUMNO_PARA_PREGUNTAS_ESPECIFICAS_SERVICE,
                                       params=parametros, cookies=cookie)
    escribir_resultado_servicio('Obtener Respuestas Alumno para preguntas específicas', respuestas_response)
    return json.loads(respuestas_response.text)["respuestas_encuestas"]
