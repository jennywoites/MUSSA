from app.API_Rest.codes import *
from flask_user import login_required
from app.API_Rest.Services.BaseService import BaseService
from app.models.generadorJSON.respuestas_encuestas_generadorJSON import generarJSON_encuesta_alumno
from app.models.respuestas_encuesta_models import EncuestaAlumno


class AllEncuestaAlumnoService(BaseService):
    def getNombreClaseServicio(self):
        return "All Encuesta Alumno Service"

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

        finalizada = self.obtener_booleano("finalizada")

        parametros_son_validos, msj, codigo = self.validar_parametros(dict([
            ("finalizada", {
                self.PARAMETRO: finalizada,
                self.ES_OBLIGATORIO: False,
                self.FUNCIONES_VALIDACION: [
                    (self.booleano_es_valido, [])
                ]
            })
        ]))

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': msj}, codigo

        query = EncuestaAlumno.query.filter_by(alumno_id=alumno.id)
        if finalizada is not None:
            query = query.filter_by(finalizada=finalizada)

        result_encuestas = []
        for encuesta in query.all():
            result_encuestas.append(generarJSON_encuesta_alumno(encuesta))

        result = ({"encuestas": result_encuestas}, SUCCESS_OK)
        self.logg_resultado(result)

        return result


#########################################
CLASE = AllEncuestaAlumnoService
URLS_SERVICIOS = (
    '/api/alumno/encuesta/all',
)
#########################################
