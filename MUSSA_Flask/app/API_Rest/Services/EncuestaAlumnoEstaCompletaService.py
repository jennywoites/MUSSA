from flask_restful import Resource
from app.API_Rest.codes import *
from flask import request

from flask_user import current_user, login_required
from app.models.alumno_models import Alumno
from app.models.respuestas_encuesta_models import EncuestaAlumno, EstadoPasosEncuestaAlumno

import logging


class EncuestaAlumnoEstaCompletaService(Resource):
    @login_required
    def get(self):
        args = request.args
        logging.info(
            'Se invoco al servicio Encuesta alumno está completa con los siguientes parametros: {}'.format(args))

        id_encuesta = args["id_encuesta"] if "id_encuesta" in args else None

        alumno = Alumno.query.filter_by(user_id=current_user.id).first()

        if not self.id_encuesta_es_valido(id_encuesta, alumno):
            logging.error('El servicio recibió un id de encuesta invalido')
            return {'Error': 'El servicio recibió un id de encuesta invalido'}, CLIENT_ERROR_BAD_REQUEST

        pasos = EstadoPasosEncuestaAlumno.query.filter_by(encuesta_alumno_id=id_encuesta).first()

        result = ({'esta_completa': pasos.estan_todos_los_pasos_completos()}, SUCCESS_OK)
        logging.info('Encuesta alumno está completa devuelve como resultado: {}'.format(result))

        return result

    def id_encuesta_es_valido(self, id_encuesta, alumno):
        if not id_encuesta or not id_encuesta.isdigit():
            return False

        return EncuestaAlumno.query.filter_by(id=id_encuesta).filter_by(alumno_id=alumno.id).first()
