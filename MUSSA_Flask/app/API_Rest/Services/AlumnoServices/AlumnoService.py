from app.API_Rest.codes import *
from flask_user import login_required
from app.API_Rest.Services.BaseService import BaseService
from app.models.generadorJSON.alumno_generadorJSON import generarJSON_alumno

class AlumnoService(BaseService):
    def getNombreClaseServicio(self):
        return "Alumno Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    @login_required
    def get(self):
        self.logg_parametros_recibidos()

        alumno = self.obtener_alumno_usuario_actual()

        if not alumno:
            msj = "El usuario no tiene ningun alumno asociado"
            self.logg_error(msj)
            return {'Error': msj}, CLIENT_ERROR_NOT_FOUND

        alumno_result = generarJSON_alumno(alumno)

        result = ({'alumno': alumno_result}, SUCCESS_OK)
        self.logg_resultado(result)

        return result

#########################################
CLASE = AlumnoService
URLS_SERVICIOS = (
    '/api/alumno',
)
#########################################
