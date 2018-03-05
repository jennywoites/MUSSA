from app.API_Rest.codes import *
from flask_user import login_required
from app.API_Rest.Services.BaseService import BaseService
from app.models.alumno_models import MateriasAlumno
from app.models.carreras_models import Correlativas, Materia
from app.DAO.MateriasDAO import *
from app.models.generadorJSON.carreras_generadorJSON import generarJSON_materia


class MateriasHabilitadasService(BaseService):
    def getNombreClaseServicio(self):
        return "Materias Habilitadas Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    @login_required
    def get(self):
        alumno = self.obtener_alumno_usuario_actual()

        if not alumno:
            msj = "El usuario no tiene ningun alumno asociado"
            self.logg_error(msj)
            return {'Error': msj}, CLIENT_ERROR_NOT_FOUND

        estado_pendiente = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[PENDIENTE]).first()
        estado_aprobado = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[APROBADA]).first()

        query = MateriasAlumno.query.filter_by(alumno_id=alumno.id)

        materias_pendientes = query.filter(MateriasAlumno.estado_id == estado_pendiente.id).all()

        ids_materias_aprobadas = query.with_entities(MateriasAlumno.materia_id) \
            .filter(MateriasAlumno.estado_id == estado_aprobado.id).all()

        creditos_actuales = 0
        for id_materia in ids_materias_aprobadas:
            creditos_actuales += Materia.query.get(id_materia).creditos

        materias_result = []
        for materia_alumno in materias_pendientes:
            correlativas_aprobadas = True
            for id_correlativa in Correlativas.query.with_entities(Correlativas.materia_correlativa_id). \
                    filter_by(materia_id=materia_alumno.materia_id).all():
                if id_correlativa not in ids_materias_aprobadas:
                    correlativas_aprobadas = False
                    break

            if not correlativas_aprobadas:
                continue

            materia = Materia.query.get(materia_alumno.materia_id)

            if materia.creditos_minimos_para_cursarla <= creditos_actuales:
                materias_result.append(generarJSON_materia(materia))

        MAX_LONGITUD_CODIGO = 4
        materias_result.sort(
            key=lambda materia_i: ((MAX_LONGITUD_CODIGO - len(materia_i["codigo"])) * "0" + materia_i["codigo"]),
            reverse=False
        )

        materias_por_carrera = {}
        for materia in materias_result:
            materias = materias_por_carrera.get(materia["carrera"], [])
            materias.append(materia)
            materias_por_carrera[materia["carrera"]] = materias

        result = ({'materias_por_carrera': materias_por_carrera}, SUCCESS_OK)
        self.logg_resultado(result)
        return result


#########################################
CLASE = MateriasHabilitadasService
URLS_SERVICIOS = (
    '/api/alumno/materia/habilitadas',
)
#########################################
