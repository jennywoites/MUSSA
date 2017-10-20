from flask_restful import Resource
from app.API_Rest.codes import *
from flask import request

from app.models.carreras_models import Carrera, Materia

import logging

class ObtenerCarrerasDondeSeDictaLaMateria(Resource):
    def get(self):
        args = request.args
        logging.info('Se invoco al servicio Obtener Carreras donde se dicta la materia con los siguientes parametros: {}'.format(args))

        q_codigo = args["codigo_materia"] if "codigo_materia" in args else None

        if not q_codigo or not q_codigo.isdigit():
            logging.error('El servicio Obtener Carreras donde se dicta la materia recibe el codigo de la materia')
            return {'Error': 'Este servicio debe recibir el codigo de la materia'}, CLIENT_ERROR_BAD_REQUEST

        materias = Materia.query.filter_by(codigo=q_codigo).all()

        carreras_result = []
        for materia in materias:
            carrera = Carrera.query.filter_by(id=materia.carrera.id).first()
        
            carreras_result.append({
                'id': carrera.id,
                'codigo': carrera.codigo,
                'nombre': carrera.nombre,
                'id_materia': materia.id
            })

        result = ({'carreras': carreras_result}, SUCCESS_OK) 
        logging.info('Obtener Carreras donde se dicta la materia devuelve como resultado: {}'.format(result))

        return result