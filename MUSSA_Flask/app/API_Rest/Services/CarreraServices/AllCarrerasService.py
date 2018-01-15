from app.API_Rest.codes import *
from app.models.generadorJSON.carreras_generadorJSON import generarJSON_carrera
from app.API_Rest.Services.BaseService import BaseService
from app.models.filtros.carreras_filter import filtrar_carrera


class AllCarrerasService(BaseService):
    def getNombreClaseServicio(self):
        return "All Carreras Service"

    def get(self):
        self.logg_parametros_recibidos()

        filtros = {}

        carreras_result = []
        for carrera in filtrar_carrera(filtros):
            carreras_result.append(generarJSON_carrera(carrera))

        result = ({'carreras': carreras_result}, SUCCESS_OK)
        self.logg_resultado(result)

        return result


#########################################
CLASE = AllCarrerasService
URLS_SERVICIOS = (
    '/api/carrera/all',
)
#########################################
