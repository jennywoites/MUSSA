from app.API_Rest.Services.BaseService import BaseService
from app.models.docentes_models import Docente
from app.API_Rest.codes import *
from app.models.respuestas_encuesta_models import EncuestaAlumno, RespuestaEncuestaDocente, RespuestaEncuestaAlumno


class CuatrimestresResultadosEncuestaDocenteService(BaseService):
    def getNombreClaseServicio(self):
        return "Cuatrimestres Resultados Encuesta Docente Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    def get(self, idDocente):
        self.logg_parametros_recibidos()

        parametros_son_validos, msj, codigo = self.validar_parametros(dict([
            self.get_validaciones_entidad_basica("idDocente", idDocente, Docente, True)
        ]))

        if not parametros_son_validos:
            self.logg_error(msj)
            return {'Error': msj}, codigo

        query_docentes = RespuestaEncuestaDocente.query \
            .with_entities(RespuestaEncuestaDocente.rta_encuesta_alumno_id) \
            .filter_by(docente_id=idDocente)

        query_ids_encuestas = RespuestaEncuestaAlumno.query \
            .with_entities(RespuestaEncuestaAlumno.encuesta_alumno_id) \
            .filter(RespuestaEncuestaAlumno.id.in_(query_docentes))

        datos = EncuestaAlumno.query \
            .with_entities(EncuestaAlumno.anio_aprobacion_cursada, EncuestaAlumno.cuatrimestre_aprobacion_cursada) \
            .filter_by(finalizada=True) \
            .filter(EncuestaAlumno.id.in_(query_ids_encuestas)) \
            .group_by(EncuestaAlumno.anio_aprobacion_cursada, EncuestaAlumno.cuatrimestre_aprobacion_cursada) \
            .order_by(EncuestaAlumno.anio_aprobacion_cursada.desc()) \
            .order_by(EncuestaAlumno.cuatrimestre_aprobacion_cursada.desc()).all()

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
CLASE = CuatrimestresResultadosEncuestaDocenteService
URLS_SERVICIOS = (
    '/api/encuesta/resultados/docente/<int:idDocente>/cuatrimestres',
)
#########################################
