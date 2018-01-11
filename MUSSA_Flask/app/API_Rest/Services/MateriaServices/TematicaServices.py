from flask_restful import Resource
from app.API_Rest.codes import *
from flask_user import roles_accepted
from app.models.palabras_clave_models import TematicaMateria
import logging


class TematicaService(Resource):
    def getNombreClaseServicio(self):
        return "Tematica Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    @roles_accepted('admin')
    def get(self, idTematica):
        if not idTematica > 0:
            logging.error(self.getNombreClaseServicio() + ': El id de la temática debe ser un entero mayor a 0')
            return {'Error': 'El id de la temática debe ser un entero mayor a 0'}, CLIENT_ERROR_NOT_FOUND

        if not self.existe_id(idTematica):
            logging.error(self.getNombreClaseServicio() + ': El id de la temática no existe')
            return {'Error': 'El id de la temática no existe'}, CLIENT_ERROR_NOT_FOUND

        tematica = TematicaMateria.query.get(idTematica)
        tematica_result = self.generarJSONTematica(tematica)

        result = (tematica_result, SUCCESS_OK)
        logging.info(self.getNombreClaseServicio() + ': Resultado: {}'.format(result))

        return result

    ##########################################
    ##          Funciones Auxiliares        ##
    ##########################################

    def existe_id(self, id_tematica):
        return TematicaMateria.query.get(id_tematica)

    def generarJSONTematica(self, tematica):
        return {
            "id_tematica": tematica.id,
            "tematica": tematica.tematica,
            "verificada": tematica.verificada
        }


#########################################
CLASE = TematicaService
URLS_SERVICIOS = (
    '/api/materia/tematica/<int:idTematica>',
)
#########################################
