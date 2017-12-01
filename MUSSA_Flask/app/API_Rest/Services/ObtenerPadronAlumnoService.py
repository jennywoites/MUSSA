from flask_restful import Resource
from app.API_Rest.codes import *
from flask import request

from flask_user import current_user, login_required
from app.models.alumno_models import Alumno

import logging


class ObtenerPadronAlumno(Resource):
    @login_required
    def get(self):
        args = request.args
        logging.info('Se invoco al servicio Obtener Padron Alumno con los siguientes parametros: {}'.format(args))

        if args:
            logging.error('El servicio Obtener Padron Alumno no recibe parametros')
            return {'Error': 'Este servicio no recibe parametros'}, CLIENT_ERROR_BAD_REQUEST

        alumno = Alumno.query.filter_by(user_id=current_user.id).first()

        padron_result = alumno.padron if alumno else ""

        result = ({'padron': padron_result}, SUCCESS_OK)
        logging.info('Obtener Padron Alumno devuelve como resultado: {}'.format(result))

        return result
