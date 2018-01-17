from app.API_Rest.Services.BaseService import BaseService
from app.models.generadorJSON.horarios_generadorJSON import generarJSON_curso
from app.models.horarios_models import Curso


class CursoService(BaseService):
    def getNombreClaseServicio(self):
        return "Curso Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    def get(self, idCurso):
        return self.servicio_get_base(idCurso, "idCurso", Curso, generarJSON_curso)


#########################################
CLASE = CursoService
URLS_SERVICIOS = (
    '/api/curso/<int:idCurso>',
)
#########################################
