from flask_restful import Resource
from app.API_Rest.codes import *
from flask import request

from app.models.carreras_models import Materia, Correlativas

import logging

class ObtenerMateriasCorrelativas(Resource):
    def get(self):
        args = request.args
        logging.info('Se invoco al servicio Obtener Materia con los siguientes parametros: {}'.format(args))

        q_id = args["id_materia"] if "id_materia" in args else None

        if not q_id or not self.id_materia_es_valido(q_id):
            logging.error('El servicio Obtener Materias Correlativas recibe el id de la materia')
            return {'Error': 'Este servicio debe recibir el id de la materia'}, CLIENT_ERROR_BAD_REQUEST

        query = Correlativas.query.filter_by(materia_id=q_id)
        correlativas = query.all()

        materias_result = []
        for correlativa in correlativas:
            materia = Materia.query.filter_by(id=correlativa.materia_correlativa_id).first()
            materias_result.append({
                'id': materia.id,
                'codigo': materia.codigo,
                'nombre': materia.nombre,
            })

        materias_result.sort(key=lambda materia : materia["codigo"] if len(materia["codigo"]) > 1 else "0" + materia["codigo"])

        result = ({'correlativas': materias_result}, SUCCESS_OK)
        logging.info('Obtener Materias Correlativas devuelve como resultado: {}'.format(result))

        return result

    def id_materia_es_valido(self, q_id):
        return q_id.isdigit() and len(Materia.query.filter_by(id=q_id).all()) > 0