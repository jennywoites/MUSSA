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

    carreras_response = requests.get(OBTENER_CARRERAS_DONDE_SE_DICTA_LA_MATERIA_SERVICE, params=parametros,
                                     cookies=cookie)
    escribir_resultado_servicio('Buscar Carreras donde se dicta una materia', carreras_response)

    return json.loads(carreras_response.text)["carreras"]


def invocar_guardar_horarios_desde_PDF(csrf_token, cookie, ruta, anio, cuatrimestre):
    parametros = {}
    parametros["ruta"] = ruta
    parametros["anio"] = anio
    parametros["cuatrimestre"] = cuatrimestre

    horarios_response = requests.post(GUARDAR_HORARIOS_DESDE_ARCHIVO_PDF_SERVICE,
                                      data=parametros, cookies=cookie, headers={"X-CSRFToken": csrf_token})

    escribir_resultado_servicio('Guardar Horarios desde PDF', horarios_response)
    return json.loads(horarios_response.text)


def invocar_buscar_cursos(cookie, codigo_materia='', nombre_curso='', id_curso=''):
    parametros = {}
    if codigo_materia: parametros["codigo_materia"] = codigo_materia
    if nombre_curso: parametros["nombre_curso"] = nombre_curso
    if id_curso: parametros["id_curso"] = id_curso
    parametros["filtrar_cursos"] = False

    cursos_response = requests.get(BUSCAR_CURSOS_SERVICE, params=parametros, cookies=cookie)
    escribir_resultado_servicio('Buscar Cursos', cursos_response)
    return json.loads(cursos_response.text)["cursos"]


def invocar_servicio_obtener_curso(cookie, codigo_materia='', id_carrera=''):
    parametros = {}
    parametros["filtrar_cursos"] = True

    if codigo_materia:
        parametros["codigo_materia"] = codigo_materia

    if id_carrera:
        parametros["id_carrera"] = id_carrera

    cursos_response = requests.get(BUSCAR_CURSOS_SERVICE, params=parametros, cookies=cookie)
    escribir_resultado_servicio('Buscar Cursos', cursos_response)
    return json.loads(cursos_response.text)["cursos"]


def invocar_obtener_padron_alumno(cookie):
    padron_response = requests.get(OBTENER_PADRON_ALUMNO_SERVICE, cookies=cookie)
    escribir_resultado_servicio('Obtener Padron Alumno', padron_response)
    return json.loads(padron_response.text)["padron"]


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


def invocar_obtener_carreras_alumno(cookie):
    carreras_response = requests.get(OBTENER_CARRERAS_ALUMNO_SERVICE, cookies=cookie)
    escribir_resultado_servicio('Obtener Carreras Alumno', carreras_response)
    return json.loads(carreras_response.text)["carreras"]


def invocar_obtener_materias_alumno(cookie, estados):
    parametros = {}
    estados_text = ""
    for estado in estados:
        estados_text += str(estado) + ";"
    parametros["estados"] = estados_text[:-1]

    materias_alumno_response = requests.get(OBTENER_MATERIAS_ALUMNO_SERVICE, params=parametros, cookies=cookie)
    escribir_resultado_servicio('Obtener Materias Alumno', materias_alumno_response)
    return json.loads(materias_alumno_response.text)["materias"]


def invocar_obtener_materia_alumno(cookie, idMateriaAlumno):
    parametros = {}
    parametros["id_materia_alumno"] = idMateriaAlumno

    materias_alumno_response = requests.get(OBTENER_MATERIAS_ALUMNO_SERVICE, params=parametros, cookies=cookie)
    escribir_resultado_servicio('Obtener Materias Alumno', materias_alumno_response)
    return json.loads(materias_alumno_response.text)["materias"]


def invocar_agregar_materia_alumno(csrf_token, cookie, parametros):
    agregar_materia_alumno_response = requests.post(AGREGAR_MATERIA_ALUMNO_SERVICE, data=parametros,
                                                    cookies=cookie, headers={"X-CSRFToken": csrf_token})
    escribir_resultado_servicio('Agregar Materia Alumno', agregar_materia_alumno_response)
    return json.loads(agregar_materia_alumno_response.text)


def invocar_servicio_obtener_preguntas_encuesta(cookie, categorias):
    parametros = {}
    l_categorias = ""
    for categoria in categorias:
        l_categorias += str(categoria) + ";"
    parametros["categorias"] = l_categorias[:-1]

    carreras_response = requests.get(OBTENER_PREGUNTAS_ENCUESTA_SERVICE, params=parametros, cookies=cookie)
    escribir_resultado_servicio('Obtener preguntas encuesta', carreras_response)

    return json.loads(carreras_response.text)["preguntas"]


def invocar_obtener_docentes_del_curso(cookie, id_curso):
    parametros = {}
    parametros["id_curso"] = id_curso

    docentes_response = requests.get(OBTENER_DOCENTES_CURSO_SERVICE, params=parametros, cookies=cookie)
    escribir_resultado_servicio('Obtener Docentes del Curso', docentes_response)
    return json.loads(docentes_response.text)["docentes"]


def invocar_obtener_todos_los_docentes(cookie):
    docentes_response = requests.get(OBTENER_DOCENTES_SERVICE, cookies=cookie)
    escribir_resultado_servicio('Obtener Docentes', docentes_response)
    return json.loads(docentes_response.text)["docentes"]


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


def invocar_servicio_buscar_materias(cookie, carrera):
    parametros = {}
    parametros["carreras"] = carrera

    materias_response = requests.get(BUSCAR_MATERIAS_SERVICE, params=parametros, cookies=cookie)
    escribir_resultado_servicio('Buscar Materias', materias_response)

    return json.loads(materias_response.text)["materias"]
