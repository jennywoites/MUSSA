from flask_user import login_required
from app.API_Rest.Services.BaseService import BaseService
from app.models.generadorJSON.respuestas_encuestas_generadorJSON import generarJSON_encuesta_alumno
from app.models.respuestas_encuesta_models import EncuestaAlumno, RespuestaEncuestaTematica, RespuestaEncuestaTags
from app.models.palabras_clave_models import PalabrasClaveParaMateria, TematicaPorMateria
from app.models.alumno_models import MateriasAlumno
from app.API_Rest.codes import *
from app import db


class EncuestaAlumnoService(BaseService):
    def getNombreClaseServicio(self):
        return "Encuesta Alumno Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    @login_required
    def get(self, idEncuestaAlumno):
        self.logg_parametros_recibidos()

        parametros_son_validos, msj, codigo = self.validar_parametros(dict([
            ("idEncuestaAlumno", {
                self.PARAMETRO: idEncuestaAlumno,
                self.ES_OBLIGATORIO: True,
                self.FUNCIONES_VALIDACION: [
                    (self.id_es_valido, []),
                    (self.existe_id, [EncuestaAlumno]),
                    (self.encuesta_pertenece_al_alumno, [])
                ]
            })
        ]))

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': msj}, codigo

        encuesta = EncuestaAlumno.query.get(idEncuestaAlumno)

        result = (generarJSON_encuesta_alumno(encuesta), SUCCESS_OK)
        self.logg_resultado(result)

        return result

    @login_required
    def post(self, idEncuestaAlumno):
        self.logg_parametros_recibidos()

        alumno = self.obtener_alumno_usuario_actual()

        if not alumno:
            msj = "El usuario no tiene ningun alumno asociado"
            self.logg_error(msj)
            return {'Error': msj}, CLIENT_ERROR_NOT_FOUND

        finalizada = self.obtener_booleano("finalizada")

        parametros_son_validos, msj, codigo = self.validar_parametros(dict([
            ("idEncuestaAlumno", {
                self.PARAMETRO: idEncuestaAlumno,
                self.ES_OBLIGATORIO: True,
                self.FUNCIONES_VALIDACION: [
                    (self.id_es_valido, []),
                    (self.existe_id, [EncuestaAlumno]),
                    (self.encuesta_pertenece_al_alumno, []),
                    (self.encuesta_no_esta_finalizada, [])
                ]
            }),
            ("finalizada", {
                self.PARAMETRO: finalizada,
                self.ES_OBLIGATORIO: True,
                self.FUNCIONES_VALIDACION: [
                    (self.booleano_es_valido, [])
                ]
            })
        ]))

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': msj}, codigo

        encuesta = EncuestaAlumno.query.get(idEncuestaAlumno)
        encuesta.finalizada = finalizada
        db.session.commit()

        materiaAlumno = MateriasAlumno.query.get(encuesta.materia_alumno_id)

        self.agregarPalabrasClavesALasMaterias(encuesta, materiaAlumno.materia_id)
        self.agregarTematicasALasMaterias(encuesta, materiaAlumno.materia_id)

        result = SUCCESS_NO_CONTENT
        self.logg_resultado(result)

        return result

    def agregarPalabrasClavesALasMaterias(self, encuesta, id_materia):
        respuestas = RespuestaEncuestaTags.query.filter_by(rta_encuesta_alumno_id=encuesta.id).all()
        for respuesta in respuestas:
            entrada = PalabrasClaveParaMateria(
                materia_id=id_materia,
                palabra_clave_id=respuesta.palabra_clave_id
            )
            db.session.add(entrada)
            db.session.commit()

    def agregarTematicasALasMaterias(self, encuesta, id_materia):
        respuestas = RespuestaEncuestaTematica.query.filter_by(rta_encuesta_alumno_id=encuesta.id).all()
        for respuesta in respuestas:
            entrada = TematicaPorMateria(
                materia_id=id_materia,
                tematica_id=respuesta.tematica_id
            )
            db.session.add(entrada)
            db.session.commit()

    def encuesta_no_esta_finalizada(self, nombre_parametro, valor, esObligatorio):
        encuesta = EncuestaAlumno.query.get(valor)
        return self.mensaje_OK(nombre_parametro) if not encuesta.finalizada \
            else (False, 'La encuesta ya se encuentra finalizada', CLIENT_ERROR_METHOD_NOT_ALLOWED)


#########################################
CLASE = EncuestaAlumnoService
URLS_SERVICIOS = (
    '/api/alumno/encuesta/<int:idEncuestaAlumno>',
)
#########################################
