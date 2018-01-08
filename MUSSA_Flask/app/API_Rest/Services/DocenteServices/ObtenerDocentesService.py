from flask_restful import Resource
from app.API_Rest.codes import *
from app.models.docentes_models import Docente

import logging
from app.API_Rest.Services.DocenteServices.DocenteService import DocenteService

class ObtenerDocentesService(Resource):
    def getNombreClaseServicio(self):
        return "Obtener Docentes Service"

    def get(self):
        docentes_result = []

        query = Docente.query
        docentes = query.order_by(Docente.apellido.asc()).order_by(Docente.nombre.asc()).all()

        docenteService = DocenteService()

        for docente in docentes:
            docentes_result.append(docenteService.generarJSONDocente(docente))

        result = ({'docentes': docentes_result}, SUCCESS_OK)
        logging.info(self.getNombreClaseServicio() + ': Resultado: {}'.format(result))

        return result

#########################################
CLASE = ObtenerDocentesService
URLS_SERVICIOS = (
    '/api/docente/all',
)
#########################################
