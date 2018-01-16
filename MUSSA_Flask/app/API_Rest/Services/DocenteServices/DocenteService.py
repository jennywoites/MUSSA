from app.API_Rest.codes import *
from app.models.docentes_models import Docente
from app import db
from flask_user import roles_accepted
from app.API_Rest.Services.BaseService import BaseService
from app.models.generadorJSON.docentes_generadorJSON import generarJSON_docente
from app.models.docentes_models import CursosDocente
from app.models.horarios_models import Curso


class DocenteService(BaseService):
    def getNombreClaseServicio(self):
        return "Docente Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    def get(self, idDocente):
        return self.servicio_get_base(idDocente, "idDocente", Docente, generarJSON_docente)

    @roles_accepted('admin')
    def delete(self, idDocente):
        self.servicio_delete_base(idDocente, "idDocente", Docente)

    @roles_accepted('admin')
    def post(self, idDocente):
        self.logg_parametros_recibidos()

        apellido = self.obtener_texto('apellido')
        nombre = self.obtener_texto('nombre')

        if not nombre or not apellido:
            msj = "Uno o más parámetros requeridos no fueron enviados"
            self.logg_error(msj)
            return {'Error': msj}, CLIENT_ERROR_BAD_REQUEST

        l_ids_cursos = self.obtener_lista('l_ids_cursos')

        parametros_son_validos, msj, codigo = self.validar_parametros({
            "idDocente": {
                self.PARAMETRO: idDocente,
                self.ES_OBLIGATORIO: True,
                self.FUNCIONES_VALIDACION: [
                    (self.id_es_valido, []),
                    (self.existe_id, [Docente])
                ]
            },
            "apellido": {
                self.PARAMETRO: apellido,
                self.ES_OBLIGATORIO: True,
                self.FUNCIONES_VALIDACION: [
                    (self.validar_contenido_y_longitud_texto, [3, 35])
                ]
            },
            "nombre": {
                self.PARAMETRO: nombre,
                self.ES_OBLIGATORIO: True,
                self.FUNCIONES_VALIDACION: [
                    (self.validar_contenido_y_longitud_texto, [0, 40])
                ]
            },
            "l_ids_cursos": {
                self.PARAMETRO: l_ids_cursos,
                self.ES_OBLIGATORIO: True,
                self.FUNCIONES_VALIDACION: [
                    (self.id_es_valido, []),
                    (self.existe_id, [Curso])
                ]
            }
        })

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': msj}, codigo

        self.actualizar_datos_docente(idDocente, apellido, nombre)

        self.actualizar_cursos_que_dicta_el_docente(idDocente, l_ids_cursos)

        result = SUCCESS_OK
        self.logg_resultado(result)

        return result

    def actualizar_datos_docente(self, idDocente, apellido, nombre):
        docente = Docente.query.get(idDocente)
        docente.apellido = apellido
        docente.nombre = nombre
        db.session.commit()

    def actualizar_cursos_que_dicta_el_docente(self, idDocente, l_ids_cursos):
        CursosDocente.query.filter_by(docente_id=idDocente).delete()
        db.session.commit()

        for id_curso in l_ids_cursos:
            db.session.add(CursosDocente(
                docente_id=idDocente,
                curso_id=id_curso
            ))
            db.session.commit()


#########################################
CLASE = DocenteService
URLS_SERVICIOS = (
    '/api/docente/<int:idDocente>',
)
#########################################
