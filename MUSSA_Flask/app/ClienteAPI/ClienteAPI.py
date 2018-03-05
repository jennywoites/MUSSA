import logging
import requests
import json
from app.DAO.EncuestasDAO import *


class ClienteAPI:
    class __ClienteAPI:
        def __init__(self):
            pass

    instance = None

    def __init__(self):
        if not ClienteAPI.instance:
            ClienteAPI.instance = ClienteAPI.__ClienteAPI()

    HTTP = "http://"
    IP = "localhost:"
    PUERTO = "5000"
    BASE_API = "/api"
    BASE_URL = HTTP + IP + PUERTO + BASE_API

    def escribir_resultado_servicio(self, nombre_servicio, response):
        logging.info('Servicio {} result: {} - {}'.format(nombre_servicio, response, response.text))

    def invocar_get(self, url_servicio, cookies, parametros=None):
        if parametros:
            response = requests.get(url_servicio, params=parametros, cookies=cookies)
        else:
            response = requests.get(url_servicio, cookies=cookies)

        self.escribir_resultado_servicio(url_servicio, response)
        return response.json()

    def invocar_post(self, url_servicio, cookies, csrf_token, parametros=None):
        if parametros:
            response = requests.post(url_servicio, data=parametros, cookies=cookies,
                                     headers={"X-CSRFToken": csrf_token})
        else:
            response = requests.post(url_servicio, cookies=cookies, headers={"X-CSRFToken": csrf_token})

        self.escribir_resultado_servicio(url_servicio, response)
        return response.json()

    def invocar_put(self, url_servicio, cookies, csrf_token, parametros=None):
        if parametros:
            response = requests.put(url_servicio, data=parametros, cookies=cookies,
                                    headers={"X-CSRFToken": csrf_token})
        else:
            response = requests.put(url_servicio, cookies=cookies, headers={"X-CSRFToken": csrf_token})

        self.escribir_resultado_servicio(url_servicio, response)
        return response.json()

    def invocar_delete(self, url_servicio, cookies, csrf_token):
        response = requests.delete(url_servicio, cookies=cookies, headers={"X-CSRFToken": csrf_token})
        self.escribir_resultado_servicio(url_servicio, response)
        return response.json()

    ################################################
    ##                  URLS                      ##
    ################################################

    def get_url_get_docente(self, idDocente):
        """URL: '/api/docente/<int:idDocente>'"""
        return self.BASE_URL + '/docente/' + str(idDocente)

    def get_url_obtener_todos_los_docentes(self):
        """URL: '/api/docente/all"""
        return self.BASE_URL + '/docente/all'

    def get_url_get_tematica(self, idTematica):
        """URL: '/api/tematica/<int:idTematica>"""
        return self.BASE_URL + '/tematica/' + str(idTematica)

    def get_url_obtener_todas_las_tematicas(self):
        """URL: '/api/tematica/all'"""
        return self.BASE_URL + '/tematica/all'

    def get_url_get_carreras(self):
        """URL: '/api/carrera/all'"""
        return self.BASE_URL + '/carrera/all'

    def get_url_get_materia(self, idMateria):
        """URL: '/api/materia/<int:idMateria>'"""
        return self.BASE_URL + '/materia/' + str(idMateria)

    def get_url_get_materias(self):
        """URL: '/api/materia'"""
        return self.BASE_URL + '/materia/all'

    def get_url_materias_correlativas(self, idMateria):
        """URL: '/api/materia/<int:idMateria>/correlativas'"""
        return self.BASE_URL + '/materia/' + str(idMateria) + '/correlativas'

    def get_url_get_curso(self, idCurso):
        """URL: '/api/curso/<int:idCurso>'"""
        return self.BASE_URL + '/curso/' + str(idCurso)

    def get_url_all_cursos(self):
        """URL: '/api/curso/all'"""
        return self.BASE_URL + '/curso/all'

    def get_url_horarios_curso_PDF(self):
        """URL: '/api/curso/all/horarios/uploadPDF'"""
        return self.BASE_URL + '/curso/all/horarios/uploadPDF'

    def get_url_preguntas_encuesta(self):
        """URL: '/api/encuesta/preguntas'"""
        return self.BASE_URL + '/encuesta/preguntas'

    def get_url_get_resultados_encuesta(self, idCurso):
        """URLs:
        '/api/encuesta/resultados/curso/<int:idCurso>'"""
        return self.BASE_URL + '/encuesta/resultados/curso/' + str(idCurso)

    def get_url_get_resultados_docente_encuesta(self, idDocente):
        """URLs:
        '/api/encuesta/resultados/docente/<int:idDocente>'"""
        return self.BASE_URL + '/encuesta/resultados/docente/' + str(idDocente)

    def get_url_get_cuatrimestres_resultados_encuesta(self, idCurso):
        """URLs:
        '/api/encuesta/resultados/curso/<int:idCurso>/cuatrimestres'"""
        return self.BASE_URL + '/encuesta/resultados/curso/' + str(idCurso) + '/cuatrimestres'

    def get_url_get_cuatrimestres_resultados_encuesta_docente(self, idDocente):
        """URLs:
        '/api/encuesta/resultados/docente/<int:idDocente>/cuatrimestres'"""
        return self.BASE_URL + '/encuesta/resultados/docente/' + str(idDocente) + '/cuatrimestres'

    def get_url_preguntas_resultados_encuesta(self):
        """URL: '/api/encuesta/resultados/preguntas'"""
        return self.BASE_URL + '/encuesta/resultados/preguntas'

    def get_url_get_alumno(self):
        """URL: '/api/alumno'"""
        return self.BASE_URL + '/alumno'

    def get_url_get_materia_alumno(self, idMateriaAlumno=None):
        """URLs:
        '/api/alumno/materia'
        '/api/alumno/materia/<int:idMateriaAlumno>'"""
        return self.BASE_URL + '/alumno/materia' + ("/" + str(idMateriaAlumno) if idMateriaAlumno else '')

    def get_url_get_materias_alumno(self):
        """URL: '/api/alumno/materia/all'"""
        return self.BASE_URL + '/alumno/materia/all'

    def get_url_get_materias_pendientes_alumno(self):
        """URL: '/api/alumno/materia/pendientes'"""
        return self.BASE_URL + '/alumno/materia/pendientes'

    def get_url_get_carreras_alumno(self):
        """URL: '/api/alumno/carrera/all'"""
        return self.BASE_URL + '/alumno/carrera/all'

    def get_url_get_encuesta_alumno(self, idEncuestaAlumno):
        """URL: '/api/alumno/encuesta/<int:idEncuestaAlumno>'"""
        return self.BASE_URL + '/alumno/encuesta/' + str(idEncuestaAlumno)

    def get_url_get_encuestas_alumno(self):
        """URL: '/api/alumno/encuesta/all'"""
        return self.BASE_URL + '/alumno/encuesta/all'

    def get_url_get_encuesta_alumno_esta_completa(self, idEncuestaAlumno):
        """URL: '/api/alumno/encuesta/<int:idEncuestaAlumno>/completa'"""
        return self.BASE_URL + '/alumno/encuesta/' + str(idEncuestaAlumno) + '/completa'

    def get_url_get_respuestas_encuesta_alumno(self, idEncuestaAlumno):
        """URL: '/api/alumno/encuesta/<int:idEncuestaAlumno>/respuestas'"""
        return self.BASE_URL + '/alumno/encuesta/' + str(idEncuestaAlumno) + '/respuestas'

    def get_url_carrera_alumno(self, idCarrera=None):
        """URLs:
        '/api/alumno/carrera',
        '/api/alumno/carrera/<int:idCarrera>'
        """
        return self.BASE_URL + '/alumno/carrera' + ('/' + str(idCarrera) if idCarrera else '')

    def get_url_get_all_planes_de_estudio_alumno(self):
        """URL: '/api/alumno/planDeEstudios/all'"""
        return self.BASE_URL + '/alumno/planDeEstudios/all'

    def get_url_get_plan_de_estudio_alumno(self, idPlanDeEstudios):
        """URL: '/api/alumno/planDeEstudios/<int:idPlanDeEstudios>'"""
        return self.BASE_URL + '/alumno/planDeEstudios/' + str(idPlanDeEstudios)

    ################################################
    ##              Servicios DOCENTE             ##
    ################################################

    def get_docente(self, cookie, idDocente):
        url_servicio = self.get_url_get_docente(idDocente)
        return self.invocar_get(url_servicio, cookie)

    def modificar_docente(self, cookie, csrf_token, idDocente, apellido, nombre, l_ids_cursos):
        url_servicio = self.get_url_get_docente(idDocente)

        parametros = {}
        parametros["apellido"] = apellido
        parametros["nombre"] = nombre
        parametros["l_ids_cursos"] = json.dumps(l_ids_cursos)

        return self.invocar_post(url_servicio, cookie, csrf_token, parametros)

    def eliminar_docente(self, cookie, csrf_token, idDocente):
        url_servicio = self.get_url_get_docente(idDocente)
        return self.invocar_delete(url_servicio, cookie, csrf_token)

    def obtener_todos_los_docentes(self, cookie):
        url_servicio = self.get_url_obtener_todos_los_docentes()
        return self.invocar_get(url_servicio, cookie)["docentes"]

    ################################################
    ##            Servicios TEMATICAS             ##
    ################################################

    def get_tematica(self, cookie, idTematica):
        url_servicio = self.get_url_get_tematica(idTematica)
        return self.invocar_get(url_servicio, cookie)

    def obtener_todas_las_tematicas(self, cookie, solo_verificadas=True):
        url_servicio = self.get_url_obtener_todas_las_tematicas()

        parametros = {}
        parametros["solo_verificadas"] = solo_verificadas
        return self.invocar_get(url_servicio, cookie, parametros)["tematicas"]

    ################################################
    ##            Servicios CARRERAS              ##
    ################################################

    def obtener_todas_las_carreras(self, cookie, codigo_materia=''):
        url_servicio = self.get_url_get_carreras()

        parametros = {}
        if codigo_materia:
            parametros["codigo_materia"] = codigo_materia

        return self.invocar_get(url_servicio, cookie, parametros)["carreras"]

    ################################################
    ##              Servicios MATERIA             ##
    ################################################

    def get_materia(self, cookie, idMateria):
        url_servicio = self.get_url_get_materia(idMateria)
        return self.invocar_get(url_servicio, cookie)

    def obtener_materias_correlativas(self, cookie, idMateria):
        url_servicio = self.get_url_materias_correlativas(idMateria)
        return self.invocar_get(url_servicio, cookie)["correlativas"]

    def obtener_todas_las_materias(self, cookie, codigo_materia='', nombre='', ids_carreras=[]):
        url_servicio = self.get_url_get_materias()

        parametros = {}
        if codigo_materia:
            parametros["codigo"] = codigo_materia
        if nombre:
            parametros["nombre"] = nombre
        if ids_carreras:
            parametros["ids_carreras"] = json.dumps(ids_carreras)

        return self.invocar_get(url_servicio, cookie, parametros)["materias"]

    ################################################
    ##              Servicios CURSO               ##
    ################################################

    def get_curso(self, cookie, idCurso):
        url_servicio = self.get_url_get_curso(idCurso)
        return self.invocar_get(url_servicio, cookie)

    def obtener_docentes_del_curso(self, cookie, idCurso):
        curso = self.get_curso(cookie, idCurso)
        return curso["datos_docentes"]

    def modificar_curso(self, cookie, idCurso, ids_carreras, primer_cuatrimestre, segundo_cuatrimestre, ids_docentes,
                        horarios):
        url_servicio = self.get_url_get_curso(idCurso)

        parametros = {}
        parametros["ids_carreras"] = json.dumps(ids_carreras)
        parametros["primer_cuatrimestre"] = primer_cuatrimestre
        parametros["segundo_cuatrimestre"] = segundo_cuatrimestre
        parametros["ids_docentes"] = json.dumps(ids_docentes)
        parametros["horarios"] = json.dumps(horarios)

        return self.invocar_post(url_servicio, cookie, parametros)

    def obtener_cursos_con_filtros(self, cookie, nombre_curso='', codigo_materia='', id_carrera='', filtrar_cursos=''):
        url_servicio = self.get_url_all_cursos()

        parametros = {}
        if nombre_curso:
            parametros["nombre_curso"] = nombre_curso
        if codigo_materia:
            parametros["codigo_materia"] = codigo_materia
        if id_carrera:
            parametros["id_carrera"] = id_carrera
        if filtrar_cursos:
            parametros["filtrar_cursos"] = filtrar_cursos

        return self.invocar_get(url_servicio, cookie, parametros)["cursos"]

    def obtener_todos_los_cursos_existentes(self, cookie, nombre_curso='', codigo_materia='', id_carrera=''):
        return self.obtener_cursos_con_filtros(cookie, nombre_curso, codigo_materia, id_carrera, filtrar_cursos=False)

    def guardar_horarios_PDF(self, cookie, csrf_token, ruta, anio, cuatrimestre):
        url_servicio = self.get_url_horarios_curso_PDF()

        parametros = {}
        parametros["ruta"] = ruta
        parametros["anio"] = anio
        parametros["cuatrimestre"] = cuatrimestre

        return self.invocar_post(url_servicio, cookie, csrf_token, parametros)

    ################################################
    ##            Servicios ENCUESTA              ##
    ################################################

    def obtener_preguntas_encuesta(self, cookie, l_categorias=[]):
        url_servicio = self.get_url_preguntas_encuesta()

        parametros = {}
        if l_categorias:
            parametros["categorias"] = json.dumps(l_categorias)

        response = self.invocar_get(url_servicio, cookie, parametros)
        return response["preguntas"]

    ################################################
    ##       Servicios RESUTADOS ENCUESTA         ##
    ################################################

    def get_cuatrimestres_con_resultados_encuesta_para_un_curso(self, cookies, idCurso):
        url_servicio = self.get_url_get_cuatrimestres_resultados_encuesta(idCurso)
        return self.invocar_get(url_servicio, cookies)["cuatrimestres"]

    def get_cuatrimestres_con_resultados_encuesta_para_un_docente(self, cookies, idDocente):
        url_servicio = self.get_url_get_cuatrimestres_resultados_encuesta_docente(idDocente)
        return self.invocar_get(url_servicio, cookies)["cuatrimestres"]

    def obtener_preguntas_resultados_encuesta(self, cookie, l_categorias=[]):
        url_servicio = self.get_url_preguntas_resultados_encuesta()

        parametros = {}
        if l_categorias:
            parametros["categorias"] = json.dumps(l_categorias)

        response = self.invocar_get(url_servicio, cookie, parametros)
        return response["preguntas"]

    def obtener_repuestas_resultados_encuesta(self, cookies, idCurso, num_categoria, anio='', cuatrimestre=''):
        url_servicio = self.get_url_get_resultados_encuesta(idCurso)

        parametros = {}
        if anio:
            parametros["anio"] = anio
        if cuatrimestre:
            parametros["cuatrimestre"] = cuatrimestre

        preguntas = self.obtener_preguntas_encuesta(cookies, [num_categoria])
        ids_preguntas = []
        for pregunta in preguntas:
            ids_preguntas.append(pregunta["pregunta_id"])
            if pregunta["tipo_num"] == SI_NO:
                for subpregunta in (pregunta["rta_si"] + pregunta["rta_no"]):
                    ids_preguntas.append(subpregunta["pregunta_id"])
        if ids_preguntas:
            parametros["ids_preguntas"] = json.dumps(ids_preguntas)

        response = self.invocar_get(url_servicio, cookies, parametros)
        return response["respuestas_encuestas"]

    def obtener_repuestas_resultados_docentes_encuesta(self, cookies, idDocente, anio='', cuatrimestre=''):
        url_servicio = self.get_url_get_resultados_docente_encuesta(idDocente)

        parametros = {}
        if anio:
            parametros["anio"] = anio
        if cuatrimestre:
            parametros["cuatrimestre"] = cuatrimestre

        response = self.invocar_get(url_servicio, cookies, parametros)
        return response["respuestas_encuestas"]

    ################################################
    ##            Servicios ALUMNO                ##
    ################################################

    def obtener_alumno(self, cookie):
        url_servicio = self.get_url_get_alumno()
        return self.invocar_get(url_servicio, cookie)["alumno"]

    def modificar_alumno(self, cookie, padron=''):
        url_servicio = self.get_url_get_alumno()
        parametros = {}
        parametros["padron"] = padron
        return self.invocar_post(url_servicio, cookie, parametros)

    def obtener_materia_alumno(self, cookie, idMateriaAlumno):
        url_servicio = self.get_url_get_materia_alumno(idMateriaAlumno)
        return self.invocar_get(url_servicio, cookie)["materia_alumno"]

    def eliminar_materia_alumno(self, cookie, csrf_token, idMateriaAlumno):
        url_servicio = self.get_url_get_materia_alumno(idMateriaAlumno)
        return self.invocar_delete(url_servicio, cookie, csrf_token)

    def agregar_materia_alumno(self, cookie, csrf_token, idMateriaAlumno, idCurso, estado, cuatrimestre_aprobacion='',
                               anio_aprobacion='', fecha_aprobacion='', forma_aprobacion='', calificacion='',
                               acta_resolucion=''):
        url_servicio = self.get_url_get_materia_alumno()
        return self.aux_modificar_materia_alumno(self.invocar_put, url_servicio, cookie, csrf_token, idMateriaAlumno,
                                                 idCurso, estado, cuatrimestre_aprobacion, anio_aprobacion,
                                                 fecha_aprobacion, forma_aprobacion, calificacion, acta_resolucion)

    def modificar_materia_alumno(self, cookie, csrf_token, idMateriaAlumno, estado, cuatrimestre_aprobacion='',
                                 anio_aprobacion='', fecha_aprobacion='', forma_aprobacion='', calificacion='',
                                 acta_resolucion=''):

        idCurso = None  # No se permite modificar el curso
        url_servicio = self.get_url_get_materia_alumno(idMateriaAlumno)

        return self.aux_modificar_materia_alumno(self.invocar_post, url_servicio, cookie, csrf_token, idMateriaAlumno,
                                                 idCurso, estado, cuatrimestre_aprobacion, anio_aprobacion,
                                                 fecha_aprobacion, forma_aprobacion, calificacion, acta_resolucion)

    def aux_modificar_materia_alumno(self, funcion_a_invocar, url_servicio, cookie, csrf_token, idMateriaAlumno,
                                     idCurso, estado, cuatrimestre_aprobacion='', anio_aprobacion='',
                                     fecha_aprobacion='', forma_aprobacion='', calificacion='', acta_resolucion=''):
        parametros = {}
        parametros["idMateriaAlumno"] = idMateriaAlumno
        parametros["estado"] = estado

        if idCurso:
            parametros["idCurso"] = idCurso

        if cuatrimestre_aprobacion:
            parametros["cuatrimestre_aprobacion"] = cuatrimestre_aprobacion

        if anio_aprobacion:
            parametros["anio_aprobacion"] = anio_aprobacion

        if fecha_aprobacion:
            parametros["fecha_aprobacion"] = fecha_aprobacion

        if forma_aprobacion:
            parametros["forma_aprobacion"] = forma_aprobacion

        if calificacion:
            parametros["calificacion"] = calificacion

        if acta_resolucion:
            parametros["acta_resolucion"] = acta_resolucion

        return funcion_a_invocar(url_servicio, cookie, csrf_token, parametros)

    def obtener_materias_alumno(self, cookie, estados=[]):
        url_servicio = self.get_url_get_materias_alumno()

        parametros = {}
        parametros["estados"] = json.dumps(estados)

        return self.invocar_get(url_servicio, cookie, parametros)["materias_alumno"]

    def obtener_materias_pendientes(self, cookie, id_carrera=None):
        url_servicio = self.get_url_get_materias_pendientes_alumno()

        parametros = {}
        if id_carrera:
            parametros["id_carrera"] = id_carrera

        return self.invocar_get(url_servicio, cookie, parametros)["materias_alumno"]

    def obtener_carreras_alumno(self, cookie):
        url_servicio = self.get_url_get_carreras_alumno()
        return self.invocar_get(url_servicio, cookie)["carreras"]

    def obtener_encuesta_alumno(self, cookie, idEncuestaAlumno):
        url_servicio = self.get_url_get_encuesta_alumno(idEncuestaAlumno)
        return self.invocar_get(url_servicio, cookie)

    def obtener_todas_las_encuestas_alumno(self, cookie, finalizada=None):
        url_servicio = self.get_url_get_encuestas_alumno()

        parametros = {}
        if finalizada is not None:
            parametros["finalizada"] = finalizada

        return self.invocar_get(url_servicio, cookie, parametros)["encuestas"]

    def finalizar_encuesta_alumno(self, cookie, idEncuestaAlumno):
        url_servicio = self.get_url_get_encuesta_alumno(idEncuestaAlumno)

        parametros = {}
        parametros["finalizada"] = True

        return self.invocar_post(url_servicio, cookie)

    def encuesta_alumno_esta_completa(self, cookie, idEncuestaAlumno):
        url_servicio = self.get_url_get_encuesta_alumno_esta_completa(idEncuestaAlumno)
        return self.invocar_get(url_servicio, cookie)["esta_completa"]

    def agregar_carrera_alumno(self, cookie, csrf_token, idCarrera):
        url_servicio = self.get_url_carrera_alumno()

        parametros = {}
        parametros["idCarrera"] = idCarrera

        return self.invocar_put(url_servicio, cookie, csrf_token, parametros)

    def eliminar_carrera_alumno(self, cookie, csrf_token, idCarrera):
        url_servicio = self.get_url_carrera_alumno(idCarrera)
        return self.invocar_delete(url_servicio, cookie, csrf_token)

    def obtener_respuestas_encuesta_alumno(self, cookie, idEncuestaAlumno, preguntas=[]):
        url_servicio = self.get_url_get_respuestas_encuesta_alumno(idEncuestaAlumno)

        parametros = {}
        ids_preguntas = []
        for pregunta in preguntas:
            ids_preguntas.append(pregunta["pregunta_id"])
            if pregunta["tipo_num"] == SI_NO:
                for subpregunta in (pregunta["rta_si"] + pregunta["rta_no"]):
                    ids_preguntas.append(subpregunta["pregunta_id"])
        if ids_preguntas:
            parametros["ids_preguntas"] = json.dumps(ids_preguntas)

        return self.invocar_get(url_servicio, cookie, parametros)["respuestas_encuestas"]

    def guardar_respuestas_encuesta_alumno(self, cookie, csrf_token, idEncuestaAlumno, categoria, respuestas):
        url_servicio = self.get_url_get_respuestas_encuesta_alumno(idEncuestaAlumno)

        parametros = {}
        parametros["categoria"] = categoria
        parametros["respuestas"] = json.dumps(respuestas)

        return self.invocar_post(url_servicio, cookie, csrf_token, parametros)

    def obtener_planes_de_estudio_alumno(self, cookie):
        url_servicio = self.get_url_get_all_planes_de_estudio_alumno()
        return self.invocar_get(url_servicio, cookie)["planes_de_estudio"]

    def obtener_plan_de_estudios_alumno(self, cookie, idPlanDeEstudios):
        url_servicio = self.get_url_get_plan_de_estudio_alumno(idPlanDeEstudios)
        return self.invocar_get(url_servicio, cookie)["plan_de_estudio"]

    def eliminar_plan_de_estudios_alumno(self, cookie, csrf_token, idPlanDeEstudios):
        url_servicio = self.get_url_get_plan_de_estudio_alumno(idPlanDeEstudios)
        return self.invocar_delete(url_servicio, cookie, csrf_token)
