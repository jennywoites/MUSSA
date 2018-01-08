import logging
import requests


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

    ################################################
    ##                  URLS                      ##
    ################################################

    def get_url_get_docente(self, idDocente):
        """URL: '/api/docente/<int:idDocente>'"""
        return self.BASE_URL + '/docente/' + str(idDocente)

    def get_url_obtener_todos_los_docentes(self):
        """URL: '/api/docente/all"""
        return self.BASE_URL + '/docente/all'

    ################################################
    ##                  Servicios                 ##
    ################################################

    def get_docente(self, cookie, idDocente):
        """URL: '/api/docente/<int:idDocente>'"""
        OBTENER_DOCENTE_SERVICE = self.get_url_get_docente(idDocente)

        docentes_response = requests.get(OBTENER_DOCENTE_SERVICE, cookies=cookie)
        self.escribir_resultado_servicio(OBTENER_DOCENTE_SERVICE, docentes_response)
        return docentes_response.json()

    def obtener_todos_los_docentes(self, cookie):
        OBTENER_TODOS_LOS_DOCENTES_SERVICE = self.get_url_obtener_todos_los_docentes()
        docentes_response = requests.get(OBTENER_TODOS_LOS_DOCENTES_SERVICE, cookies=cookie)
        self.escribir_resultado_servicio(OBTENER_TODOS_LOS_DOCENTES_SERVICE, docentes_response)
        return docentes_response.json()["docentes"]
