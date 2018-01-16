from app.API_Rest.Services.BaseService import BaseService
from app.API_Rest.codes import *
from app.models.generadorJSON.palabras_clave_generadorJSON import generarJSON_tematica_materia
from app.models.filtros.palabras_clave_filter import filtrar_tematica_materia


class AllTematicasService(BaseService):
    def getNombreClaseServicio(self):
        return "All Tematicas Service"

    def get(self):
        self.logg_parametros_recibidos()

        solo_verificadas = self.obtener_booleano("solo_verificadas")

        parametros_son_validos, msj, codigo = self.validar_parametros({
            "solo_verificadas": {
                self.PARAMETRO: solo_verificadas,
                self.ES_OBLIGATORIO: False,
                self.FUNCIONES_VALIDACION: [
                    (self.booleano_es_valido, [])
                ]
            }
        })

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': msj}, codigo

        filtros = {}
        filtros["solo_verificadas"] = solo_verificadas

        tematicas = filtrar_tematica_materia(filtros)

        tematicas_result = self.generar_JSON_lista_datos(generarJSON_tematica_materia, tematicas)

        result = ({"tematicas": tematicas_result}, SUCCESS_OK)
        self.logg_resultado(result)

        return result


#########################################
CLASE = AllTematicasService
URLS_SERVICIOS = (
    '/api/tematica/all',
)
#########################################
