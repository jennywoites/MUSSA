from flask_restful import Resource
from app.API_Rest.codes import *
from flask import request

from flask_user import current_user, login_required

from app.models.alumno_models import Alumno, MateriasAlumno, EstadoMateria, FormaAprobacionMateria
from app.models.carreras_models import Carrera, Materia
from app import db

from app.DAO.MateriasDAO import *
from datetime import date
from datetime import datetime

import logging


class EliminarMateriaAlumno(Resource):
    @login_required
    def post(self):
        args = request.form

        logging.info('''Se invoco al servicio Eliminar Materia Alumno con los siguientes
            parametros: {}. Este servicio no elimina la materia de la BDD sino que coloca
            la materia como pendiente'''.format(args))

        q_id_materia_alumno = args["id_materia"] if "id_materia" in args else None

        alumno = Alumno.query.filter_by(user_id=current_user.id).first()

        if (not q_id_materia_alumno or
                not self.es_materia_valida(q_id_materia_alumno, alumno.id)):
            logging.error('El servicio Eliminar Materia Alumno debe recibir el id de carrera valida para el alumno')
            return {'Error': 'Es necesario un id de materia válido para el alumno'}, CLIENT_ERROR_BAD_REQUEST

        query_materia = MateriasAlumno.query.filter_by(alumno_id=alumno.id)
        materia = query_materia.filter_by(id=q_id_materia_alumno).first()

        estado_desaprobado = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[DESAPROBADA]).first()

        se_elimino_materia_actual = False
        if materia.estado_id == estado_desaprobado.id:
            se_elimino_materia_actual = self.eliminar_correspondientes_desaprobadas(materia)

        if se_elimino_materia_actual:
            result = ({'OK': "Se eliminó la materia satisfactoriamente (se elimino la entrada actual)"}, SUCCESS_OK)
            logging.info('Eliminar Materia Alumno devuelve como resultado: {}'.format(result))
            return result

        estado_pendiente = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[PENDIENTE]).first()
        materia.estado_id = estado_pendiente.id

        self.anular_datos_materia(materia)

        db.session.commit()

        result = ({'OK': "Se eliminó la materia satisfactoriamente (queda como pendiente)"}, SUCCESS_OK)
        logging.info('Eliminar Materia Alumno devuelve como resultado: {}'.format(result))

        return result

    def eliminar_correspondientes_desaprobadas(self, materia):
        se_elimino_materia_actual = False

        estado_desaprobado = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[DESAPROBADA]).first()
        estado_pendiente = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[PENDIENTE]).first()

        query = MateriasAlumno.query.filter_by(alumno_id=materia.alumno_id)
        query = query.filter_by(materia_id=materia.materia_id)
        otras_materias = query.filter(MateriasAlumno.id.isnot(materia.id)).all()

        a_eliminar = []
        for otra in otras_materias:
            if otra.estado_id == estado_pendiente.id:
                a_eliminar.append(otra.id)

        if len(a_eliminar) == 0:
            se_elimino_materia_actual = True
            a_eliminar.append(materia.id)

        MateriasAlumno.query.filter_by(id=materia.id).delete()
        db.session.commit()

        return se_elimino_materia_actual

    def es_materia_valida(self, id_materia, alumno_id):
        query_materia = MateriasAlumno.query.filter_by(alumno_id=alumno_id)
        materia = query_materia.filter_by(id=id_materia).first()
        return (materia is not None)

    def anular_datos_materia(self, materia):
        materia.calificacion = None
        materia.fecha_aprobacion = None
        materia.cuatrimestre_aprobacion_cursada = None
        materia.anio_aprobacion_cursada = None
        materia.acta_o_resolucion = ''
        materia.forma_aprobacion_id = None
