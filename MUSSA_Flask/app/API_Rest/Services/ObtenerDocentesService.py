from flask_restful import Resource
from app.API_Rest.codes import *
from flask import request

from app.models.docentes_models import Docente, CursosDocente
from app.models.carreras_models import Materia, Carrera
from app.models.horarios_models import Curso

import logging


class ObtenerDocentes(Resource):
    def get(self):
        args = request.args
        logging.info('Se invoco al servicio Obtener Docentes con los siguientes parametros: {}'.format(args))

        id_docente = args["idDocente"] if "idDocente" in args else None

        if id_docente and not self.id_docente_es_valido(id_docente):
            logging.error('El servicio Obtener Docentes recibio un id de docente invalido')
            return {'Error': 'Este servicio recibio un id docente'
                             ' invalido'}, CLIENT_ERROR_BAD_REQUEST

        docentes_result = []

        query = Docente.query

        if id_docente:
            query = query.filter_by(id=id_docente)

        docentes = query.order_by(Docente.apellido.asc()).order_by(Docente.nombre.asc()).all()

        for docente in docentes:
            materias = {}

            cursos_del_docente = CursosDocente.query.filter_by(docente_id=docente.id).all()
            for c in cursos_del_docente:
                curso = Curso.query.filter_by(id=c.curso_id).first()
                materia = Materia.query.filter_by(codigo=curso.codigo_materia).first()
                carrera = Carrera.query.filter_by(id=materia.carrera_id).first()
                materias[materia.codigo] = {"nombre": materia.nombre,
                                            "id_carrera": materia.carrera_id,
                                            "carrera": carrera.get_descripcion_carrera()}

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

    def id_docente_es_valido(self, id_docente):
        return id_docente.isdigit() and Docente.query.filter_by(id=id_docente).first()