from flask_restful import Resource
from app.API_Rest.codes import *
from app.models.docentes_models import Docente, CursosDocente
from app.models.carreras_models import Materia, Carrera
from app.models.horarios_models import Curso
from app import db
from flask_user import roles_accepted
import logging


class DocenteService(Resource):

    def getNombreClaseServicio(self):
        return "Docente Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    def get(self, idDocente):
        if not idDocente > 0:
            logging.error(self.getNombreClaseServicio() + ': El id docente debe ser un entero mayor a 0')
            return {'Error': 'El id docente debe ser un entero mayor a 0'}, CLIENT_ERROR_NOT_FOUND

        if not self.existe_id_docente(idDocente):
            logging.error(self.getNombreClaseServicio() + ': El id docente no existe')
            return {'Error': 'El id docente no existe'}, CLIENT_ERROR_NOT_FOUND

        docente = Docente.query.get(idDocente)
        docente_result = self.generarJSONDocente(docente)

        result = (docente_result, SUCCESS_OK)
        logging.info(self.getNombreClaseServicio() + ': Resultado: {}'.format(result))

        return result

    @roles_accepted('admin')
    def delete(self, idDocente):
        if not idDocente > 0:
            logging.error(self.getNombreClaseServicio() + ': El id docente debe ser un entero mayor a 0')
            return {'Error': 'El id docente debe ser un entero mayor a 0'}, CLIENT_ERROR_NOT_FOUND

        if not self.existe_id_docente(idDocente):
            logging.error(self.getNombreClaseServicio() + ': El id docente no existe')
            return {'Error': 'El id docente no existe'}, CLIENT_ERROR_NOT_FOUND

        Docente.query.filter_by(id=idDocente).delete()
        db.session.commit()

        result = SUCCESS_NO_CONTENT
        logging.info(self.getNombreClaseServicio() + ': Resultado: {}'.format(result))

        return result

    ##########################################
    ##          Funciones Auxiliares        ##
    ##########################################

    def existe_id_docente(self, id_docente):
        return Docente.query.filter_by(id=id_docente).first()

    def generarJSONDocente(self, docente):
        return {
            "id_docente": docente.id,
            "apellido": docente.apellido,
            "nombre": docente.nombre,
            "nombre_completo": docente.obtener_nombre_completo(),
            "materias_que_dicta": self.generarJSONMateriasDocente(docente)
        }

    def generarJSONMateriasDocente(self, docente):
        materias = {}

        cursos_del_docente = CursosDocente.query.filter_by(docente_id=docente.id).all()
        for c in cursos_del_docente:
            curso = Curso.query.filter_by(id=c.curso_id).first()
            materia = Materia.query.filter_by(codigo=curso.codigo_materia).first()
            carrera = Carrera.query.filter_by(id=materia.carrera_id).first()
            materias[materia.codigo] = {
                "nombre": materia.nombre,
                "id_carrera": materia.carrera_id,
                "carrera": carrera.get_descripcion_carrera()
            }

        return materias

#########################################
CLASE = DocenteService
URLS_SERVICIOS = (
    '/api/docente/<int:idDocente>',
)
#########################################
