import logging
import requests
import json


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

    def get_url_preguntas_encuesta(self):
        """URL: '/api/encuesta/preguntas'"""
        return self.BASE_URL + '/encuesta/preguntas'

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
            parametros["codigo_materia"] = codigo_materia
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

        response = self.invocar_get(url_servicio, cookie, parametros)
        return response["cursos"]

    def obtener_todos_los_cursos_existentes(self, cookie, nombre_curso='', codigo_materia='', id_carrera=''):
        return self.obtener_cursos_con_filtros(cookie, nombre_curso, codigo_materia, id_carrera, filtrar_cursos=False)

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
