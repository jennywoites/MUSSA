from app.API_Rest.Services.BaseService import BaseService
from flask_user import login_required
from app.API_Rest.codes import *
from app.models.plan_de_estudios_models import PlanDeEstudiosFinalizadoProcesar
from app.models.respuestas_encuesta_models import EncuestaAlumno


class NotificacionesService(BaseService):
    def getNombreClaseServicio(self):
        return "Notificaciones Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    @login_required
    def get(self):
        self.logg_parametros_recibidos()

        alumno = self.obtener_alumno_usuario_actual()

        notificaciones = {}

        encuestas_pendientes = self.obtener_cant_notificaciones_encuestas_pendientes(alumno)
        if encuestas_pendientes:
            notificaciones["encuestas"] = encuestas_pendientes

        planes_sin_visualizar = self.obtener_cant_notificaciones_planes_sin_ver(alumno)
        if planes_sin_visualizar:
            notificaciones["planes_de_estudio"] = planes_sin_visualizar

        result = ({"notificaciones": notificaciones}, SUCCESS_OK)
        self.logg_resultado(result)
        return result

    def obtener_cant_notificaciones_encuestas_pendientes(self, alumno):
        encuestas = EncuestaAlumno.query.with_entities(EncuestaAlumno.id) \
            .filter_by(alumno_id=alumno.id).filter_by(finalizada=False).all()
        return len(encuestas)

    def obtener_cant_notificaciones_planes_sin_ver(self, alumno):
        planes_sin_procesar = PlanDeEstudiosFinalizadoProcesar.query \
            .with_entities(PlanDeEstudiosFinalizadoProcesar.id).filter_by(alumno_id=alumno.id).all()
        return len(planes_sin_procesar)


#########################################
CLASE = NotificacionesService
URLS_SERVICIOS = (
    '/api/notificaciones',
)
#########################################
