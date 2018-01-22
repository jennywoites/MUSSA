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


def invocar_agregar_carrera_alumno(csrf_token, cookie, id_carrera):
    parametros = {}
    parametros["id_carrera"] = id_carrera

    agregar_carrera_response = requests.post(AGREGAR_CARRERA_ALUMNO_SERVICE, data=parametros,
                                             cookies=cookie, headers={"X-CSRFToken": csrf_token})
    escribir_resultado_servicio('Agregar Carrera Alumno', agregar_carrera_response)
    return json.loads(agregar_carrera_response.text)


def invocar_eliminar_carrera_alumno(csrf_token, cookie, id_carrera):
    parametros = {}
    parametros["id_carrera"] = id_carrera

    eliminar_carrera_response = requests.post(ELIMINAR_CARRERA_ALUMNO_SERVICE, data=parametros,
                                              cookies=cookie, headers={"X-CSRFToken": csrf_token})
    escribir_resultado_servicio('Eliminar Carrera Alumno', eliminar_carrera_response)
    return json.loads(eliminar_carrera_response.text)


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


def invocar_obtener_encuestas_alumno(cookie, finalizadas):
    parametros = {}
    parametros["finalizadas"] = finalizadas

    encuestas_response = requests.get(OBTENER_ENCUESTAS_ALUMNO_SERVICE, params=parametros, cookies=cookie)
    escribir_resultado_servicio('Obtener Encuestas Alumno', encuestas_response)
    return json.loads(encuestas_response.text)["encuestas"]


def invocar_obtener_encuesta_alumno(cookie, id_encuesta):
    parametros = {}
    parametros["id_encuesta"] = id_encuesta

    encuestas_response = requests.get(OBTENER_ENCUESTAS_ALUMNO_SERVICE, params=parametros, cookies=cookie)
    escribir_resultado_servicio('Obtener Encuestas Alumno', encuestas_response)
    return json.loads(encuestas_response.text)["encuestas"].pop()


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


def invocar_encuesta_alumno_esta_completa(cookie, idEncuestaAlumno):
    parametros = {"id_encuesta": idEncuestaAlumno}
    response = requests.get(ENCUESTA_ALUMNO_ESTA_COMPLETA_SERVICE, params=parametros, cookies=cookie)
    escribir_resultado_servicio('Encuesta Alumno está completa', response)
    return json.loads(response.text)["esta_completa"]
