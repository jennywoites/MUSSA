from flask_restful import Resource
from app.API_Rest.codes import *
from flask import request

from app.models.carreras_models import Carrera, Materia

import logging

class BuscarCarreras(Resource):
    def get(self):
        logging.info('Se invoco al servicio Buscar Carreras')
        args = request.args

        if args:
            logging.error('El servicio Buscar Carreras no recibe parámetros')
            return {'Error': 'Este servicio no recibe parametros'}, CLIENT_ERROR_BAD_REQUEST

        carreras = Carrera.query.all()

        carreras_result = []
        for carrera in carreras:
            carreras_result.append({
                'id': carrera.id,
                'codigo': carrera.codigo,
                'nombre': carrera.nombre,
                'plan': carrera.plan
            })

        result = ({'carreras': carreras_result}, SUCCESS_OK) 
        logging.info('Buscar Carreras devuelve como resultado: {}'.format(result))
        return result