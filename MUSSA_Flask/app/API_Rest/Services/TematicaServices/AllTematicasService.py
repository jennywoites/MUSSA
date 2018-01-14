from app.API_Rest.Services.BaseService import BaseService
from app.API_Rest.codes import *
from app.models.generadorJSON.palabras_clave_generadorJSON import generarJSON_tematica_materia
from app.models.filtros.palabras_clave_filter import filtrar_tematica_materia


class AllTematicasService(BaseService):
    def getNombreClaseServicio(self):
        return "All Tematicas Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    def get(self):
        self.logg_parametros_recibidos()

        solo_verificadas = self.obtener_booleano("solo_verificadas")

        if not self.booleano_es_valido(solo_verificadas, obligatorio=False):
            msj = "El parámetro 'solo_verificadas' no tiene un valor válido."
            self.logg_error(msj)
            return {'Error': msj}, CLIENT_ERROR_BAD_REQUEST

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
