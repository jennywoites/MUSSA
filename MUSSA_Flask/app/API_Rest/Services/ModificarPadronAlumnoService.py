from flask_restful import Resource
from app.API_Rest.codes import *
from flask import request

from flask_user import current_user, login_required
from app.models.alumno_models import Alumno

from app import db

import logging

LONGITUD_MINIMA_PADRON = 5
LONGITUD_MAXIMA_PADRON = 7

class ModificarPadronAlumno(Resource):
    
    @login_required
    def get(self):
        args = request.args
        logging.info('Se invoco al servicio Modificar Padron Alumno con los siguientes parametros: {}'.format(args))

        q_padron = args["padron"] if "padron" in args else None

        if not q_padron:
            logging.error('El servicio Modificar Padron Alumno debe recibir el nuevo padron')
            return {'Error': 'Este servicio debe recibir un padron'}, CLIENT_ERROR_BAD_REQUEST

        alumno = Alumno.query.filter_by(user_id=current_user.id).first()

        if not self.es_valido(q_padron, alumno.id):
            logging.error('El nuevo padrón no es válido')
            return {'Error': 'El nuevo padrón no es válido'}, CLIENT_ERROR_BAD_REQUEST

        if not alumno:
            alumno = Alumno(user_id=current_user.id)
            db.session.add(alumno)

        alumno.padron = q_padron
        db.session.commit()

        result = ({'OK': "El padron ha sido modificado"}, SUCCESS_OK)
        logging.info('Modificar Padron Alumno devuelve como resultado: {}'.format(result))

        return result


    def es_valido(self, padron, id_alumno):
        if not padron:
            return False

        if not padron.isdigit() or not (LONGITUD_MINIMA_PADRON<=len(padron)<=LONGITUD_MAXIMA_PADRON):
            return False

        alumnos = Alumno.query.filter_by(padron=padron).filter(Alumno.id.isnot(id_alumno)).all()
        return len(alumnos) == 0
