from app.API_Rest.codes import *
from app.models.docentes_models import Docente
from app.models.generadorJSON.docentes_generadorJSON import generarJSON_docente
from app.API_Rest.Services.BaseService import BaseService


class AllDocentesService(BaseService):
    def getNombreClaseServicio(self):
        return "All Docentes Service"

    def get(self):
        self.logg_parametros_recibidos()

        docentes_result = []

        query = Docente.query
        docentes = query.order_by(Docente.apellido.asc()).order_by(Docente.nombre.asc()).all()

        for docente in docentes:
            docentes_result.append(generarJSON_docente(docente))

        result = ({'docentes': docentes_result}, SUCCESS_OK)
        self.logg_resultado(result)

        return result


#########################################
CLASE = AllDocentesService
URLS_SERVICIOS = (
    '/api/docente/all',
)
#########################################
