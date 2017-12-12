from flask_restful import Resource
from app.API_Rest.codes import *
from flask import request

from flask_user import current_user, login_required
from app.models.alumno_models import Alumno
from app.models.respuestas_encuesta_models import EncuestaAlumno

import logging


class ObtenerEncuestasAlumno(Resource):
    @login_required
    def get(self):
        args = request.args
        logging.info('Se invoco al servicio Obtener Encuesta Alumno con los siguientes parametros: {}'.format(args))

        if args and not self.parametros_es_valido(args):
            logging.error('El servicio Obtener Encuestas Alumno solo recibe si las encuestas deben estar finalizadas o no')
            return {'Error': 'Este servicio solo recibe si las encuestas deben estar finalizadas o no'}, CLIENT_ERROR_BAD_REQUEST

        alumno = Alumno.query.filter_by(user_id=current_user.id).first()

        encuestas = []
        if alumno:
            query = EncuestaAlumno.query.filter_by(alumno_id=alumno.id)
            if "finalizadas" in args:
                query = query.filter_by(finalizada=self.obtener_parametro_finalizadas(args))
            encuestas = query.all()


        encuestas_result = []
        for encuesta in encuestas:
            encuestas_result.append({
                "id": encuesta.id,
                "alumno_id": encuesta.alumno_id,
                "materia_alumno_id": encuesta.materia_alumno_id,
                "carrera": encuesta.carrera,
                "materia": encuesta.materia,
                "curso": encuesta.curso,
                "cuatrimestre_aprobacion_cursada": encuesta.cuatrimestre_aprobacion_cursada,
                "anio_aprobacion_cursada": encuesta.anio_aprobacion_cursada,
                "fecha_aprobacion": "{}C / {}".format(encuesta.cuatrimestre_aprobacion_cursada,
                                                      encuesta.anio_aprobacion_cursada),
                "finalizada": encuesta.finalizada
            })

        result = ({'encuestas': encuestas_result}, SUCCESS_OK)
        logging.info('Obtener Encuestas Alumno devuelve como resultado: {}'.format(result))

        return result

    def obtener_parametro_finalizadas(self, args):
        finalizadas = args["finalizadas"].upper()
        return finalizadas == "TRUE"

    def parametros_es_valido(self, args):
        if not "finalizadas" in args:
            return False

        finalizadas = args["finalizadas"].upper()
        return (finalizadas == "TRUE" or finalizadas == "FALSE")