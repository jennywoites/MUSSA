from app.API_Rest.codes import *
from flask_user import login_required
from app.API_Rest.Services.BaseService import BaseService
from app.models.generadorJSON.plan_de_estudios_generadorJSON import generarJSON_plan_de_estudios
from app.models.plan_de_estudios_models import PlanDeEstudios, PlanDeEstudiosFinalizadoProcesar
from app import db


class AllPlanesDeEstudiosService(BaseService):
    def getNombreClaseServicio(self):
        return "All Planes de Estudio Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    @login_required
    def get(self):
        self.logg_parametros_recibidos()

        alumno = self.obtener_alumno_usuario_actual()

        if not alumno:
            msj = "El usuario no tiene ningun alumno asociado"
            self.logg_error(msj)
            return {'Error': msj}, CLIENT_ERROR_NOT_FOUND

        query = PlanDeEstudios.query.filter_by(alumno_id=alumno.id)
        query = query.order_by(PlanDeEstudios.fecha_generacion.desc())

        result_planes = []
        for encuesta in query.all():
            result_planes.append(generarJSON_plan_de_estudios(encuesta))

        self.actualizar_notificaciones_planes_visualizados(alumno)

        result = ({"planes_de_estudio": result_planes}, SUCCESS_OK)
        self.logg_resultado(result)

        return result

    def actualizar_notificaciones_planes_visualizados(self, alumno):
        """
        Elimina todas las notificaciones del planes sin visualizar para
        el alumno ya que se ha accedido a ver el listado de los planes.
        """
        PlanDeEstudiosFinalizadoProcesar.query.filter_by(alumno_id=alumno.id).delete()
        db.session.commit()


#########################################
CLASE = AllPlanesDeEstudiosService
URLS_SERVICIOS = (
    '/api/alumno/planDeEstudios/all',
)
#########################################
