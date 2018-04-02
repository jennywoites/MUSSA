from app.API_Rest.Services.BaseService import BaseService
from app.models.horarios_models import Curso
from app.models.respuestas_encuesta_models import EncuestaAlumno, RespuestaEncuestaAlumno
from app.models.alumno_models import MateriasAlumno
from app.API_Rest.codes import *
from app.DAO.EncuestasDAO import *
from app.models.generadorJSON.resultados_encuestas_generadorJSON import generar_estructura_respuesta_por_tipo, \
    actualizar_respuesta_JSON, ajustar_franjas_respuestas_horarios


class ResultadosEncuestaCursoService(BaseService):
    def getNombreClaseServicio(self):
        return "Resultados Encuesta Curso Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    def get(self, idCurso):
        self.logg_parametros_recibidos()

        cuatrimestre = self.obtener_parametro("cuatrimestre")
        anio = self.obtener_parametro("anio")
        ids_preguntas = self.obtener_lista("ids_preguntas")

        if (cuatrimestre and not anio) or (not cuatrimestre and anio):
            msj = "El grupo cuatrimestre/año no está completo"
            self.logg_error(msj)
            return {'Error': msj}, CLIENT_ERROR_BAD_REQUEST

        parametros_son_validos, msj, codigo = self.validar_parametros(dict([
            self.get_validaciones_entidad_basica("idCurso", idCurso, Curso, True),
            ("cuatrimestre", {
                self.PARAMETRO: cuatrimestre,
                self.ES_OBLIGATORIO: False,
                self.FUNCIONES_VALIDACION: [
                    (self.es_numero_valido, []),
                    (self.es_numero_entero_valido_entre_min_y_max, [1, 2]),
                ]
            }),
            ("anio", {
                self.PARAMETRO: anio,
                self.ES_OBLIGATORIO: False,
                self.FUNCIONES_VALIDACION: [
                    (self.es_numero_valido, [])
                ]
            }),
            self.get_validaciones_entidad_basica("ids_preguntas", ids_preguntas, PreguntaEncuesta, True)
        ]))

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': msj}, codigo

        query_materias_del_curso = MateriasAlumno.query.with_entities(MateriasAlumno.id).filter_by(curso_id=idCurso)

        query_encuestas = EncuestaAlumno.query.with_entities(EncuestaAlumno.id). \
            filter_by(finalizada=True).filter(EncuestaAlumno.materia_alumno_id.in_(query_materias_del_curso))

        if cuatrimestre and anio:
            query_encuestas = query_encuestas.filter_by(cuatrimestre_aprobacion_cursada=cuatrimestre) \
                .filter_by(anio_aprobacion_cursada=anio)

        respuestas_encuesta = RespuestaEncuestaAlumno.query \
            .filter(RespuestaEncuestaAlumno.encuesta_alumno_id.in_(query_encuestas)) \
            .filter(RespuestaEncuestaAlumno.pregunta_encuesta_id.in_(ids_preguntas)).all()

        respuestas_JSON = {}
        for rta_encuesta in respuestas_encuesta:
            id_pregunta_resultados = PreguntaResultadoEncuesta.query \
                .filter_by(pregunta_encuesta_id=rta_encuesta.pregunta_encuesta_id).first().id
            if not id_pregunta_resultados in respuestas_JSON:
                respuestas_JSON[id_pregunta_resultados] = generar_estructura_respuesta_por_tipo(rta_encuesta.tipo_id)
            actualizar_respuesta_JSON(rta_encuesta, respuestas_JSON[id_pregunta_resultados], rta_encuesta.tipo_id)

        for id_pregunta in respuestas_JSON:
            ajustar_franjas_respuestas_horarios(respuestas_JSON[id_pregunta])

        result = ({"respuestas_encuestas": respuestas_JSON}, SUCCESS_OK)
        self.logg_resultado(result)

        return result


#########################################
CLASE = ResultadosEncuestaCursoService
URLS_SERVICIOS = (
    '/api/encuesta/resultados/curso/<int:idCurso>',
)
#########################################
