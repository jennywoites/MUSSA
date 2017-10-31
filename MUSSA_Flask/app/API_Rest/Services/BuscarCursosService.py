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
        q_carrera = args["id_carrera"] if "id_carrera" in args else None

        #Agregar validaciones de los parametros enviados

        query = Curso.query
        if q_nombre_curso: query = query.filter(Curso.codigo.like("%" + q_nombre_curso + "%"))
        if q_codigo_materia: query = query.filter(Curso.codigo_materia.like(q_codigo_materia + "%"))

        #Filtrar aquellos cursos que no se estan dando ni el primer ni el segundo cuatrimestre (ambos en false)

        cursos = query.all()

        cursos_result = []
        for curso in cursos:

            carreras_response = []
            query = CarreraPorCurso.query.filter_by(curso_id=curso.id)
            if q_carrera: query = query.filter_by(carrera_id=q_carrera)
            carrerasPorCurso = query.all()
            for carrera in carrerasPorCurso:
                carrera_db = Carrera.query.filter_by(id=carrera.carrera_id).first()
                carreras_response.append({
                    'codigo': carrera_db.codigo,
                    'nombre': carrera_db.nombre
                })
            if not carreras_response: #No es un curso valido para la query elegida
                continue

            horarios_response = []
            for horario in HorarioPorCurso.query.filter_by(curso_id=curso.id).all():
                horario_db = Horario.query.filter_by(id=horario.horario_id).first()
                horarios_response.append({
                    'dia': horario_db.dia,
                    'hora_desde': self.convertir_hora(horario_db.hora_desde),
                    'hora_hasta': self.convertir_hora(horario_db.hora_hasta) 
                })

            cursos_result.append({
                'id': curso.id,
                'codigo_curso': curso.codigo,
                'codigo_materia': curso.codigo_materia,
                'se_dicta_primer_cuatri': curso.se_dicta_primer_cuatrimestre,
                'se_dicta_segundo_cuatri': curso.se_dicta_segundo_cuatrimestre,
                'cuatrimestre': self.mensaje_cuatrimestre(curso),
                'carreras': carreras_response,
                'horarios': horarios_response,
                'docentes': curso.docentes,
                'puntaje': self.calcular_puntaje(curso)
            })

        cursos_result.sort(key=lambda curso : curso["puntaje"], reverse=True)

        result = ({'cursos': cursos_result}, SUCCESS_OK)
        logging.info('Buscar Cursos devuelve como resultado: {}'.format(result))

        return result

    def calcular_puntaje(self, curso):
        if curso.cantidad_encuestas_completas == 0:
            return 0
        return (curso.puntaje_total_encuestas / curso.cantidad_encuestas_completas)

    def convertir_hora(self, horario):
        l_horario = str(horario).split(".")
        if len(l_horario) == 1:
            return l_horario[0] + ":00"
        return l_horario[0] + ":30"

    def mensaje_cuatrimestre(slef, curso):
        if not curso.se_dicta_primer_cuatrimestre and not curso.se_dicta_segundo_cuatrimestre:
            return "No se dicta actualmente"
        if curso.se_dicta_primer_cuatrimestre and curso.se_dicta_segundo_cuatrimestre:
            return "Ambos cuatrimestres"
        if curso.se_dicta_primer_cuatrimestre:
            return "Solo el 1º cuatrimestre"
        return "Solo el 2º cuatrimestre"

