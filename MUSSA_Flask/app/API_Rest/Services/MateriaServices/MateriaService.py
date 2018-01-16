from app.API_Rest.Services.BaseService import BaseService
from app.models.generadorJSON.carreras_generadorJSON import generarJSON_materia
from app.models.carreras_models import Materia


class MateriaService(BaseService):
    def getNombreClaseServicio(self):
        return "Materia Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    def get(self, idMateria):
        return self.servicio_get_base(idMateria, "idMateria", Materia, generarJSON_materia)


#########################################
CLASE = MateriaService
URLS_SERVICIOS = (
    '/api/materia/<int:idMateria>',
)
#########################################
