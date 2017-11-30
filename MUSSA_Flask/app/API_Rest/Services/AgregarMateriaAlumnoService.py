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

class AgregarMateriaAlumno(Resource):

    @login_required
    def post(self):
        args = request.form

        logging.info('Se invoco al servicio Agregar Materia Alumno con los siguientes parametros: {}'.format(args))

        q_id_carrera = args["id_carrera"] if "id_carrera" in args else None
        q_id_materia = args["id_materia"] if "id_materia" in args else None
        q_estado = args["estado"] if "estado" in args else None

        alumno = Alumno.query.filter_by(user_id=current_user.id).first()

        if (not q_id_carrera or not q_id_materia or not q_estado
            or not self.son_ids_validos(q_id_carrera, q_id_materia, q_estado, alumno.id)):
            logging.error('El servicio Agregar Materia Alumno debe recibir el id de carrera, materia y el estado')
            return {'Error': 'No se han enviado uno o más parámetros requeridos o éstos no son válidos (id carrera, id materia, estado)'}, CLIENT_ERROR_BAD_REQUEST

        query_materia = MateriasAlumno.query.filter_by(alumno_id=alumno.id)
        query_materia = query_materia.filter_by(materia_id=q_id_materia)
        materia = query_materia.filter_by(carrera_id=q_id_carrera).first()

        estado = EstadoMateria.query.filter_by(estado=q_estado).first()

        materia.estado_id = estado.id
                
        self.anular_datos_materia(materia)
        
        if (q_estado == ESTADO_MATERIA[EN_CURSO]):
            return self.guardar_y_devolver_success()

        q_cuatrimestre_aprobacion = args["cuatrimestre_aprobacion"] if "cuatrimestre_aprobacion" in args else None
        q_anio_aprobacion = args["anio_aprobacion"] if "anio_aprobacion" in args else None

        if not self.fecha_aprobacion_cursada_es_valida(q_cuatrimestre_aprobacion, q_anio_aprobacion):
            msj = 'Requiere el cuatrimestre y año de aprobación de cursada'
            logging.error(msj)
            return {'Error': msj}, CLIENT_ERROR_BAD_REQUEST

        materia.cuatrimestre_aprobacion_cursada = q_cuatrimestre_aprobacion
        materia.anio_aprobacion_cursada = q_anio_aprobacion

        if (q_estado == ESTADO_MATERIA[FINAL_PENDIENTE]):
            return self.guardar_y_devolver_success()

        q_fecha_aprobacion = args["fecha_aprobacion"] if "fecha_aprobacion" in args else None
        q_forma_aprobacion = args["forma_aprobacion"] if "forma_aprobacion" in args else None
        q_calificacion = args["calificacion"] if "calificacion" in args else None
        q_acta_resolucion = args["acta_resolucion"] if "acta_resolucion" in args else None

        if not self.datos_aprobacion_son_validos(q_fecha_aprobacion, q_forma_aprobacion,
            q_calificacion, q_acta_resolucion, estado.estado):
            msj = 'Requiere la fecha y forma de aprobación, la calificación y el acta o resolución'
            logging.error(msj)
            return {'Error': msj}, CLIENT_ERROR_BAD_REQUEST

        anio, mes, dia = q_fecha_aprobacion.split("-")
        materia.fecha_aprobacion = date(int(anio), int(mes), int(dia))

        materia.forma_aprobacion_id = FormaAprobacionMateria.query.filter_by(forma=q_forma_aprobacion).first().id

        materia.calificacion = int(q_calificacion)
        materia.acta_o_resolucion = q_acta_resolucion

        return self.guardar_y_devolver_success()


    def son_ids_validos(self, id_carrera, id_materia, estado, alumno_id):
        if not Carrera.query.filter_by(id=id_carrera).first():
            return False

        if not MateriasAlumno.query.filter_by(id=id_materia).first():
            return False

        if not EstadoMateria.query.filter_by(estado=estado).first():
            return False

        query_materia = MateriasAlumno.query.filter_by(alumno_id=alumno_id)
        query_materia = query_materia.filter_by(materia_id=id_materia)
        materia = query_materia.filter_by(carrera_id=id_carrera).first()
        return (materia is not None)


    def anular_datos_materia(self, materia):
        materia.calificacion = None
        materia.fecha_aprobacion = None
        materia.cuatrimestre_aprobacion_cursada = None
        materia.anio_aprobacion_cursada = None
        materia.acta_o_resolucion = ''
        materia.forma_aprobacion_id = None


    def fecha_aprobacion_cursada_es_valida(self, cuatrimestre, anio):
        if (cuatrimestre != '1' and cuatrimestre != '2'):
            return False

        MAX_TIEMPO = 10
        hoy = datetime.now().year
        anios = [str(x) for x in range(hoy, hoy - MAX_TIEMPO, -1)]
        return (anio in anios)


    def datos_aprobacion_son_validos(self, fecha_aprobacion, forma_aprobacion,
            calificacion, acta_resolucion, estado):
        try:
            anio, mes, dia = fecha_aprobacion.split("-")
            date(int(anio), int(mes), int(dia))
        except Exception as e:
            return False

        if len(FormaAprobacionMateria.query.filter_by(forma=forma_aprobacion).all()) == 0:
            return False

        calificacion = int(calificacion)
        if calificacion < 2 or calificacion > 10:
            return False

        if estado == "Desaprobado" and calificacion >= 4:
            return False

        if estado == "Aprobado" and calificacion < 4:
            return False

        return (acta_resolucion != "")


    def guardar_y_devolver_success(self):
        db.session.commit()

        result = ({'OK': "Se agrego la materia satisfactoriamente"}, SUCCESS_OK)
        logging.info('Agregar Materia Alumno devuelve como resultado: {}'.format(result))
        return result