from app.API_Rest.codes import *
from flask_user import login_required
from app.API_Rest.Services.BaseService import BaseService
from app.models.carreras_models import Carrera, Materia
from app.models.alumno_models import AlumnosCarreras, MateriasAlumno
from app.DAO.MateriasDAO import *


class CarreraAlumnoService(BaseService):
    def getNombreClaseServicio(self):
        return "Carrera Alumno Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    @login_required
    def put(self):
        self.logg_parametros_recibidos()

        alumno = self.obtener_alumno_usuario_actual()

        if not alumno:
            msj = "El usuario no tiene ningun alumno asociado"
            self.logg_error(msj)
            return {'Error': msj}, CLIENT_ERROR_NOT_FOUND

        idCarrera = self.obtener_parametro("idCarrera")

        parametros_son_validos, msj, codigo = self.validar_parametros(dict([
            ("idCarrera", {
                self.PARAMETRO: idCarrera,
                self.ES_OBLIGATORIO: True,
                self.FUNCIONES_VALIDACION: [
                    (self.id_es_valido, []),
                    (self.existe_id, [Carrera]),
                    (self.carrera_no_fue_agregada_anteriormente, [])
                ]
            })
        ]))

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': msj}, codigo

        carrera_nueva = AlumnosCarreras(alumno_id=alumno.id, carrera_id=idCarrera)

        db.session.add(carrera_nueva)
        db.session.commit()

        self.agregar_materias_carrera(alumno.id, idCarrera)

        result = SUCCESS_NO_CONTENT
        self.logg_resultado(result)

        return result

    @login_required
    def delete(self, idCarrera):
        self.logg_parametros_recibidos()

        alumno = self.obtener_alumno_usuario_actual()

        if not alumno:
            msj = "El usuario no tiene ningun alumno asociado"
            self.logg_error(msj)
            return {'Error': msj}, CLIENT_ERROR_NOT_FOUND

        parametros_son_validos, msj, codigo = self.validar_parametros(dict([
            ("idCarrera", {
                self.PARAMETRO: idCarrera,
                self.ES_OBLIGATORIO: True,
                self.FUNCIONES_VALIDACION: [
                    (self.id_es_valido, []),
                    (self.existe_id, [Carrera]),
                    (self.carrera_pertenece_al_alumno, [])
                ]
            })
        ]))

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': msj}, codigo

        AlumnosCarreras.query.filter_by(alumno_id=alumno.id).filter_by(carrera_id=idCarrera).delete()
        db.session.commit()

        self.eliminar_materias_carrera(alumno.id, idCarrera)

        result = SUCCESS_NO_CONTENT
        self.logg_resultado(result)

        return result

    def eliminar_materias_carrera(self, id_alumno, id_carrera):
        query = MateriasAlumno.query.filter_by(alumno_id=id_alumno).filter_by(carrera_id=id_carrera)
        query.delete()
        db.session.commit()

    def agregar_materias_carrera(self, id_alumno, id_carrera):
        materias_carrera = Materia.query.filter_by(carrera_id=id_carrera).all()
        estado_pendiente = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[PENDIENTE]).first()

        for materia_carrera in materias_carrera:
            db.session.add(MateriasAlumno(
                alumno_id=id_alumno,
                materia_id=materia_carrera.id,
                estado_id=estado_pendiente.id,
                carrera_id=id_carrera
            ))

        db.session.commit()

    def carrera_pertenece_al_alumno(self, nombre_parametro, id_carrera, es_obligatorio):
        alumno = self.obtener_alumno_usuario_actual()

        existe_carrera = AlumnosCarreras.query.filter_by(alumno_id=alumno.id).filter_by(carrera_id=id_carrera).first()

        return self.mensaje_OK(nombre_parametro) if existe_carrera \
            else (False, 'La carrera {} no pertenece al alumno'.format(id_carrera), CLIENT_ERROR_BAD_REQUEST)

    def carrera_no_fue_agregada_anteriormente(self, nombre_parametro, id_carrera, es_obligatorio):
        if not id_carrera and not es_obligatorio:
            return True, 'El {} no existe'.format(nombre_parametro), -1

        alumno = self.obtener_alumno_usuario_actual()

        existe_carrera = AlumnosCarreras.query.filter_by(alumno_id=alumno.id).filter_by(carrera_id=id_carrera).first()

        msj = 'El campo {} con valor {} es '.format(nombre_parametro, id_carrera)
        return (True, msj + 'valido', -1) if not existe_carrera else (False, msj + 'invalido', CLIENT_ERROR_BAD_REQUEST)


#########################################
CLASE = CarreraAlumnoService
URLS_SERVICIOS = (
    '/api/alumno/carrera',
    '/api/alumno/carrera/<int:idCarrera>'
)
#########################################
