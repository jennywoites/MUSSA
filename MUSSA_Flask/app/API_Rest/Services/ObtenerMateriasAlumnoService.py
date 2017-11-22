from flask_restful import Resource
from app.API_Rest.codes import *
from flask import request

from flask_user import current_user, login_required

from app.models.alumno_models import Alumno, MateriasAlumno, EstadoMateria, FormaAprobacionMateria
from app.models.carreras_models import Carrera, Materia
from app import db

from app.DAO.MateriasDAO import *

import logging

class ObtenerMateriasAlumno(Resource):

    @login_required
    def get(self):
        args = request.args
        logging.info('Se invoco al servicio Obtener Materias Alumno con los siguientes parametros: {}'.format(args))

        estados = self.obtener_ids_estados(args)

        id_materia_alumno = args["id_materia_alumno"] if "id_materia_alumno" in args else None

        alumno = Alumno.query.filter_by(user_id=current_user.id).first()

        query = MateriasAlumno.query.filter_by(alumno_id=alumno.id)

        if id_materia_alumno:
            query = query.filter_by(id=id_materia_alumno)

        if estados:
            query = query.filter(MateriasAlumno.estado_id.in_(estados))

        materias = query.all()

        materias_result = []
        for materia_alumno in materias:
            materia_carrera = Materia.query.filter_by(id=materia_alumno.materia_id).first()
            carrera = Carrera.query.filter_by(id=materia_alumno.carrera_id).first()
            estado = EstadoMateria.query.filter_by(id=materia_alumno.estado_id).first().estado
            
            calificacion = materia_alumno.calificacion if materia_alumno.calificacion else "-"

            fecha_aprobacion = "-"
            if materia_alumno.fecha_aprobacion:
                anio, mes, dia = str(materia_alumno.fecha_aprobacion ).split(" ")[0].split("-")
                fecha_aprobacion = "{}/{}/{}".format(dia, mes, anio)

            aprobacion_cursada = "-"
            if (materia_alumno.cuatrimestre_aprobacion_cursada and
                materia_alumno.anio_aprobacion_cursada):
                aprobacion_cursada = materia_alumno.cuatrimestre_aprobacion_cursada  + "C / "
                aprobacion_cursada += materia_alumno.anio_aprobacion_cursada

            acta_o_resolucion = materia_alumno.acta_o_resolucion if materia_alumno.acta_o_resolucion else "-"

            forma_aprobacion_materia = "-"
            if materia_alumno.forma_aprobacion_id:
                query = FormaAprobacionMateria.query.filter_by(id=materia_alumno.forma_aprobacion_id)
                forma_aprobacion_materia = query.first().forma

            materias_result.append({
                'id': materia_alumno.id,
                'id_materia': materia_carrera.id,
                'codigo': materia_carrera.codigo,
                'nombre': materia_carrera.nombre,
                'id_carrera': carrera.id,
                'carrera': carrera.nombre + " (" + carrera.plan + ")",
                'estado': estado,
                'aprobacion_cursada': aprobacion_cursada,
                'calificacion': calificacion,
                'fecha_aprobacion': fecha_aprobacion,
                'acta_o_resolucion': acta_o_resolucion,
                'forma_aprobacion_materia': forma_aprobacion_materia
            })

        result = ({'materias': materias_result}, SUCCESS_OK)
        logging.info('Buscar Materias Alumno devuelve como resultado: {}'.format(result))

        return result

    def obtener_ids_estados(self, args):
        ids_estados = []

        estados = args["estados"].split(";") if "estados" in args else []
        for cod_estado in estados:
            texto = ESTADO_MATERIA[int(cod_estado)]
            estado = EstadoMateria.query.filter_by(estado=texto).first()
            ids_estados.append(estado.id)

        return ids_estados