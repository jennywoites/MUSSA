from flask_restful import Resource
from app.API_Rest.codes import *
from flask import request

from app.models.carreras_models import Materia

import logging

class ObtenerMateria(Resource):
    def get(self):
        args = request.args
        logging.info('Se invoco al servicio Obtener Materia con los siguientes parametros: {}'.format(args))

        q_id = args["id_materia"] if "id_materia" in args else None

        if not q_id or not q_id.isdigit():
            logging.error('El servicio Obtener Materia recibe el id de la materia')
            return {'Error': 'Este servicio debe recibir el id de la materia'}, CLIENT_ERROR_BAD_REQUEST

        query = Materia.query.filter_by(id=q_id)
        materia = query.first()

        materia_result = {
            'id': materia.id,
            'codigo': materia.codigo,
            'nombre': materia.nombre,
            'creditos': materia.creditos,
            'creditos_minimos_para_cursarla': materia.creditos_minimos_para_cursarla,
            #'tipo': materia.tipo_materia_id.descripcion,
            'carrera_id': materia.carrera.id,
            'carrera': materia.carrera.nombre
        }

        result = ({'materia': materia_result}, SUCCESS_OK)
        logging.info('Obtener Materia devuelve como resultado: {}'.format(result))

        return result