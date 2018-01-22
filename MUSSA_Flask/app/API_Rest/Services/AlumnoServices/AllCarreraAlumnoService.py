from app.API_Rest.codes import *
from flask_user import login_required
from app.API_Rest.Services.BaseService import BaseService
from app.models.generadorJSON.carreras_generadorJSON import generarJSON_carrera
from app.models.alumno_models import AlumnosCarreras
from app.models.carreras_models import Carrera


class AllCarreraAlumnoService(BaseService):
    def getNombreClaseServicio(self):
        return "All Carrera Alumno Service"

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

        carreras_result = []
        for carrera_alumno in AlumnosCarreras.query.filter_by(alumno_id=alumno.id).all():
            carrera = Carrera.query.get(carrera_alumno.carrera_id)
            carreras_result.append(generarJSON_carrera(carrera))

        result = ({'carreras': carreras_result}, SUCCESS_OK)
        self.logg_resultado(result)

        return result


#########################################
CLASE = AllCarreraAlumnoService
URLS_SERVICIOS = (
    '/api/alumno/carrera/all',
)
#########################################
