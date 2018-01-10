from flask_restful import Resource
from app.API_Rest.codes import *
from flask import request
from app import db
from flask_user import current_user, login_required
from app.models.alumno_models import Alumno, MateriasAlumno
from app.models.respuestas_encuesta_models import EncuestaAlumno, RespuestaEncuestaTags, RespuestaEncuestaTematica
from app.models.palabras_clave_models import PalabrasClaveParaMateria, TematicaPorMateria

import logging


class FinalizarEncuestaAlumnoService(Resource):
    @login_required
    def post(self):
        args = request.form
        logging.info(
            'Se invoco al servicio Finalizar Encuesta alumno con los siguientes parametros: {}'.format(args))

        id_encuesta = args["id_encuesta"] if "id_encuesta" in args else None

        alumno = Alumno.query.filter_by(user_id=current_user.id).first()

        if not self.id_encuesta_es_valido(id_encuesta, alumno):
            logging.error('El servicio recibió un id de encuesta invalido')
            return {'Error': 'El servicio recibió un id de encuesta invalido'}, CLIENT_ERROR_BAD_REQUEST

        encuesta = EncuestaAlumno.query.filter_by(id=id_encuesta).filter_by(alumno_id=alumno.id).first()

        if encuesta.finalizada:
            logging.error('El servicio recibió un id de encuesta ya finalizada')
            return {'Error': 'El servicio recibió un id de encuesta ya finalizada'}, CLIENT_ERROR_PRECONDITION_FAILED

        encuesta.finalizada = True
        db.session.commit()

        materiaAlumno = MateriasAlumno.query.get(encuesta.materia_alumno_id)

        self.agregarPalabrasClavesALasMaterias(encuesta, materiaAlumno.materia_id)
        self.agregarTematicasALasMaterias(encuesta, materiaAlumno.materia_id)

        result = SUCCESS_NO_CONTENT
        logging.info('Finalizar Encuesta alumno  devuelve como resultado: {}'.format(result))

        return result

    def agregarPalabrasClavesALasMaterias(self, encuesta, id_materia):
        respuestas = RespuestaEncuestaTags.query.filter_by(rta_encuesta_alumno_id=encuesta.id).all()
        for respuesta in respuestas:
            entrada = PalabrasClaveParaMateria(
                materia_id=id_materia,
                palabra_clave_id=respuesta.palabra_clave_id
            )
            db.session.add(entrada)
            db.session.commit()

    def agregarTematicasALasMaterias(self, encuesta, id_materia):
        respuestas = RespuestaEncuestaTematica.query.filter_by(rta_encuesta_alumno_id=encuesta.id).all()
        for respuesta in respuestas:
            entrada = TematicaPorMateria(
                materia_id=id_materia,
                tematica_id=respuesta.tematica_id
            )
            db.session.add(entrada)
            db.session.commit()

    def id_encuesta_es_valido(self, id_encuesta, alumno):
        if not id_encuesta or not id_encuesta.isdigit():
            return False

        return EncuestaAlumno.query.filter_by(id=id_encuesta).filter_by(alumno_id=alumno.id).first()
