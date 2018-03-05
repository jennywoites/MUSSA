from app.API_Rest.Services.BaseService import BaseService
from app.models.horarios_models import Curso
from app.models.respuestas_encuesta_models import EncuestaAlumno, RespuestaEncuestaAlumno, RespuestaEncuestaDocente
from app.API_Rest.codes import *
from app.models.alumno_models import MateriasAlumno
from app.models.carreras_models import Carrera, Materia
from app.models.docentes_models import CursosDocente, Docente


class ResultadosEncuestaDocenteService(BaseService):
    def getNombreClaseServicio(self):
        return "Resultados Encuesta Docente Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    def get(self, idDocente):
        self.logg_parametros_recibidos()

        cuatrimestre = self.obtener_parametro("cuatrimestre")
        anio = self.obtener_parametro("anio")

        if (cuatrimestre and not anio) or (not cuatrimestre and anio):
            msj = "El grupo cuatrimestre/año no está completo"
            self.logg_error(msj)
            return {'Error': msj}, CLIENT_ERROR_BAD_REQUEST

        parametros_son_validos, msj, codigo = self.validar_parametros(dict([
            self.get_validaciones_entidad_basica("idDocente", idDocente, Docente, True),
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
            })
        ]))

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': msj}, codigo

        query_encuestas = EncuestaAlumno.query.with_entities(EncuestaAlumno.id).filter_by(finalizada=True)

        if cuatrimestre:
            query_encuestas = query_encuestas.filter_by(cuatrimestre_aprobacion_cursada=cuatrimestre)

        if anio:
            query_encuestas = query_encuestas.filter_by(anio_aprobacion_cursada=anio)

        query_ids_respuestas = RespuestaEncuestaAlumno.query \
            .with_entities(RespuestaEncuestaAlumno.id) \
            .filter(RespuestaEncuestaAlumno.encuesta_alumno_id.in_(query_encuestas))

        respuestas_docentes = RespuestaEncuestaDocente.query \
            .filter(RespuestaEncuestaDocente.rta_encuesta_alumno_id.in_(query_ids_respuestas))\
            .filter_by(docente_id=idDocente).all()

        respuestas_JSON = {}
        cursos_del_docente = CursosDocente.query.filter_by(docente_id=idDocente).all()
        for c in cursos_del_docente:
            curso = Curso.query.get(c.curso_id)
            materia = Materia.query.filter_by(codigo=curso.codigo_materia).first()
            carrera = Carrera.query.get(materia.carrera_id)
            respuestas_JSON[curso.id] = {
                "codigo": materia.codigo,
                "nombre": materia.nombre,
                "id_carrera": materia.carrera_id,
                "carrera": carrera.get_descripcion_carrera(),
                "curso": curso.codigo,
                "id_curso": curso.id,
                "comentarios": []
            }

        for respuesta in respuestas_docentes:
            id_curso = MateriasAlumno.query \
                .get(EncuestaAlumno.query.get(
                RespuestaEncuestaAlumno.query.get(
                    respuesta.rta_encuesta_alumno_id).encuesta_alumno_id).materia_alumno_id).curso_id
            respuestas_JSON[id_curso]["comentarios"].append(respuesta.comentario)

        respuestas = []
        for id_curso in respuestas_JSON:
            respuestas.append(respuestas_JSON[id_curso])
        respuestas = sorted(respuestas, key=lambda datos: datos["codigo"] + "-" + datos["curso"])

        result = ({"respuestas_encuestas": respuestas}, SUCCESS_OK)
        self.logg_resultado(result)

        return result


#########################################
CLASE = ResultadosEncuestaDocenteService
URLS_SERVICIOS = (
    '/api/encuesta/resultados/docente/<int:idDocente>',
)
#########################################
