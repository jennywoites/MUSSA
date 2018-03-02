from app.API_Rest.Services.BaseService import BaseService
from app.models.horarios_models import Curso
from app.API_Rest.codes import *
from app.models.respuestas_encuesta_models import EncuestaAlumno
from app.models.alumno_models import MateriasAlumno


class CuatrimestresResultadosEncuestaCursoService(BaseService):
    def getNombreClaseServicio(self):
        return "Cuatrimestres Resultados Encuesta Curso Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    def get(self, idCurso):
        self.logg_parametros_recibidos()

        parametros_son_validos, msj, codigo = self.validar_parametros(dict([
            self.get_validaciones_entidad_basica("idCurso", idCurso, Curso, True)
        ]))

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': msj}, codigo

        query_materias_del_curso = MateriasAlumno.query.with_entities(MateriasAlumno.id).filter_by(curso_id=idCurso)

        datos = EncuestaAlumno.query \
            .with_entities(EncuestaAlumno.anio_aprobacion_cursada, EncuestaAlumno.cuatrimestre_aprobacion_cursada) \
            .filter_by(finalizada=True) \
            .filter(EncuestaAlumno.materia_alumno_id.in_(query_materias_del_curso)) \
            .group_by(EncuestaAlumno.anio_aprobacion_cursada, EncuestaAlumno.cuatrimestre_aprobacion_cursada) \
            .order_by(EncuestaAlumno.anio_aprobacion_cursada.desc()) \
            .order_by(EncuestaAlumno.anio_aprobacion_cursada.desc()).all()

        resultados_json = []
        for anio, cuatrimestre in datos:
            resultados_json.append({
                "anio": anio,
                "cuatrimestre": cuatrimestre
            })

        result = ({"cuatrimestres": resultados_json}, SUCCESS_OK)
        self.logg_resultado(result)

        return result


#########################################
CLASE = CuatrimestresResultadosEncuestaCursoService
URLS_SERVICIOS = (
    '/api/encuesta/resultados/curso/<int:idCurso>/cuatrimestres',
)
#########################################
