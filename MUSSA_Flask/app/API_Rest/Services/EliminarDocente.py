from flask_restful import Resource
from app.API_Rest.codes import *
from flask import request

from flask_user import login_required
from app.models.docentes_models import Docente

from app import db

import logging

class EliminarDocente(Resource):
    
    @login_required
    def post(self):
        args = request.form

        logging.info('Se invoco al servicio Eliminar Docente: {}'.format(args))

        q_id_docente = args["id_docente"] if "id_docente" in args else None

        if not q_id_docente or not self.es_valido(q_id_docente):
            logging.error('El servicio Eliminar Docente debe recibir el id de docente')
            return {'Error': 'Este servicio debe recibir un id de docente válido'}, CLIENT_ERROR_BAD_REQUEST

        docente = Docente.query.get(q_id_docente)
        if not docente:
            error_msg = 'El docente con id {} no existe.'.format(q_id_docente)
            logging.error(error_msg)
            return {'Error': error_msg}, CLIENT_ERROR_NOT_FOUND

        docente.delete()
        db.session.commit()

        result = ({'OK': "El docente ha sido eliminado"}, SUCCESS_OK)
        logging.info('Eliminar Carrera Alumno devuelve como resultado: {}'.format(result))

        return result

    def es_valido(self, id_docente):
        return  id_docente.isdigit()