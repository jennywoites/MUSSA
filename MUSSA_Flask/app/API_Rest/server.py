from flask_restful import Resource
from app.API_Rest.codes import *

from app.models.carreras_models import Carrera

class BuscarCarreras(Resource):
    def get(self):
        carreras = Carrera.query.all()

        carreras_result = []
        for carrera in carreras:
            carreras_result.append({
                'id': carrera.id,
                'codigo': carrera.codigo,
                'nombre': carrera.nombre
            })

        return {'carreras': carreras_result}, SUCCESS_OK

