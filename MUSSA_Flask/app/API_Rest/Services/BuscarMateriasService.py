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

        if not self.son_parametros_validos(q_codigo, q_nombre, q_carreras):
            logging.error('El servicio Buscar Materias recibió parámetros inválidos')
            return {'Error': 'Uno o más parámteros enviados son inválidos'}, CLIENT_ERROR_BAD_REQUEST

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

    def son_parametros_validos(self, codigo, nombre, carreras):
        if codigo and not self.es_codigo_valido(codigo):
            return False

        if nombre and not self.es_nombre_de_materia_valido(nombre):
            return False

        if carreras and not self.son_carreras_validas(carreras):
            return False

        return True

    def es_codigo_valido(self, codigo):
        LONGITUD_CODIGO_MAXIMA = 4
        return codigo.isdigit() and len(codigo) <= LONGITUD_CODIGO_MAXIMA

    def es_nombre_de_materia_valido(self, nombre):
        for palabra in nombre.split(" "):
            if not palabra.isalpha():
                return False
        return True

    def son_carreras_validas(self, carreras):
        for carrera in carreras:
            if (not carrera.isdigit() or
                    not Carrera.query.filter_by(codigo=carrera).first()):
                return False

        return True
