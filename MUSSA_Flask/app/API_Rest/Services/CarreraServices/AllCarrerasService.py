from app.API_Rest.codes import *
from app.models.generadorJSON.carreras_generadorJSON import generarJSON_carrera
from app.API_Rest.Services.BaseService import BaseService
from app.models.filtros.carreras_filter import filtrar_carrera
from app.models.carreras_models import Materia


class AllCarrerasService(BaseService):
    def getNombreClaseServicio(self):
        return "All Carreras Service"

    def get(self):
        self.logg_parametros_recibidos()

        codigo_materia = self.obtener_parametro("codigo_materia")

        parametros_son_validos, msj, codigo = self.validar_parametros({
            "codigo_materia": {
                self.PARAMETRO: codigo_materia,
                self.ES_OBLIGATORIO: False,
                self.FUNCIONES_VALIDACION: [
                    (self.es_numero_valido, []),
                    (self.existe_el_elemento, [Materia, Materia.codigo])
                ]
            }
        })

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': msj}, codigo

        filtros = {}
        if codigo_materia:
            filtros["codigo_materia"] = codigo_materia

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
