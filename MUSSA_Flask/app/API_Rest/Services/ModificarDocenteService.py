from flask_restful import Resource
from app.API_Rest.codes import *
from flask import request

from app.models.horarios_models import Horario, Curso, CarreraPorCurso, HorarioPorCurso
from app.models.carreras_models import Carrera
from app.models.docentes_models import Docente, CursosDocente

import logging
from flask_user import roles_accepted
from app import db

from app.utils import DIAS


class ModificarDocente(Resource):

    @roles_accepted('admin')
    def post(self):
        return 'Todo piola'
        args = request.args
        if not args["id_docente"]:
            return {'Error': 'No se envio el id_docente'}, CLIENT_ERROR_BAD_REQUEST
        docente = Docente.get(int(args["id_docente"]))
        if not docente:
            return {'Error': 'Id de docente no valido'}, CLIENT_ERROR_BAD_REQUEST

        return "OK"
