from flask_restful import Resource
from app.API_Rest.codes import *
from flask import request

from app.models.docentes_models import Docente, CursosDocente
from app.models.carreras_models import Materia
from app.models.horarios_models import Curso

import logging


class ObtenerDocentesCurso(Resource):
    def get(self):
        args = request.args
        logging.info('Se invoco al servicio Obtener Docentes del Curso con los siguientes parametros: {}'.format(args))

        id_curso = args["id_curso"] if "id_curso" in args else None

        if not id_curso or not self.es_valido(id_curso):
            logging.error('El servicio Obtener Docentes del curso debe recibir el id del curso')
            return {'Error': 'Este servicio debe recibir el id del curso'}, CLIENT_ERROR_BAD_REQUEST

        docentes_result = []

        docentes_del_curso = CursosDocente.query.filter_by(curso_id=id_curso).all()
        for doc in docentes_del_curso:
            materias = {}
            docente = Docente.query.filter_by(id=doc.docente_id).first()

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
        logging.info('Obtener Docentes del Curso devuelve como resultado: {}'.format(result))

        return result

    def es_valido(self, id_curso):
        return id_curso.isdigit() and len(Curso.query.filter_by(id=id_curso).all()) > 0