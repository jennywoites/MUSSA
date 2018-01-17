from app.API_Rest.codes import *
from flask_user import roles_accepted
from app.models.palabras_clave_models import TematicaMateria
from app.models.generadorJSON.palabras_clave_generadorJSON import generarJSON_tematica_materia
from app.API_Rest.Services.BaseService import BaseService


class TematicaService(BaseService):
    def getNombreClaseServicio(self):
        return "Tematica Service"

    @roles_accepted('admin')
    def get(self, idTematica):
        return self.servicio_get_base(idTematica, "idTematica", TematicaMateria, generarJSON_tematica_materia)


#########################################
CLASE = TematicaService
URLS_SERVICIOS = (
    '/api/tematica/<int:idTematica>',
)
#########################################
