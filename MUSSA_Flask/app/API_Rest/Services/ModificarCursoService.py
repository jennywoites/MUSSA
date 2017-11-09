from flask_restful import Resource
from app.API_Rest.codes import *
from flask import request

from app.models.horarios_models import Horario, Curso, CarreraPorCurso, HorarioPorCurso
from app.models.carreras_models import Carrera, Materia

import logging
from flask_user import roles_accepted
from app import db


class ModificarCurso(Resource):

    @roles_accepted('admin')
    def get(self):
        args = request.args
        logging.info('Se invoco al servicio Modificar Curso con los siguientes parametros: {}'.format(args))

        q_id_curso = args["id_curso"] if "id_curso" in args else None

        q_carreras = args["carreras"] if "carreras" in args else None
        q_primer_cuatrimestre = args["primer_cuatrimestre"] if "primer_cuatrimestre" in args else None
        q_segundo_cuatrimestre = args["segundo_cuatrimestre"] if "segundo_cuatrimestre" in args else None
        q_docentes = args["docentes"] if "docentes" in args else None
        q_horarios = args["horarios"] if "horarios" in args else None

        print(args)
        return {'Error': ''}, 400

        #Validar argumentos (que existan y que sean lo que corresponde)

        #if not self.parametros_son_validos(q_id_curso, q_nombre_curso, q_codigo_materia, q_carrera):
        #    logging.error('El servicio Buscar Cursos recibió parámetros inválidos')
        #    return {'Error': 'Este servicio recibió parámetros inválidos'}, CLIENT_ERROR_BAD_REQUEST

        curso = Curso.query.filter_by(id=q_id_curso)

        self.eliminar_horarios_viejos(q_id_curso)
        self.eliminar_carreras_asociadas_viejas(q_id_curso)

        curso.se_dicta_primer_cuatrimestre = q_primer_cuatrimestre
        curso.se_dicta_segundo_cuatrimestre = q_segundo_cuatrimestre
        curso.docentes = q_docentes

        self.agregar_horarios(q_id_curso, q_horarios)
        self.agregar_carreras(q_id_curso, q_carreras)

        db.session.commit()


    def eliminar_horarios_viejos(self, id_curso):
        horarios_por_curso = HorarioPorCurso.query.filter_by(curso_id=id_curso).all()

        ids_horarios = []
        for h in horarios_por_curso:
            ids_horarios.append(h.horario_id)

        HorarioPorCurso.query.filter_by(curso_id=id_curso).delete()
        db.session.commit()

        for id_horario in ids_horarios:
            Horario.query.filter(id=id_horario).delete()

        db.session.commit()


    def eliminar_carreras_asociadas_viejas(self, id_curso):
        CarreraPorCurso.query.filter_by(curso_id=id_curso).delete()
        db.session.commit()


    def agregar_horarios(self, id_curso, horarios):
        for horario_a_agregar in horarios:
            horario = Horario(
                        dia = horario_a_agregar["dia"],
                        hora_desde = horario_a_agregar["hora_desde"],
                        hora_hasta = horario_a_agregar["hora_hasta"],
                    )
            db.session.add(horario)

            db.session.add(HorarioPorCurso(curso_id=id_curso, horario_id=horario.id))

        db.session.commit()


    def agregar_carreras(self, id_curso, carreras):
        for id_carrera in carreras:
            db.session.add(CarreraPorCurso(curso_id=id_curso, carrera_id=id_carrera))

        db.session.commit()
