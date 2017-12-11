from flask_restful import Resource
from app.API_Rest.codes import *
from flask import request

from app.models.docentes_models import Docente, CursosDocente
from app.models.carreras_models import Materia
from app.models.horarios_models import Curso

import logging


class ObtenerDocentes(Resource):
    def get(self):
        args = request.args
        logging.info('Se invoco al servicio Obtener Docentes con los siguientes parametros: {}'.format(args))

        if args:
            logging.error('El servicio Obtener Docentes no recibe parámetros')
            return {'Error': 'Este servicio no recibe parámetros'}, CLIENT_ERROR_BAD_REQUEST

        docentes_result = []

        docentes = Docente.query.order_by(Docente.apellido.asc()).order_by(Docente.nombre.asc()).all()
        for docente in docentes:
            materias = {}

            cursos_del_docente = CursosDocente.query.filter_by(docente_id=docente.id).all()
            for c in cursos_del_docente:
                curso = Curso.query.filter_by(id=c.curso_id).first()
                materia = Materia.query.filter_by(codigo=curso.codigo_materia).first()
                if not materia.codigo in materias:
                    materias[materia.codigo] = materia.nombre

            docentes_result.append({
                "id_docente": docente.id,
                "apellido": docente.apellido,
                "nombre": docente.nombre,
                "nombre_completo": docente.obtener_nombre_completo(),
                "materias_que_dicta": materias
            })

        result = ({'docentes': docentes_result}, SUCCESS_OK)
        logging.info('Obtener Docentes devuelve como resultado: {}'.format(result))

        return result