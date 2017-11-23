from flask_restful import Resource
from app.API_Rest.codes import *
from flask import request

from flask_user import current_user, login_required
from app.models.alumno_models import Alumno, AlumnosCarreras, MateriasAlumno
from app.models.carreras_models import Carrera, Materia

from app import db

from app.DAO.MateriasDAO import *

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

        self.agregar_materias_carrera(alumno.id, q_id_carrera)

        result = ({'OK': "La carrera ha sido guardada"}, SUCCESS_OK)
        logging.info('Agregar Carrera Alumno devuelve como resultado: {}'.format(result))

        return result


    def es_valido(self, id_carrera):
        return len(Carrera.query.filter_by(id=id_carrera).all()) == 1


    def carrera_ya_fue_agregada(self, id_alumno, id_carrera):
        query = AlumnosCarreras.query.filter_by(alumno_id=id_alumno).filter_by(carrera_id=id_carrera)
        return len(query.all()) > 0


    def agregar_materias_carrera(self, id_alumno, id_carrera):
        materias_carrera = Materia.query.filter_by(carrera_id=id_carrera).all()
        estado_pendiente = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[PENDIENTE]).first()

        for materia_carrera in materias_carrera:
            db.session.add(MateriasAlumno(
                alumno_id = id_alumno,
                materia_id = materia_carrera.id,
                estado_id = estado_pendiente.id,
                carrera_id = id_carrera
            ))

        db.session.commit()