from app.API_Rest.codes import *
from app.models.docentes_models import Docente
from app import db
from flask_user import roles_accepted
from app.API_Rest.Services.BaseService import BaseService
from app.models.generadorJSON.docentes_generadorJSON import generarJSON_docente


class DocenteService(BaseService):
    def getNombreClaseServicio(self):
        return "Docente Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    def get(self, idDocente):
        self.logg_parametros_recibidos()

        parametros_son_validos, msj, codigo = self.validar_parametros({
            "idDocente": self.validaciones_id_docente(idDocente)
        })

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': 'msj'}, codigo

        docente = Docente.query.get(idDocente)
        docente_result = generarJSON_docente(docente)

        result = (docente_result, SUCCESS_OK)
        self.logg_resultado(result)

        return result

    @roles_accepted('admin')
    def delete(self, idDocente):
        self.logg_parametros_recibidos()

        parametros_son_validos, msj, codigo = self.validar_parametros({
            "idDocente": self.validaciones_id_docente(idDocente)
        })

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': 'msj'}, codigo

        Docente.query.filter_by(id=idDocente).delete()
        db.session.commit()

        result = SUCCESS_NO_CONTENT
        self.logg_resultado(result)

        return result

    def validaciones_id_docente(self, idDocente):
        return {
            self.PARAMETRO: idDocente,
            self.ES_OBLIGATORIO: True,
            self.FUNCIONES_VALIDACION: {
                self.id_es_valido: [],
                self.existe_id: [Docente]
            }
        }

#########################################
CLASE = DocenteService
URLS_SERVICIOS = (
    '/api/docente/<int:idDocente>',
)
#########################################
