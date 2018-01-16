from app.API_Rest.codes import *
from flask_user import login_required
from app.API_Rest.Services.BaseService import BaseService
from app.models.generadorJSON.alumno_generadorJSON import generarJSON_alumno
from app.models.alumno_models import Alumno


class AlumnoService(BaseService):
    def getNombreClaseServicio(self):
        return "Alumno Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    @login_required
    def get(self, idAlumno):
        self.logg_parametros_recibidos()

        parametros_son_validos, msj, codigo = self.validar_parametros({
            "idAlumno": {
                self.PARAMETRO: idAlumno,
                self.ES_OBLIGATORIO: True,
                self.FUNCIONES_VALIDACION: {
                    self.id_es_valido: [],
                    self.existe_id: [Alumno],
                    self.alumno_es_usuario_actual: []
                }
            }
        })

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': msj}, codigo

        alumno = Alumno.query.get(idAlumno)
        alumno_result = generarJSON_alumno(alumno)

        result = ({'alumno': alumno_result}, SUCCESS_OK)
        self.logg_resultado(result)

        return result


#########################################
CLASE = AlumnoService
URLS_SERVICIOS = (
    '/api/alumno/<int:idAlumno>',
)
#########################################
