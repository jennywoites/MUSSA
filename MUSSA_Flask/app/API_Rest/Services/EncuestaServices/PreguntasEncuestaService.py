from app.API_Rest.Services.BaseService import BaseService
from app.models.encuestas_models import GrupoEncuesta
from app.models.filtros.encuestas_filter import filtrar_encuestas
from app.models.generadorJSON.encuestas_generadorJSON import generarJSON_encuesta
from app.API_Rest.codes import *


class PreguntasEncuestaService(BaseService):
    def getNombreClaseServicio(self):
        return "Preguntas Encuesta Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    def get(self):
        self.logg_parametros_recibidos()

        categorias = self.obtener_lista("categorias")

        parametros_son_validos, msj, codigo = self.validar_parametros(dict([
            ("categorias", {
                self.PARAMETRO: categorias,
                self.ES_OBLIGATORIO: False,
                self.FUNCIONES_VALIDACION: [
                    (self.es_numero_valido, []),
                    (self.existe_el_elemento, [GrupoEncuesta, GrupoEncuesta.numero_grupo])
                ]
            })
        ]))

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': msj}, codigo

        filtros = {}
        if categorias:
            filtros["categorias"] = categorias

        preguntas_result = []
        for encuesta in filtrar_encuestas(filtros):
            preguntas_result.append(generarJSON_encuesta(encuesta))

        result = ({'preguntas': preguntas_result}, SUCCESS_OK)
        self.logg_resultado(result)

        return result


#########################################
CLASE = PreguntasEncuestaService
URLS_SERVICIOS = (
    '/api/encuesta/preguntas',
)
#########################################
