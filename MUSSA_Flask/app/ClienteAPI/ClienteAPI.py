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
            response = requests.post(url_servicio, data=parametros, cookies=cookies, headers={"X-CSRFToken": csrf_token})
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

    def obtener_todas_las_carreras(self, cookie):
        url_servicio = self.get_url_get_carreras()
        return self.invocar_get(url_servicio, cookie, {})["carreras"]