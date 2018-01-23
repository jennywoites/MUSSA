from flask_user import login_required
from app.API_Rest.Services.BaseService import BaseService
from app.models.generadorJSON.respuestas_encuestas_generadorJSON import generarJSON_encuesta_alumno
from app.models.respuestas_encuesta_models import EncuestaAlumno


class EncuestaAlumnoService(BaseService):
    def getNombreClaseServicio(self):
        return "Encuesta Alumno Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    @login_required
    def get(self, idEncuestaAlumno):
        return self.servicio_get_base(idEncuestaAlumno, "idEncuestaAlumno", EncuestaAlumno, generarJSON_encuesta_alumno)


#########################################
CLASE = EncuestaAlumnoService
URLS_SERVICIOS = (
    '/api/alumno/encuesta/<int:idEncuestaAlumno>',
)
#########################################
