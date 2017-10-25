from flask_restful import Resource
from app.API_Rest.codes import *
from flask import request

from app.models.horarios_models import Horario, Curso, CarreraPorCurso, HorarioPorCurso
from app.models.carreras_models import Carrera, Materia

import logging

class BuscarCursos(Resource):
    def get(self):
        args = request.args
        logging.info('Se invoco al servicio Buscar Cursos con los siguientes parametros: {}'.format(args))

        q_nombre_curso = args["nombre_curso"] if "nombre_curso" in args else None
        q_codigo_materia = args["codigo_materia"] if "codigo_materia" in args else None

        #Agregar validaciones de los parametros enviados

        query = Curso.query
        if q_nombre_curso: query = query.filter(Curso.codigo.like("%" + q_nombre_curso + "%"))
        if q_codigo_materia: query = query.filter(Curso.codigo_materia.like(q_codigo_materia + "%"))
        cursos = query.all()

        cursos_result = []
        for curso in cursos:

            carreras_response = []
            for carrera in CarreraPorCurso.query.filter_by(curso_id=curso.id).all():
                carrera_db = Carrera.query.filter_by(id=carrera.carrera_id).first()
                carreras_response.append({
                    'codigo': carrera_db.codigo,
                    'nombre': carrera_db.nombre
                })

            horarios_response = []
            for horario in HorarioPorCurso.query.filter_by(curso_id=curso.id).all():
                horario_db = Horario.query.filter_by(id=horario.horario_id).first()
                horarios_response.append({
                    'dia': horario_db.dia,
                    'hora_desde': horario_db.hora_desde,
                    'hora_hasta': horario_db.hora_hasta 
                })

            cursos_result.append({
                'id': curso.id,
                'codigo_curso': curso.codigo,
                'codigo_materia': curso.codigo_materia,
                'se_dicta_primer_cuatri': curso.se_dicta_primer_cuatrimestre,
                'se_dicta_segundo_cuatri': curso.se_dicta_segundo_cuatrimestre,
                'carreras': carreras_response,
                'horarios': horarios_response,
            })

        result = ({'cursos': cursos_result}, SUCCESS_OK)
        logging.info('Buscar Cursos devuelve como resultado: {}'.format(result))

        return result