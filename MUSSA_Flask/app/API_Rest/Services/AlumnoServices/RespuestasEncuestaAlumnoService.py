from flask_user import login_required
from app.API_Rest.Services.BaseService import BaseService
from app.models.encuestas_models import PreguntaEncuesta
from app.models.respuestas_encuesta_models import EncuestaAlumno
from app.models.filtros.respuestas_encuestas_filter import filtrar_respuesta_encuesta
from app.models.generadorJSON.respuestas_encuestas_generadorJSON import generarJSON_respuesta_pregunta
from app.API_Rest.codes import *


class RespuestasEncuestaAlumnoService(BaseService):
    def getNombreClaseServicio(self):
        return "Respuestas Encuesta Alumno Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    @login_required
    def get(self, idEncuestaAlumno):
        self.logg_parametros_recibidos()

        ids_preguntas = self.obtener_lista("ids_preguntas")

        parametros_son_validos, msj, codigo = self.validar_parametros(dict([
            ("idEncuestaAlumno", {
                self.PARAMETRO: idEncuestaAlumno,
                self.ES_OBLIGATORIO: True,
                self.FUNCIONES_VALIDACION: [
                    (self.id_es_valido, []),
                    (self.existe_id, [EncuestaAlumno]),
                    (self.encuesta_pertenece_al_alumno, [])
                ]
            }),
            self.get_validaciones_entidad_basica("ids_preguntas", ids_preguntas, PreguntaEncuesta, True)
        ]))

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': msj}, codigo

        filtro = {}
        filtro["idEncuestaAlumno"] = idEncuestaAlumno
        if ids_preguntas:
            filtro["ids_preguntas"] = ids_preguntas

        preguntas_result = {}
        for respuesta_encuesta in filtrar_respuesta_encuesta(filtro):
            datos = generarJSON_respuesta_pregunta(respuesta_encuesta)
            if datos:
                preguntas_result[respuesta_encuesta.pregunta_encuesta_id] = datos

        result = ({'respuestas_encuestas': preguntas_result}, SUCCESS_OK)
        self.logg_resultado(result)

        return result


#########################################
CLASE = RespuestasEncuestaAlumnoService
URLS_SERVICIOS = (
    '/api/alumno/encuesta/<int:idEncuestaAlumno>/respuestas',
)
#########################################
