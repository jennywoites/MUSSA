from flask_restful import Resource
from app.API_Rest.codes import *
from flask import request

from flask_user import current_user, login_required
from app.models.alumno_models import Alumno, AlumnosCarreras
from app.models.carreras_models import Carrera

from app import db

import logging

class AgregarCarreraAlumno(Resource):
    
    @login_required
    def post(self):
        args = request.form

        logging.info('Se invoco al servicio Agregar Carrera Alumno con los siguientes parametros: {}'.format(args))

        q_id_carrera = args["id_carrera"] if "id_carrera" in args else None

        if not q_id_carrera or not self.es_valido(q_id_carrera):
            logging.error('El servicio Agregar Carrera Alumno debe recibir el id de carrera')
            return {'Error': 'Este servicio debe recibir un id de carrera válido'}, CLIENT_ERROR_BAD_REQUEST

        alumno = Alumno.query.filter_by(user_id=current_user.id).first()

        if self.carrera_ya_fue_agregada(alumno.id, q_id_carrera):
            logging.error('El alumno ya tiene esta carrera agregada')
            return {'Error': 'No es posible agregar la carrera ya que fue agregada anteriormente.'}, CLIENT_ERROR_BAD_REQUEST

        carrera_nueva = AlumnosCarreras(alumno_id=alumno.id, carrera_id=q_id_carrera)

        db.session.add(carrera_nueva)
        db.session.commit()

        result = ({'OK': "La carrera ha sido guardada"}, SUCCESS_OK)
        logging.info('Agregar Carrera Alumno devuelve como resultado: {}'.format(result))

        return result


    def es_valido(self, id_carrera):
        return len(Carrera.query.filter_by(id=id_carrera).all()) == 1


    def carrera_ya_fue_agregada(self, id_alumno, id_carrera):
        query = AlumnosCarreras.query.filter_by(alumno_id=id_alumno).filter_by(carrera_id=id_carrera)
        return len(query.all()) > 0
