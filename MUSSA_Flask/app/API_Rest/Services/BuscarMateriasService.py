from flask_restful import Resource
from app.API_Rest.codes import *
from flask import request

from app.models.carreras_models import Carrera, Materia

import logging

class BuscarMaterias(Resource):
    def get(self):
        args = request.args
        logging.info('Se invoco al servicio Buscar Materias con los siguientes parametros: {}'.format(args))

        q_codigo = args["codigo"] if "codigo" in args else None
        q_nombre = args["nombre"] if "nombre" in args else None
        q_carreras = args["carreras"].split(",") if "carreras" in args else None

        #Agregar validaciones de los parametros enviados

        query = Materia.query
        if q_codigo: query = query.filter(Materia.codigo.like(q_codigo + "%"))
        if q_nombre: query = query.filter(Materia.nombre.like("%" + q_nombre + "%"))
        if q_carreras: query = query.filter(Materia.carrera.has(Carrera.codigo.in_(q_carreras)))

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