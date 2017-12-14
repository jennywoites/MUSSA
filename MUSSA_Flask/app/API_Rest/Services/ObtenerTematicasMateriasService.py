from flask_restful import Resource
from app.API_Rest.codes import *
from flask import request
from app.models.palabras_clave_models import TematicaMateria
import logging


class ObtenerTematicasMaterias(Resource):
    def get(self):
        args = request.args
        logging.info('Se invoco al servicio Obtener Temáticas Materias con los siguientes parametros: {}'.format(args))

        if args:
            logging.error('El servicio Obtener Temáticas Materias no recibe parametros')
            return {'Error': 'Este servicio no recibe parametros'}, CLIENT_ERROR_BAD_REQUEST

        tematicas_result = []
        for tematica in TematicaMateria.query.order_by(TematicaMateria.tematica.asc()).all():
            tematicas_result.append({
                "id": tematica.id,
                "tema": tematica.tematica
            })

        result = ({'tematicas': tematicas_result}, SUCCESS_OK)
        logging.info('Obtener Temáticas Materiasdevuelve como resultado: {}'.format(result))

        return result
