from app.API_Rest.codes import *
from flask_user import roles_accepted
from app.models.palabras_clave_models import TematicaMateria
from app.models.generadorJSON.palabras_clave_generadorJSON import generarJSON_tematica_materia
from app.API_Rest.Services.BaseService import BaseService


class TematicaService(BaseService):
    def getNombreClaseServicio(self):
        return "Tematica Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    @roles_accepted('admin')
    def get(self, idTematica):
        self.logg_parametros_recibidos()

        if not idTematica > 0:
            msj = "El id de la temática debe ser un entero mayor a 0"
            self.logg_error(msj)
            return {'Error': 'msj'}, CLIENT_ERROR_NOT_FOUND

        if not self.existe_id(TematicaMateria, idTematica):
            msj = "El id de la temática no existe"
            self.logg_error(msj)
            return {'Error': 'msj'}, CLIENT_ERROR_NOT_FOUND

        tematica = TematicaMateria.query.get(idTematica)
        tematica_result = generarJSON_tematica_materia(tematica)

        result = (tematica_result, SUCCESS_OK)
        self.logg_resultado(result)
        return result


#########################################
CLASE = TematicaService
URLS_SERVICIOS = (
    '/api/tematica/<int:idTematica>',
)
#########################################
