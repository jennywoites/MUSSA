from flask_user import login_required
from app.API_Rest.Services.BaseService import BaseService
from app.DAO.MateriasDAO import *
from app.API_Rest.Services.AlumnoServices.AllMateriasAlumnoService import AllMateriasAlumnoService


class MateriaPendienteService(BaseService):
    def getNombreClaseServicio(self):
        return "Materia Pendiente Service"

    ##########################################
    ##                Servicios             ##
    ##########################################

    @login_required
    def get(self):
        estados = [PENDIENTE]
        estados_invalidos = [EN_CURSO, FINAL_PENDIENTE, APROBADA, DESAPROBADA]
        servicio = AllMateriasAlumnoService()
        id_carrera = self.obtener_parametro("id_carrera")
        return servicio.obtener_materias_alumno_por_categorias(estados, estados_invalidos, id_carrera)


#########################################
CLASE = MateriaPendienteService
URLS_SERVICIOS = (
    '/api/alumno/materia/pendientes',
)
#########################################
