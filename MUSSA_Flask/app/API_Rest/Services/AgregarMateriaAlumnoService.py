from flask_restful import Resource
from app.API_Rest.codes import *
from flask import request
from flask_user import current_user, login_required
from app.models.alumno_models import Alumno, MateriasAlumno
from app.models.carreras_models import Carrera, Materia
from app.models.horarios_models import Curso
from app.models.docentes_models import CursosDocente, Docente
from app.models.respuestas_encuesta_models import EncuestaAlumno, EstadoPasosEncuestaAlumno
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
        q_id_curso = args["id_curso"] if "id_curso" in args else None
        q_estado = args["estado"] if "estado" in args else None

        alumno = Alumno.query.filter_by(user_id=current_user.id).first()

        if (not q_id_carrera or not q_id_materia or not q_estado or not alumno or not q_id_curso
            or not self.son_ids_validos(q_id_carrera, q_id_materia, q_id_curso, q_estado, alumno.id)):
            logging.error(
                'El servicio Agregar Materia Alumno debe recibir el id de carrera, materia, curso y el estado')
            return {
                       'Error': 'No se han enviado uno o más parámetros requeridos o éstos no son válidos (id carrera, id materia, id_curso, estado)'}, CLIENT_ERROR_BAD_REQUEST

        query_materia = MateriasAlumno.query.filter_by(alumno_id=alumno.id)
        query_materia = query_materia.filter_by(materia_id=q_id_materia)

        # No modificar materias en estado final (aprobada o desaprobada)
        estado_aprobado = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[APROBADA]).first()
        estado_desaprobado = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[DESAPROBADA]).first()
        estados_finalizados = [estado_aprobado.id, estado_desaprobado.id]
        query_materia = query_materia.filter(~MateriasAlumno.estado_id.in_(estados_finalizados))

        materia = query_materia.filter_by(carrera_id=q_id_carrera).first()

        estado = EstadoMateria.query.filter_by(estado=q_estado).first()

        materia.estado_id = estado.id

        self.anular_datos_materia(materia)

        if (q_id_curso != "-1"):  # Si es -1 significa que no hay un curso designado
            materia.curso_id = int(q_id_curso)

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

        if materia.curso_id:  # Solo se generan encuestas si la materia tiene un curso seleccionado
            self.crear_o_actualizar_encuesta(materia)

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

        if (q_estado == ESTADO_MATERIA[DESAPROBADA]):
            # En caso de que la materia este desaprobada, se puede volver a cursar
            # por lo que se agrega esta materia como una nueva entrada pendiente
            self.agregar_materia_pendiente(materia)

        return self.guardar_y_devolver_success()

    def son_ids_validos(self, id_carrera, id_materia, id_curso, estado, alumno_id):
        if not id_carrera.isdigit() or not Carrera.query.filter_by(id=id_carrera).first():
            return False

        if not id_materia.isdigit() or not MateriasAlumno.query.filter_by(materia_id=id_materia).first():
            return False

        if ((id_curso != "-1" and not id_curso.isdigit()) or
                (id_curso != "-1" and not Curso.query.filter_by(id=id_curso).first())):
            return False

        if not EstadoMateria.query.filter_by(estado=estado).first():
            return False

        query_materia = MateriasAlumno.query.filter_by(alumno_id=alumno_id)
        query_materia = query_materia.filter_by(materia_id=id_materia)
        materia = query_materia.filter_by(carrera_id=id_carrera).first()
        return (materia is not None)

    def anular_datos_materia(self, materia):
        materia.calificacion = None
        materia.curso_id = None
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

    def agregar_materia_pendiente(self, materia):
        estado_pendiente = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[PENDIENTE]).first()

        db.session.add(MateriasAlumno(
            alumno_id=materia.alumno_id,
            materia_id=materia.materia_id,
            estado_id=estado_pendiente.id,
            carrera_id=materia.carrera_id
        ))
        db.session.commit()

    def crear_o_actualizar_encuesta(self, materia_alumno):
        encuesta = EncuestaAlumno.query.filter_by(materia_alumno_id=materia_alumno.id).first()

        if encuesta and encuesta.finalizada:  # No modificar encuestas finalizadas
            return

        if not encuesta:
            encuesta = self.crear_encuesta(materia_alumno)

        curso = Curso.query.filter_by(id=materia_alumno.curso_id).first()
        docentes = ""
        for cdoc in CursosDocente.query.filter_by(curso_id=materia_alumno.curso_id).all():
            docente = Docente.query.filter_by(id=cdoc.docente_id).first()
            docentes += docente.obtener_nombre_completo() + "-"
        encuesta.curso = "{}: {}".format(curso.codigo, docentes[:-1])

        encuesta.cuatrimestre_aprobacion_cursada = materia_alumno.cuatrimestre_aprobacion_cursada
        encuesta.anio_aprobacion_cursada = materia_alumno.anio_aprobacion_cursada
        encuesta.finalizada = False
        db.session.commit()

    def crear_encuesta(self, materia_alumno):
        encuesta = EncuestaAlumno(
            alumno_id=materia_alumno.alumno_id,
            materia_alumno_id=materia_alumno.id,
            cuatrimestre_aprobacion_cursada=materia_alumno.cuatrimestre_aprobacion_cursada,
            anio_aprobacion_cursada=materia_alumno.anio_aprobacion_cursada,
            finalizada=False
        )
        db.session.add(encuesta)
        db.session.commit()

        estado_pasos = EstadoPasosEncuestaAlumno(encuesta_alumno_id=encuesta.id)
        estado_pasos.inicializar_pasos()
        db.session.add(estado_pasos)
        db.session.commit()

        return encuesta
