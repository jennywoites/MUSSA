from app.API_Rest.codes import *
from flask_user import login_required
from app.API_Rest.Services.BaseService import BaseService
from app.models.generadorJSON.alumno_generadorJSON import generarJSON_materia_alumno
from app.models.alumno_models import MateriasAlumno
from app.DAO.MateriasDAO import *


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

    @login_required
    def delete(self, idMateriaAlumno):
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

        materia = MateriasAlumno.query.get(idMateriaAlumno)

        se_elimino_materia_actual = False
        if materia.estado_id == EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[DESAPROBADA]).first().id:
            se_elimino_materia_actual = self.eliminar_correspondientes_desaprobadas(materia)

        if se_elimino_materia_actual:
            result = SUCCESS_NO_CONTENT
            self.logg_resultado(result)
            return result

        materia.estado_id = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[PENDIENTE]).first().id
        self.anular_datos_materia(materia)
        db.session.commit()

        result = SUCCESS_NO_CONTENT
        self.logg_resultado(result)

        return result

    def eliminar_correspondientes_desaprobadas(self, materia):
        se_elimino_materia_actual = False

        estado_desaprobado = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[DESAPROBADA]).first()
        estado_pendiente = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[PENDIENTE]).first()

        query = MateriasAlumno.query.filter_by(alumno_id=materia.alumno_id)
        query = query.filter_by(materia_id=materia.materia_id)
        otras_materias = query.filter(MateriasAlumno.id.isnot(materia.id)).all()

        a_eliminar = []
        for otra in otras_materias:
            if otra.estado_id == estado_pendiente.id:
                a_eliminar.append(otra.id)

        if len(a_eliminar) == 0:
            se_elimino_materia_actual = True
            a_eliminar.append(materia.id)

        MateriasAlumno.query.filter_by(id=materia.id).delete()
        db.session.commit()

        return se_elimino_materia_actual

    def es_materia_valida(self, id_materia, alumno_id):
        query_materia = MateriasAlumno.query.filter_by(alumno_id=alumno_id)
        materia = query_materia.filter_by(id=id_materia).first()
        return (materia is not None)

    def anular_datos_materia(self, materia):
        materia.calificacion = None
        materia.fecha_aprobacion = None
        materia.cuatrimestre_aprobacion_cursada = None
        materia.anio_aprobacion_cursada = None
        materia.acta_o_resolucion = ''
        materia.forma_aprobacion_id = None


#########################################
CLASE = MateriaAlumnoService
URLS_SERVICIOS = (
    '/api/alumno/materia/<int:idMateriaAlumno>',
)
#########################################
