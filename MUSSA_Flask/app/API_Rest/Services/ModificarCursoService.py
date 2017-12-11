from flask_restful import Resource
from app.API_Rest.codes import *
from flask import request

from app.models.horarios_models import Horario, Curso, CarreraPorCurso, HorarioPorCurso
from app.models.carreras_models import Carrera
from app.models.docentes_models import Docente, CursosDocente

import logging
from flask_user import roles_accepted
from app import db

from app.utils import DIAS

class ModificarCurso(Resource):

    @roles_accepted('admin')
    def get(self):
        args = request.args
        logging.info('Se invoco al servicio Modificar Curso con los siguientes parametros: {}'.format(args))

        q_id_curso = args["id_curso"] if "id_curso" in args else None

        q_carreras = args["carreras"] if "carreras" in args else None
        q_primer_cuatrimestre = self.convertir_booleano(args["primer_cuatrimestre"]) if "primer_cuatrimestre" in args else None
        q_segundo_cuatrimestre = self.convertir_booleano(args["segundo_cuatrimestre"]) if "segundo_cuatrimestre" in args else None
        q_docentes = args["docentes"] if "docentes" in args else None
        q_horarios = args["horarios"] if "horarios" in args else None

        if (not q_id_curso or not q_carreras or q_primer_cuatrimestre == None or
            q_segundo_cuatrimestre == None or not q_docentes or not q_horarios):
            logging.error('El servicio Modificar Curso recibió menos argumentos de los que debe')
            return {'Error': 'Falta enviar uno o mas de los argumentos obligatorios'}, CLIENT_ERROR_BAD_REQUEST            


        if not self.id_es_valido(q_id_curso):
            logging.error('El servicio Modificar Curso recibió un id de curso inválido')
            return {'Error': 'El id no es válido'}, CLIENT_ERROR_BAD_REQUEST            

        if not self.argumentos_son_validos(q_carreras, q_docentes, q_horarios):
            logging.error('El servicio Modificar Curso recibió uno o más argumentos inválidos')
            return {'Error': 'Uno o más argumentos no son válidos'}, CLIENT_ERROR_BAD_REQUEST        


        curso = Curso.query.filter_by(id=q_id_curso).first()

        self.eliminar_horarios_viejos(q_id_curso)
        self.eliminar_carreras_asociadas_viejas(q_id_curso)
        self.eliminar_docentes_actuales(q_id_curso)

        curso.se_dicta_primer_cuatrimestre = q_primer_cuatrimestre
        curso.se_dicta_segundo_cuatrimestre = q_segundo_cuatrimestre

        curso.docentes = q_docentes

        db.session.commit()

        self.agregar_horarios(q_id_curso, q_horarios)
        self.agregar_carreras(q_id_curso, q_carreras)
        self.agregar_docentes(q_id_curso, q_docentes)

        db.session.commit()


    def convertir_booleano(self, valor):
        valor = valor.lower()

        if valor == 'true':
            return True

        if valor == 'false':
            return False

        return None


    def eliminar_horarios_viejos(self, id_curso):
        horarios_por_curso = HorarioPorCurso.query.filter_by(curso_id=id_curso).all()

        ids_horarios = []
        for h in horarios_por_curso:
            ids_horarios.append(h.horario_id)

        HorarioPorCurso.query.filter_by(curso_id=id_curso).delete()
        db.session.commit()

        for id_horario in ids_horarios:
            Horario.query.filter_by(id=id_horario).delete()

        db.session.commit()


    def eliminar_carreras_asociadas_viejas(self, id_curso):
        CarreraPorCurso.query.filter_by(curso_id=id_curso).delete()
        db.session.commit()

    def eliminar_docentes_actuales(self, id_curso):
        CursosDocente.query.filter_by(curso_id=id_curso).delete()
        db.session.commit()

    def agregar_horarios(self, id_curso, horarios):
        horarios = horarios.split(";")
        for horario_a_agregar in horarios:
            dia, hora_desde, hora_hasta = self.parsear_horario(horario_a_agregar)
            horario = Horario(
                        dia = dia,
                        hora_desde = hora_desde,
                        hora_hasta = hora_hasta,
                    )
            db.session.add(horario)
            db.session.commit()

            db.session.add(HorarioPorCurso(curso_id=id_curso, horario_id=horario.id))

        db.session.commit()


    def parsear_horario(self, horario_a_agregar):
        horario_a_agregar = horario_a_agregar[1:-1]

        dia, hora_desde, hora_hasta = horario_a_agregar.split(",")
        dia = dia.split(":")[-1].upper()

        if not dia in DIAS:
            raise Exception("El nombre del dia no es válido")

        hora_desde = self.convertir_hora(hora_desde)
        hora_hasta = self.convertir_hora(hora_hasta)

        return dia, hora_desde, hora_hasta


    def agregar_docentes(self, id_curso, docentes):
        ids_docentes = docentes.split(";")
        for id_docente in ids_docentes:
            db.session.add(CursosDocente(
                curso_id=id_curso,
                docente_id=id_docente
            ))
        db.session.commit()


    def convertir_hora(self, hora):
        label, horas, minutos = hora.split(":")
        c_hora = int(horas)
        c_hora += 0.5 if int(minutos) == 30 else 0
        return c_hora


    def agregar_carreras(self, id_curso, carreras):
        carreras = carreras.split(";")
        for id_carrera in carreras:
            db.session.add(CarreraPorCurso(curso_id=id_curso, carrera_id=int(id_carrera)))
            db.session.commit()


    def esta_formado_solo_por_numeros(self, cadena):
        for letra in cadena:
            if not letra.isdigit():
                return False
        return True


    def id_es_valido(self, id_curso):
        es_un_id = id_curso and self.esta_formado_solo_por_numeros(id_curso)

        if not es_un_id:
            return False

        return (len(Curso.query.filter_by(id=id_curso).all()) == 1)


    def argumentos_son_validos(self, carreras, docentes, horarios):
        return (self.carreras_son_validas(carreras) and
                self.docentes_son_validos(docentes) and
                self.horarios_son_validos(horarios))


    def carreras_son_validas(self, carreras):
        carreras = carreras.split(";")
        for carrera in carreras:
            if (not self.esta_formado_solo_por_numeros(carrera) or
                    not len((Carrera.query.filter_by(id=carrera).all())) > 0):
                return False
        return True


    def docentes_son_validos(self, docentes):
        ids_docentes = docentes.split(";")
        for id_docente in ids_docentes:
            if (not id_docente.isdigit() or
                    not Docente.query.filter_by(id=id_docente).first()):
                return False

        return True


    def horarios_son_validos(self, horarios):
        horarios = horarios.split(";")
        for horario in horarios:
            try:
                self.parsear_horario(horario)
            except Exception as e:
                return False

        return True