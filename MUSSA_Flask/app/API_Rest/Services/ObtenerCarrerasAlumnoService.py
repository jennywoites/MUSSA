from flask_restful import Resource
from app.API_Rest.codes import *
from flask import request

from flask_user import current_user, login_required
from app.models.alumno_models import Alumno, AlumnosCarreras
from app.models.carreras_models import Carrera

from app import db

import logging


class ObtenerCarrerasAlumno(Resource):
    @login_required
    def get(self):
        args = request.args
        logging.info('Se invoco al servicio Obtener Carreras Alumno con los siguientes parametros: {}'.format(args))

        if args:
            logging.error('El servicio Obtener Carreras Alumno no recibe parámteros')
            return {'Error': 'Este servicio no recibe parámetros'}, CLIENT_ERROR_BAD_REQUEST

        alumno = Alumno.query.filter_by(user_id=current_user.id).first()

        if not alumno:
            logging.info('Se crea el alumno para el usuario {}'.format(current_user.id))
            alumno = Alumno(user_id=current_user.id)
            db.session.add(alumno)
            db.session.commit()

        carreras = AlumnosCarreras.query.filter_by(alumno_id=alumno.id).all()

        carreras_result = []
        for carrera_alumno in carreras:
            carrera = Carrera.query.get(carrera_alumno.carrera_id)
            carreras_result.append({
                'id': carrera.id,
                'codigo': carrera.codigo,
                'nombre': carrera.nombre,
                'plan': carrera.plan
            })

        result = ({'carreras': carreras_result}, SUCCESS_OK)
        logging.info('Obtener Carreras Alumno devuelve como resultado: {}'.format(result))

        return result
