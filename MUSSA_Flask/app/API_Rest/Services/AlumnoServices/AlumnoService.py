from app.API_Rest.codes import *
from flask_user import login_required
from app.API_Rest.Services.BaseService import BaseService
from app.models.generadorJSON.alumno_generadorJSON import generarJSON_alumno
from app import db


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

    @login_required
    def post(self):
        self.logg_parametros_recibidos()

        alumno = self.obtener_alumno_usuario_actual()

        if not alumno:
            msj = "El usuario no tiene ningun alumno asociado"
            self.logg_error(msj)
            return {'Error': msj}, CLIENT_ERROR_NOT_FOUND

        padron = self.obtener_texto("padron")

        parametros_son_validos, msj, codigo = self.validar_parametros(dict([
            ("padron", {
                self.PARAMETRO: padron,
                self.ES_OBLIGATORIO: True,
                self.FUNCIONES_VALIDACION: [
                    (self.padron_es_valido, [alumno.id])
                ]
            })
        ]))

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': msj}, codigo

        alumno.padron = padron
        db.session.commit()

        result = SUCCESS_NO_CONTENT
        self.logg_resultado(result)

        return result


#########################################
CLASE = AlumnoService
URLS_SERVICIOS = (
    '/api/alumno',
)
#########################################
