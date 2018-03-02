from app.API_Rest.Services.BaseService import BaseService
from app.models.horarios_models import Curso
from app.API_Rest.codes import *
from app.DAO.EncuestasDAO import *


class ResultadosEncuestaCursoService(BaseService):
    def getNombreClaseServicio(self):
        return "Resultados Encuesta Curso Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    def get(self, idCurso):
        self.logg_parametros_recibidos()

        parametros_son_validos, msj, codigo = self.validar_parametros(dict([
            self.get_validaciones_entidad_basica("idCurso", idCurso, Curso, True)
        ]))

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': msj}, codigo

        resultados_json = [{
            "cuatrimestre": "1",
            "anio": "2016",
            "resultados": [{
                "pregunta": "Cómo le parecieron las clases a los alumnos",
                "tipo_pregunta": "Puntaje 1 a 5",
                "id_tipo_pregunta": PUNTAJE_1_A_5,
                "respuesta": {
                    "puntaje_promedio": 3,
                    "puntajes": [{
                        "puntaje": 3,
                        "cantidad_encuestas": 2,
                        "porcentaje": 100
                    }]
                }
            }]
        }]

        result = (resultados_json, SUCCESS_OK)
        self.logg_resultado(result)

        return result


#########################################
CLASE = ResultadosEncuestaCursoService
URLS_SERVICIOS = (
    '/api/encuesta/resultados/curso/<int:idCurso>',
)
#########################################
