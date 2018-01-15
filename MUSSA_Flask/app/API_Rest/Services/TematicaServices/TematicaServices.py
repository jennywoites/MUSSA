from app.API_Rest.codes import *
from flask_user import roles_accepted
from app.models.palabras_clave_models import TematicaMateria
from app.models.generadorJSON.palabras_clave_generadorJSON import generarJSON_tematica_materia
from app.API_Rest.Services.BaseService import BaseService


class TematicaService(BaseService):
    def getNombreClaseServicio(self):
        return "Tematica Service"

    @roles_accepted('admin')
    def get(self, idTematica):
        self.logg_parametros_recibidos()

        parametros_son_validos, msj, codigo = self.validar_parametros({
            "idTematica": {
                self.PARAMETRO: idTematica,
                self.ES_OBLIGATORIO: True,
                self.FUNCIONES_VALIDACION: {
                    self.id_es_valido: [],
                    self.existe_id: [TematicaMateria]
                }
            }
        })

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': msj}, codigo

        tematica = TematicaMateria.query.get(idTematica)
        tematica_result = generarJSON_tematica_materia(tematica)

        result = (tematica_result, SUCCESS_OK)
        self.logg_resultado(result)
        return result


#########################################
CLASE = TematicaService
URLS_SERVICIOS = (
    '/api/tematica/<int:idTematica>',
)
#########################################
