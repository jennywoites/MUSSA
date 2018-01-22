from app.API_Rest.codes import *
from flask_user import login_required
from app.API_Rest.Services.BaseService import BaseService
from app.models.generadorJSON.alumno_generadorJSON import generarJSON_materia_alumno
from app.models.alumno_models import MateriasAlumno


class MateriaAlumnoService(BaseService):
    def getNombreClaseServicio(self):
        return "Materia Alumno Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    @login_required
    def get(self, idMateriaAlumno):
        self.logg_parametros_recibidos()

        alumno = self.obtener_alumno_usuario_actual()

        if not alumno:
            msj = "El usuario no tiene ningun alumno asociado"
            self.logg_error(msj)
            return {'Error': msj}, CLIENT_ERROR_NOT_FOUND

        parametros_son_validos, msj, codigo = self.validar_parametros(dict([
            self.get_validaciones_materia_alumno("idMateriaAlumno", idMateriaAlumno, True)
        ]))

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': msj}, codigo

        materia_alumno = MateriasAlumno.query.get(idMateriaAlumno)
        materia_alumno_result = generarJSON_materia_alumno(materia_alumno)

        result = ({'materia_alumno': materia_alumno_result}, SUCCESS_OK)
        self.logg_resultado(result)

        return result


#########################################
CLASE = MateriaAlumnoService
URLS_SERVICIOS = (
    '/api/alumno/materia/<int:idMateriaAlumno>',
)
#########################################
