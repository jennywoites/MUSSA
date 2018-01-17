from app.API_Rest.Services.BaseService import BaseService
from app.models.carreras_models import Materia, Correlativas
from app.API_Rest.codes import *
from app.models.generadorJSON.carreras_generadorJSON import generarJSON_materia

class CorrelativasService(BaseService):
    def getNombreClaseServicio(self):
        return "Correlativas Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    def get(self, idMateria):
        self.logg_parametros_recibidos()

        parametros_son_validos, msj, codigo = self.validar_parametros(dict([
            self.get_validaciones_entidad_basica("idMateria", idMateria, Materia)
        ]))

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': msj}, codigo

        correlativas = Correlativas.query.filter_by(materia_id=idMateria).all()

        materias_result = []
        for correlativa in correlativas:
            materia_correlativa = Materia.query.get(correlativa.materia_correlativa_id)
            materias_result.append(generarJSON_materia(materia_correlativa))

        materias_result.sort(
            key=lambda materia : materia["codigo"] if len(materia["codigo"]) > 1 else "0" + materia["codigo"]
        )

        result = ({'correlativas': materias_result}, SUCCESS_OK)
        self.logg_resultado(result)

        return result


#########################################
CLASE = CorrelativasService
URLS_SERVICIOS = (
    '/api/materia/<int:idMateria>/correlativas',
)
#########################################
