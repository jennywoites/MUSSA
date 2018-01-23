from flask_user import login_required
from app.API_Rest.Services.BaseService import BaseService
from app.models.respuestas_encuesta_models import EncuestaAlumno, EstadoPasosEncuestaAlumno
from app.API_Rest.codes import *


class EstadoEncuestaAlumnoService(BaseService):
    def getNombreClaseServicio(self):
        return "Encuesta Alumno Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    @login_required
    def get(self, idEncuestaAlumno):
        self.logg_parametros_recibidos()

        parametros_son_validos, msj, codigo = self.validar_parametros(dict([
            ("idEncuestaAlumno", {
                self.PARAMETRO: idEncuestaAlumno,
                self.ES_OBLIGATORIO: True,
                self.FUNCIONES_VALIDACION: [
                    (self.id_es_valido, []),
                    (self.existe_id, [EncuestaAlumno]),
                    (self.encuesta_pertenece_al_alumno, [])
                ]
            })
        ]))

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': msj}, codigo

        pasos = EstadoPasosEncuestaAlumno.query.filter_by(encuesta_alumno_id=idEncuestaAlumno).first()

        result = ({'esta_completa': pasos.estan_todos_los_pasos_completos()}, SUCCESS_OK)
        self.logg_resultado(result)

        return result

#########################################
CLASE = EstadoEncuestaAlumnoService
URLS_SERVICIOS = (
    '/api/alumno/encuesta/<int:idEncuestaAlumno>/completa',
)
#########################################
