from app.API_Rest.Services.BaseService import BaseService
from app.models.generadorJSON.carreras_generadorJSON import generarJSON_carrera
from app.models.carreras_models import Carrera


class CarreraService(BaseService):
    def getNombreClaseServicio(self):
        return "Carrera Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    def get(self, idCarrera):
        return self.servicio_get_base(idCarrera, "idCarrera", Carrera, generarJSON_carrera)


#########################################
CLASE = CarreraService
URLS_SERVICIOS = (
    '/api/carrera/<int:idCarrera>',
)
#########################################
