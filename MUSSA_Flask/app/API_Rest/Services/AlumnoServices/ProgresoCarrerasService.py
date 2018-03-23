from app.API_Rest.codes import *
from flask_user import login_required
from app.API_Rest.Services.BaseService import BaseService
from app.models.alumno_models import AlumnosCarreras


class ProgresoCarrerasService(BaseService):
    def getNombreClaseServicio(self):
        return "Progreso Carrera Service"

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

        progreso_result = {}
        for carrera_alumno in AlumnosCarreras.query.filter_by(alumno_id=alumno.id).all():
            carrera_id = carrera_alumno.carrera_id
            progreso_result[carrera_id] = {}
            creditos = Creditos.query.filter_by(carrera_id=carrera_id).first()

            for id_orientacion in self.obtener_ids_orientaciones(carrera_id):
                separacion_por_trabajos = self.generar_separacion_por_trabajo_final(creditos)
                progreso_result[carrera_id][id_orientacion] = separacion_por_trabajos

                separacion_por_trabajos["creditos_requeridos_obligatorias"] = creditos.creditos_obligatorias
                separacion_por_trabajos["creditos_obtenidos_obligatorias"] = 0
                separacion_por_trabajos["porcentaje_obligatorias"] = 0

                separacion_por_trabajos["creditos_requeridos_electivas"] = 0
                separacion_por_trabajos["creditos_obtenidos_electivas"] = 0
                separacion_por_trabajos["porcentaje_electivas"] = 0

                separacion_por_trabajos["creditos_requeridos_orientacion"] = creditos.creditos_orientacion
                separacion_por_trabajos["creditos_obtenidos_orientacion"] = 0
                separacion_por_trabajos["porcentaje_orientacion"] = 0

                separacion_por_trabajos["creditos_requeridos_trabajo_final"] = 0
                separacion_por_trabajos["creditos_obtenidos_trabajo_final"] = 0
                separacion_por_trabajos["porcentaje_trabajo_final"] = 0

        return {
            "electivas_general": creditos.creditos_electivas_general,
            "electivas_con_tp": creditos.creditos_electivas_con_tp,
            "electivas_con_tesis": creditos.creditos_electivas_con_tesis,
            "tesis": creditos.creditos_tesis,
            "tp_profesional": creditos.creditos_tp_profesional
        }

        result = ({'progreso': progreso_result}, SUCCESS_OK)
        self.logg_resultado(result)

        return result

    def obtener_ids_orientaciones(self, carrera_id):
        orientaciones = Orientacion.query.filter_by(carrera_id=carrera_id).all()

        ids_orientaciones = []
        for orientacion in orientaciones:
            ids_orientaciones.append(orientacion.id)

        if not orientaciones:
            ids_orientaciones.append(-1)

        return ids_orientaciones

    def generar_separacion_por_trabajo_final(self, creditos):
        trabajos = {}

        if creditos.creditos_tesis > 0:
            trabajos["TESIS"] = {}

        if creditos.creditos_tesis > 0:
            trabajos["TP_PROFESIONAL"] = {}

        if not trabajos:
            trabajos["GRAL"] = {}

        return trabajos


#########################################
CLASE = ProgresoCarrerasService
URLS_SERVICIOS = (
    '/api/alumno/progreso',
)
#########################################
