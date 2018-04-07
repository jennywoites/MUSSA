from app.API_Rest.codes import *
from app.models.docentes_models import Docente
from app.models.generadorJSON.docentes_generadorJSON import generarJSON_docente
from app.API_Rest.Services.BaseService import BaseService
from sqlalchemy import or_


class AllDocentesService(BaseService):
    def getNombreClaseServicio(self):
        return "All Docentes Service"

    def get(self):
        self.logg_parametros_recibidos()

        nombre = self.obtener_texto("nombre")
        apellido = self.obtener_texto("apellido")

        parametros_son_validos, msj, codigo = self.validar_parametros(dict([
            ("nombre", {
                self.PARAMETRO: nombre,
                self.ES_OBLIGATORIO: False,
                self.FUNCIONES_VALIDACION: [
                    (self.validar_contenido_y_longitud_texto, [1, 40])
                ]
            }),
            ("apellido", {
                self.PARAMETRO: apellido,
                self.ES_OBLIGATORIO: False,
                self.FUNCIONES_VALIDACION: [
                    (self.validar_contenido_y_longitud_texto, [1, 35])
                ]
            })
        ]))

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': msj}, codigo

        docentes_result = []

        query = Docente.query.filter_by(eliminado=False)

        if nombre:
            query = query.filter(Docente.apellido.like("%" + nombre + "%"))

        if apellido:
            query = query.filter(Docente.apellido.like("%" + apellido + "%"))

        docentes = query.order_by(Docente.apellido.asc()).order_by(Docente.nombre.asc()).all()

        for docente in docentes:
            docentes_result.append(generarJSON_docente(docente))

        result = ({'docentes': docentes_result}, SUCCESS_OK)
        self.logg_resultado(result)

        return result


#########################################
CLASE = AllDocentesService
URLS_SERVICIOS = (
    '/api/docente/all',
)
#########################################
