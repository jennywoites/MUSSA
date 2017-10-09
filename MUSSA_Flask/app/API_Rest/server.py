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
                'nombre': carrera.nombre
            })

        result = ({'carreras': carreras_result}, SUCCESS_OK) 
        logging.info('Buscar Carreras devuelve como resultado: {}'.format(result))
        return result


class BuscarMaterias(Resource):
    def get(self):
        args = request.args
        logging.info('Se invoco al servicio Buscar Materias con los siguientes parametros: {}'.format(args))

        q_codigo = args["codigo"] if "codigo" in args else None
        q_nombre = args["nombre"] if "nombre" in args else None
        q_carreras = ["10"]

        #Agregar validaciones de los parametros enviados

        query = Materia.query
        if q_codigo: query = query.filter(Materia.codigo.like(q_codigo + "%"))
        if q_nombre: query = query.filter(Materia.nombre.like("%" + q_nombre + "%"))

        #Falta las carreras

        materias = query.order_by(Materia.codigo.asc()).all()

        materias_result = []
        for materia in materias:
            materias_result.append({
                'id': materia.id,
                'codigo': materia.codigo,
                'nombre': materia.nombre,
                'carrera': materia.carrera.nombre
            })

        result = ({'materias': materias_result}, SUCCESS_OK)
        logging.info('Buscar Materias devuelve como resultado: {}'.format(result))

        return result