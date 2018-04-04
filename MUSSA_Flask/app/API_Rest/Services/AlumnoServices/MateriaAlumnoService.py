from app.API_Rest.codes import *
from flask_user import login_required
from app.API_Rest.Services.BaseService import BaseService
from app.models.generadorJSON.alumno_generadorJSON import generarJSON_materia_alumno
from app.models.alumno_models import MateriasAlumno
from app.models.carreras_models import Materia, MateriasIncompatibles
from app.models.respuestas_encuesta_models import EncuestaAlumno, EstadoPasosEncuestaAlumno, RespuestaEncuestaTematica, \
    RespuestaEncuestaTags, RespuestaEncuestaAlumno
from app.models.palabras_clave_models import PalabrasClaveParaMateria, TematicaPorMateria
from app.models.horarios_models import Curso
from app.models.docentes_models import Docente, CursosDocente
from app.DAO.MateriasDAO import *
from datetime import date
from datetime import datetime
from app.API_Rest.Services.AlumnoServices.RespuestasEncuestaAlumnoService import RespuestasEncuestaAlumnoService


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
    def put(self):
        self.logg_parametros_recibidos()

        alumno = self.obtener_alumno_usuario_actual()

        if not alumno:
            msj = "El usuario no tiene ningun alumno asociado"
            self.logg_error(msj)
            return {'Error': msj}, CLIENT_ERROR_NOT_FOUND

        datos_materia = self.obtener_parametros_materia()

        parametros_son_validos, msj, codigo = self.validar_parametros(dict([
            ("idMateriaAlumno", {
                self.PARAMETRO: datos_materia["idMateriaAlumno"],
                self.ES_OBLIGATORIO: True,
                self.FUNCIONES_VALIDACION: [
                    (self.id_es_valido, []),
                    (self.existe_id, [MateriasAlumno]),
                    (self.materia_pertenece_al_alumno, []),
                    (self.materia_tiene_estado_pendiente, [])
                ]
            }),
            self.datos_validacion_id_curso(datos_materia),
            ("estado", {
                self.PARAMETRO: datos_materia["estado"],
                self.ES_OBLIGATORIO: True,
                self.FUNCIONES_VALIDACION: [
                    (self.existe_el_elemento, [EstadoMateria, EstadoMateria.estado]),
                    (self.es_estado_materia_valido, [])
                ]
            }),
            self.datos_validacion_cuatrimestre(datos_materia),
            self.datos_validacion_anio_aprobacion(datos_materia),
            self.datos_validacion_fecha_aprobacion(datos_materia),
            self.datos_validacion_forma_aprobacion(datos_materia),
            self.datos_validacion_calificacion(datos_materia),
            self.datos_validacion_acta_o_resolucion(datos_materia)
        ]))

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': msj}, codigo

        self.actualizar_materia_alumno(datos_materia)

        result = SUCCESS_NO_CONTENT
        self.logg_resultado(result)

        return result

    @login_required
    def post(self, idMateriaAlumno):
        self.logg_parametros_recibidos()

        alumno = self.obtener_alumno_usuario_actual()

        if not alumno:
            msj = "El usuario no tiene ningun alumno asociado"
            self.logg_error(msj)
            return {'Error': msj}, CLIENT_ERROR_NOT_FOUND

        datos_materia = self.obtener_parametros_materia()
        datos_materia["idMateriaAlumno"] = idMateriaAlumno
        datos_materia["idCurso"] = None  # No está permitido el cambio de curso

        parametros_son_validos, msj, codigo = self.validar_parametros(dict([
            ("idMateriaAlumno", {
                self.PARAMETRO: datos_materia["idMateriaAlumno"],
                self.ES_OBLIGATORIO: True,
                self.FUNCIONES_VALIDACION: [
                    (self.id_es_valido, []),
                    (self.existe_id, [MateriasAlumno]),
                    (self.materia_pertenece_al_alumno, []),
                    (self.materia_permite_ser_modificada, [])
                ]
            }),
            ("estado", {
                self.PARAMETRO: datos_materia["estado"],
                self.ES_OBLIGATORIO: True,
                self.FUNCIONES_VALIDACION: [
                    (self.existe_el_elemento, [EstadoMateria, EstadoMateria.estado]),
                    (self.nuevo_estado_materia_es_valido, [datos_materia["idMateriaAlumno"]])
                ]
            }),
            self.datos_validacion_cuatrimestre(datos_materia),
            self.datos_validacion_anio_aprobacion(datos_materia),
            self.datos_validacion_fecha_aprobacion(datos_materia),
            self.datos_validacion_forma_aprobacion(datos_materia),
            self.datos_validacion_calificacion(datos_materia),
            self.datos_validacion_acta_o_resolucion(datos_materia)
        ]))

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': msj}, codigo

        self.actualizar_materia_alumno(datos_materia)

        result = SUCCESS_NO_CONTENT
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

        self.eliminar_encuesta_asociada(materia)

        self.actualizar_materias_incompatibles_al_eliminar_materia(materia)

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

    def eliminar_encuesta_asociada(self, materia_alumno):
        """
        Elimina la encuesta y las respuestas asociadas a la materia alumno.
        Si la encuesta estaba finalizada:
        - Se actualizan los datos de cantidad y encuestas y puntaje correspondientes
        para la materia asociada.
        - Se actualizan los tags / palabras clave
        - Se actualizan las temáticas    def actualizar_puntaje_y_cantidad_encuestas_curso(self, encuesta, id_curso):
        """
        encuesta = EncuestaAlumno.query.filter_by(materia_alumno_id=materia_alumno.id).first()
        if not encuesta:
            return

        if encuesta.finalizada:
            self.disminuir_estrellas_curso(materia_alumno, encuesta)
            self.eliminarPalabrasClavesALasMaterias(materia_alumno.materia_id, encuesta)
            self.eliminarTematicasALasMaterias(materia_alumno.materia_id, encuesta)

        self.eliminar_encuesta_y_respuestas(encuesta)

    def disminuir_estrellas_curso(self, materia_alumno, encuesta):
        estrellas_encuesta = encuesta.obtener_cantidad_estrellas_elegidas()

        curso = Curso.query.get(materia_alumno.curso_id)
        curso.puntaje_total_encuestas -= estrellas_encuesta
        curso.cantidad_encuestas_completas -= 1
        db.session.commit()

        self.logg_info("Se disminuyeron las estrellas del curso en {} estrellas".format(estrellas_encuesta))

    def eliminarPalabrasClavesALasMaterias(self, id_materia, encuesta):
        respuestas = RespuestaEncuestaTags.query.filter_by(rta_encuesta_alumno_id=encuesta.id).all()
        for respuesta in respuestas:
            entrada = PalabrasClaveParaMateria.query.filter_by(materia_id=id_materia) \
                .filter_by(palabra_clave_id=respuesta.palabra_clave_id).first()
            if not entrada:
                continue
            entrada.cantidad_encuestas_asociadas -= 1
            db.session.commit()
            self.logg_info("Se disminuyó la cantidad de encuestas asociadas con la palabra clave de"
                           " id {} relacionada con la materia de id {}".format(respuesta.palabra_clave_id, id_materia))

            if entrada.cantidad_encuestas_asociadas == 0:
                PalabrasClaveParaMateria.query.filter_by(materia_id=id_materia) \
                    .filter_by(palabra_clave_id=respuesta.palabra_clave_id).delete()
                db.session.commit()
                self.logg_info("Se elimino la palabra clave de id {} relacionada con la "
                               "materia de id {}".format(respuesta.palabra_clave_id, id_materia))

    def eliminarTematicasALasMaterias(self, id_materia, encuesta):
        respuestas = RespuestaEncuestaTematica.query.filter_by(rta_encuesta_alumno_id=encuesta.id).all()
        for respuesta in respuestas:
            entrada = TematicaPorMateria.query.filter_by(materia_id=id_materia). \
                filter_by(tematica_id=respuesta.tematica_id).first()
            entrada.cantidad_encuestas_asociadas -= 1
            db.session.commit()
            self.logg_info("Se disminuyó la cantidad de encuestas asociadas con la tematica de"
                           " id {} relacionada con la materia de id {}".format(respuesta.tematica_id, id_materia))

            if entrada.cantidad_encuestas_asociadas == 0:
                TematicaPorMateria.query.filter_by(materia_id=id_materia). \
                    filter_by(tematica_id=respuesta.tematica_id).delete()
                db.session.commit()
                self.logg_info("Se elimino la tematica de id {} relacionada con la "
                               "materia de id {}".format(respuesta.tematica_id, id_materia))

    def eliminar_encuesta_y_respuestas(self, encuesta):
        respuestas_encuestas = RespuestaEncuestaAlumno.query.filter_by(encuesta_alumno_id=encuesta.id).all()
        servicio_respuesta_encuesta = RespuestasEncuestaAlumnoService()
        servicio_respuesta_encuesta.eliminar_respuestas(respuestas_encuestas)
        db.session.commit()

        RespuestaEncuestaAlumno.query.filter_by(encuesta_alumno_id=encuesta.id).delete()
        db.session.commit()

        EstadoPasosEncuestaAlumno.query.filter_by(encuesta_alumno_id=encuesta.id).delete()
        db.session.commit()

        EncuestaAlumno.query.filter_by(id=encuesta.id).delete()
        db.session.commit()
        self.logg_info("Se eliminaron las respuestas asociadas a la encuesta")

    def datos_validacion_cuatrimestre(self, datos_materia):
        return ("cuatrimestre_aprobacion", {
            self.PARAMETRO: datos_materia["cuatrimestre_aprobacion"],
            self.ES_OBLIGATORIO: datos_materia["estado"] in [ESTADO_MATERIA[FINAL_PENDIENTE], ESTADO_MATERIA[APROBADA],
                                                             ESTADO_MATERIA[DESAPROBADA]],
            self.FUNCIONES_VALIDACION: [
                (self.es_numero_entero_valido_entre_min_y_max, [1, 2])
            ]
        })

    def datos_validacion_id_curso(self, datos_materia):
        return ("idCurso", {
            self.PARAMETRO: datos_materia["idCurso"] if (str(datos_materia["idCurso"]) != "-1") else None,
            self.ES_OBLIGATORIO: False,
            self.FUNCIONES_VALIDACION: [
                (self.id_es_valido, []),
                (self.existe_id, [Curso]),
                (self.el_curso_pertenece_a_la_materia_del_alumno, [datos_materia["idMateriaAlumno"]])
            ]
        })

    def datos_validacion_fecha_aprobacion(self, datos_materia):
        return ("fecha_aprobacion", {
            self.PARAMETRO: datos_materia["fecha_aprobacion"],
            self.ES_OBLIGATORIO: datos_materia["estado"] in [ESTADO_MATERIA[APROBADA], ESTADO_MATERIA[DESAPROBADA]],
            self.FUNCIONES_VALIDACION: [
                (self.fecha_aprobacion_es_valida, [])
            ]
        })

    def datos_validacion_anio_aprobacion(self, datos_materia):
        return ("anio_aprobacion", {
            self.PARAMETRO: datos_materia["anio_aprobacion"],
            self.ES_OBLIGATORIO: datos_materia["estado"] in [ESTADO_MATERIA[FINAL_PENDIENTE],
                                                             ESTADO_MATERIA[APROBADA],
                                                             ESTADO_MATERIA[DESAPROBADA]],
            self.FUNCIONES_VALIDACION: [
                (self.es_numero_valido, []),
                (self.fecha_aprobacion_cursada_es_valida, [datos_materia["cuatrimestre_aprobacion"]]),
                (self.es_de_un_cuatrimestre_posterior_al_desprobado_anterior,
                 [datos_materia["cuatrimestre_aprobacion"], datos_materia["idMateriaAlumno"]]),
            ]
        })

    def datos_validacion_forma_aprobacion(self, datos_materia):
        return ("forma_aprobacion", {
            self.PARAMETRO: datos_materia["forma_aprobacion"],
            self.ES_OBLIGATORIO: datos_materia["estado"] in [ESTADO_MATERIA[APROBADA], ESTADO_MATERIA[DESAPROBADA]],
            self.FUNCIONES_VALIDACION: [
                (self.existe_el_elemento, [FormaAprobacionMateria, FormaAprobacionMateria.forma])
            ]
        })

    def datos_validacion_calificacion(self, datos_materia):
        return ("calificacion", {
            self.PARAMETRO: datos_materia["calificacion"],
            self.ES_OBLIGATORIO: datos_materia["estado"] in [ESTADO_MATERIA[APROBADA], ESTADO_MATERIA[DESAPROBADA]],
            self.FUNCIONES_VALIDACION: [
                (self.es_numero_entero_valido_entre_min_y_max, [2, 10]),
                (self.es_calificacion_valida_para_el_estado, [datos_materia["estado"]])
            ]
        })

    def datos_validacion_acta_o_resolucion(self, datos_materia):
        return ("acta_resolucion", {
            self.PARAMETRO: datos_materia["acta_resolucion"],
            self.ES_OBLIGATORIO: datos_materia["estado"] in [ESTADO_MATERIA[APROBADA], ESTADO_MATERIA[DESAPROBADA]],
            self.FUNCIONES_VALIDACION: [
                (self.validar_contenido_y_longitud_texto, [1, 35])
            ]
        })

    def obtener_parametros_materia(self):
        datos_materia = {}
        datos_materia["idMateriaAlumno"] = self.obtener_texto("idMateriaAlumno")
        datos_materia["idCurso"] = self.obtener_parametro("idCurso")
        datos_materia["estado"] = self.obtener_texto("estado")
        datos_materia["cuatrimestre_aprobacion"] = self.obtener_texto("cuatrimestre_aprobacion")
        datos_materia["anio_aprobacion"] = self.obtener_texto("anio_aprobacion")
        datos_materia["fecha_aprobacion"] = self.obtener_parametro("fecha_aprobacion")
        datos_materia["forma_aprobacion"] = self.obtener_texto("forma_aprobacion")
        datos_materia["calificacion"] = self.obtener_texto("calificacion")
        datos_materia["acta_resolucion"] = self.obtener_texto("acta_resolucion")
        return datos_materia

    def actualizar_materia_alumno(self, datos_materia):

        materia = MateriasAlumno.query.get(datos_materia["idMateriaAlumno"])

        materia.estado_id = EstadoMateria.query.filter_by(estado=datos_materia["estado"]).first().id

        if datos_materia["cuatrimestre_aprobacion"]:
            materia.cuatrimestre_aprobacion_cursada = datos_materia["cuatrimestre_aprobacion"]

        if datos_materia["anio_aprobacion"]:
            materia.anio_aprobacion_cursada = datos_materia["anio_aprobacion"]

        # Si es -1 significa que no hay un curso designado
        if (datos_materia["idCurso"] is not None and datos_materia["idCurso"] != "-1"):
            materia.curso_id = int(datos_materia["idCurso"])
            if datos_materia["estado"] in [ESTADO_MATERIA[FINAL_PENDIENTE], ESTADO_MATERIA[APROBADA],
                                           ESTADO_MATERIA[DESAPROBADA]]:
                self.crear_encuesta(materia)

        if datos_materia["fecha_aprobacion"]:
            anio, mes, dia = datos_materia["fecha_aprobacion"].split("-")
            materia.fecha_aprobacion = date(int(anio), int(mes), int(dia))

        if datos_materia["forma_aprobacion"]:
            id_forma = FormaAprobacionMateria.query.filter_by(forma=datos_materia["forma_aprobacion"]).first().id
            materia.forma_aprobacion_id = id_forma

        if datos_materia["calificacion"]:
            materia.calificacion = int(datos_materia["calificacion"])

        if datos_materia["acta_resolucion"]:
            materia.acta_o_resolucion = datos_materia["acta_resolucion"]

        if datos_materia["estado"] == ESTADO_MATERIA[DESAPROBADA]:
            # En caso de que la materia este desaprobada, se puede volver a cursar
            # por lo que se agrega esta materia como una nueva entrada pendiente
            self.agregar_materia_pendiente(materia)

        db.session.commit()

        self.actualizar_materias_incompatibles(materia)

    def actualizar_materias_incompatibles(self, materia):
        """
        Si la materia tiene materias incompatibles que se encuentren en un estado pendiente
        o en estado incompatible las actualiza.
        Si la materia actual esta desaprobada todas las incompatibles quedan como pendientes
        ya que pueden ser cursadas.
        Si la materia actual está en cualquier otro estado, marcar las materias correspondientes
        como incompatibles
        """
        incompatibles = MateriasIncompatibles.query.filter_by(materia_id=materia.materia_id).all()
        if not incompatibles:
            return

        estado_desaprobada = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[DESAPROBADA]).first().id
        estado_incompatible = EstadoMateria.query.filter_by(
            estado=ESTADO_MATERIA[ELIMINADA_POR_INCOMPATIBLE]).first().id
        estado_pendiente = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[PENDIENTE]).first().id

        for materia_incompatible in incompatibles:
            materias_alumno = MateriasAlumno.query.filter_by(materia_id=materia_incompatible.materia_incompatible_id). \
                filter_by(alumno_id=materia.alumno_id).all()
            if not materias_alumno:
                continue

            for materia_alumno in materias_alumno:
                # Si la materia esta desaprobada, todas las materias que se supone son incompatibles y estan en
                # estado ELIMINADA_POR_INCOMPATIBLE quedan en estado PENDIENTE
                if materia.estado_id == estado_desaprobada:
                    if materia_alumno.estado_id == estado_incompatible:
                        materia_alumno.estado_id = estado_pendiente

                # Si se la cursa o aprueba, entonces todas las materias que se supone que son incompatibles y se
                # encuentran en estado pendiente, quedan como incompatibles
                elif materia_alumno.estado_id == estado_pendiente:
                    materia_alumno.estado_id = estado_incompatible

                db.session.commit()

    def actualizar_materias_incompatibles_al_eliminar_materia(self, materia):
        estado_desaprobada = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[DESAPROBADA]).first().id

        # Si la materia a eliminar estaba desaprobada entonces no se modifican las otras materias
        if materia.estado_id == estado_desaprobada:
            return

        incompatibles = MateriasIncompatibles.query.filter_by(materia_id=materia.materia_id).all()
        if not incompatibles:
            return

        alumno = self.obtener_alumno_usuario_actual()

        estado_incompatible = EstadoMateria.query.filter_by(
            estado=ESTADO_MATERIA[ELIMINADA_POR_INCOMPATIBLE]).first().id
        estado_pendiente = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[PENDIENTE]).first().id

        for materia_incompatible in incompatibles:
            materias_alumno = MateriasAlumno.query.filter_by(materia_id=materia_incompatible.materia_incompatible_id). \
                filter_by(alumno_id=alumno.id).filter_by(estado_id=estado_incompatible).all()
            if not materias_alumno:
                continue

            for materia_alumno in materias_alumno:
                materia_alumno.estado_id = estado_pendiente
                db.session.commit()

    def es_calificacion_valida_para_el_estado(self, nombre_parametro, valor, obligatorio, estado):
        if not valor and not obligatorio:
            return self.mensaje_campo_no_obligatorio(nombre_parametro)

        calificacion = int(str(valor))
        if estado == "Desaprobado" and calificacion >= 4:
            return False, 'La calificación debe ser menor que 4', CLIENT_ERROR_BAD_REQUEST

        if estado == "Aprobado" and calificacion < 4:
            return False, 'La calificación debe ser mayor o igual que 4', CLIENT_ERROR_BAD_REQUEST

        return self.mensaje_OK(nombre_parametro)

    def materia_tiene_estado_pendiente(self, nombre_parametro, valor, obligatorio):
        estado_pendiente = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[PENDIENTE]).first()
        materia = MateriasAlumno.query.get(valor)
        return self.mensaje_OK(nombre_parametro) if materia.estado_id == estado_pendiente.id else \
            (False, 'La materia no está en estado pendiente por lo tanto no puede ser añadida', CLIENT_ERROR_NOT_FOUND)

    def materia_permite_ser_modificada(self, nombre_parametro, valor, obligatorio):
        estado_pendiente = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[PENDIENTE]).first()
        estado_aprobada = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[APROBADA]).first()
        estado_desaprobada = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[DESAPROBADA]).first()

        materia = MateriasAlumno.query.get(valor)

        es_valida = materia.estado_id not in [estado_pendiente.id, estado_aprobada.id, estado_desaprobada.id]

        return self.mensaje_OK(nombre_parametro) if es_valida else \
            (False, 'La materia no puede ser modificada en el estado actual.', CLIENT_ERROR_NOT_FOUND)

    def nuevo_estado_materia_es_valido(self, nombre_parametro, valor, obligatorio, idMateriaAlumno):
        estado_actual = EstadoMateria.query.get(MateriasAlumno.query.get(idMateriaAlumno).estado_id).estado

        es_valido = False

        if estado_actual == ESTADO_MATERIA[EN_CURSO]:
            es_valido = (valor in [ESTADO_MATERIA[EN_CURSO], ESTADO_MATERIA[FINAL_PENDIENTE], ESTADO_MATERIA[APROBADA],
                                   ESTADO_MATERIA[DESAPROBADA]])

        if estado_actual == ESTADO_MATERIA[FINAL_PENDIENTE]:
            es_valido = (valor in [ESTADO_MATERIA[FINAL_PENDIENTE], ESTADO_MATERIA[APROBADA],
                                   ESTADO_MATERIA[DESAPROBADA]])

        return self.mensaje_OK(nombre_parametro) if es_valido else \
            (False, 'El estado {} nuevo no es valido'.format(valor), CLIENT_ERROR_BAD_REQUEST)

    def es_estado_materia_valido(self, nombre_parametro, valor, obligatorio):
        es_valido = (valor in [ESTADO_MATERIA[EN_CURSO],
                               ESTADO_MATERIA[FINAL_PENDIENTE],
                               ESTADO_MATERIA[APROBADA],
                               ESTADO_MATERIA[DESAPROBADA]])
        return self.mensaje_OK(nombre_parametro) if es_valido else \
            (False, 'El estado {} no es valido'.format(valor), CLIENT_ERROR_BAD_REQUEST)

    def fecha_aprobacion_es_valida(self, nombre_parametro, valor, obligatorio):
        if not valor and not obligatorio:
            return self.mensaje_campo_no_obligatorio(nombre_parametro)

        try:
            anio, mes, dia = valor.split("-")
            date(int(anio), int(mes), int(dia))
            return self.mensaje_OK(nombre_parametro)
        except Exception as e:
            return False, 'La fecha {} no es válida'.format(valor), CLIENT_ERROR_BAD_REQUEST

    def el_curso_pertenece_a_la_materia_del_alumno(self, nombre_parametro, valor, obligatorio, idMateriaAlumno):
        if not valor and not obligatorio:
            return self.mensaje_campo_no_obligatorio(nombre_parametro)

        try:
            cod_materia = Materia.query.get(MateriasAlumno.query.get(idMateriaAlumno).materia_id).codigo
            curso = Curso.query.get(valor)
            es_valido = (curso.codigo_materia == cod_materia)
            return self.mensaje_OK(nombre_parametro) if es_valido else \
                (False, 'El curso {} no es un curso de la materia elegida'.format(valor), CLIENT_ERROR_NOT_FOUND)
        except:
            return False, 'No se encuentra el curso correspondiente', CLIENT_ERROR_NOT_FOUND

    def fecha_aprobacion_cursada_es_valida(self, nombre_parametro, anio, obligatorio, cuatrimestre):
        if not obligatorio and not anio:
            return self.mensaje_campo_no_obligatorio(nombre_parametro)

        MAX_TIEMPO = 20
        hoy = datetime.now().year
        anios = [str(x) for x in range(hoy, hoy - MAX_TIEMPO, -1)]
        return self.mensaje_OK(nombre_parametro) if anio in anios else \
            (False, 'El anio no es valido', CLIENT_ERROR_BAD_REQUEST)

    def es_de_un_cuatrimestre_posterior_al_desprobado_anterior(self, nombre_parametro, anio, obligatorio, cuatrimestre,
                                                               idMateriaAlumno):
        if not obligatorio and not anio:
            return self.mensaje_campo_no_obligatorio(nombre_parametro)

        idMateria = MateriasAlumno.query.get(idMateriaAlumno).materia_id

        alumno = self.obtener_alumno_usuario_actual()

        ultima_materia = MateriasAlumno.query.filter(MateriasAlumno.id != idMateriaAlumno)\
            .filter_by(alumno_id=alumno.id).filter_by(materia_id=idMateria)\
            .order_by(MateriasAlumno.anio_aprobacion_cursada.desc())\
            .order_by(MateriasAlumno.cuatrimestre_aprobacion_cursada.desc()).first()

        if not ultima_materia:
            return self.mensaje_OK(nombre_parametro)

        es_valido = (ultima_materia.anio_aprobacion_cursada < anio or
                     ultima_materia.cuatrimestre_aprobacion_cursada < cuatrimestre)

        return (False, 'La nueva cursada de esta materia debe ser de un '
                       'cuatrimestre posterior a la misma materia que quedó desaprobada', CLIENT_ERROR_BAD_REQUEST) if \
            not es_valido else self.mensaje_OK(nombre_parametro)

    def eliminar_correspondientes_desaprobadas(self, materia):
        se_elimino_materia_actual = False

        estado_pendiente = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[PENDIENTE]).first()

        query = MateriasAlumno.query.filter_by(alumno_id=materia.alumno_id)
        query = query.filter_by(materia_id=materia.materia_id)
        otras_materias = query.filter(MateriasAlumno.id != materia.id).all()

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

    def agregar_materia_pendiente(self, materia):
        estado_pendiente = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[PENDIENTE]).first()

        db.session.add(MateriasAlumno(
            alumno_id=materia.alumno_id,
            materia_id=materia.materia_id,
            estado_id=estado_pendiente.id,
            carrera_id=materia.carrera_id
        ))
        db.session.commit()

    def crear_encuesta(self, materia_alumno):
        encuesta = EncuestaAlumno.query.filter_by(materia_alumno_id=materia_alumno.id).first()
        if encuesta:  # Las encuestas no tiene datos que puedan ser actualizados
            return

        encuesta = EncuestaAlumno(
            alumno_id=materia_alumno.alumno_id,
            materia_alumno_id=materia_alumno.id,
            cuatrimestre_aprobacion_cursada=materia_alumno.cuatrimestre_aprobacion_cursada,
            anio_aprobacion_cursada=materia_alumno.anio_aprobacion_cursada,
            finalizada=False
        )
        db.session.add(encuesta)
        db.session.commit()

        estado_pasos = EstadoPasosEncuestaAlumno(encuesta_alumno_id=encuesta.id)
        estado_pasos.inicializar_pasos()
        db.session.add(estado_pasos)
        db.session.commit()

        curso = Curso.query.get(materia_alumno.curso_id)
        docentes = ""
        for cdoc in CursosDocente.query.filter_by(curso_id=materia_alumno.curso_id).all():
            docente = Docente.query.get(cdoc.docente_id)
            docentes += docente.obtener_nombre_completo() + "-"
        encuesta.curso = "{}: {}".format(curso.codigo, docentes[:-1])

        encuesta.cuatrimestre_aprobacion_cursada = materia_alumno.cuatrimestre_aprobacion_cursada
        encuesta.anio_aprobacion_cursada = materia_alumno.anio_aprobacion_cursada
        encuesta.finalizada = False
        db.session.commit()


#########################################
CLASE = MateriaAlumnoService
URLS_SERVICIOS = (
    '/api/alumno/materia/<int:idMateriaAlumno>',
    '/api/alumno/materia',
)
#########################################
