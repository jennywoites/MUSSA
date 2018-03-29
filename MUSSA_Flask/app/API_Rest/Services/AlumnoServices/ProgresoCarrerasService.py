from app.API_Rest.codes import *
from flask_user import login_required
from app.API_Rest.Services.BaseService import BaseService
from app.models.alumno_models import AlumnosCarreras
from app.models.carreras_models import Orientacion, Creditos, Materia, TipoMateria
from app.DAO.MateriasDAO import APROBADA
from app.API_Rest.Services.AlumnoServices.AllMateriasAlumnoService import AllMateriasAlumnoService


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

            for orientacion in self.obtener_orientaciones(carrera_id):
                separacion_por_trabajos = self.generar_separacion_por_trabajo_final(creditos)
                progreso_result[carrera_id][orientacion] = separacion_por_trabajos

                for trabajo in separacion_por_trabajos:
                    datos_creditos = self.inicializar_creditos_requeridos(creditos)

                    if trabajo == "TESIS":
                        datos_creditos["creditos_requeridos_electivas"] = creditos.creditos_electivas_con_tesis
                        datos_creditos["creditos_requeridos_trabajo_final"] = creditos.creditos_tesis
                    elif trabajo == "TP_PROFESIONAL":
                        datos_creditos["creditos_requeridos_electivas"] = creditos.creditos_electivas_con_tp
                        datos_creditos["creditos_requeridos_trabajo_final"] = creditos.creditos_tp_profesional
                    else:
                        datos_creditos["creditos_requeridos_electivas"] = creditos.creditos_electivas_general
                        datos_creditos["creditos_requeridos_trabajo_final"] = 0

                    promedio = self.actualizar_creditos_materias_aprobadas(carrera_id, orientacion, trabajo, datos_creditos)
                    datos_creditos["promedio"] = promedio

                    self.guardar_porcentajes_aprobacion(datos_creditos)
                    self.guardar_avance_total(datos_creditos)

                    progreso_result[carrera_id][orientacion][trabajo] = datos_creditos

        result = ({'progreso': progreso_result}, SUCCESS_OK)
        self.logg_resultado(result)

        return result

    def inicializar_creditos_requeridos(self, creditos):
        datos_creditos = {}

        datos_creditos["cantidad_materias_CBC_requeridas"] = 6
        datos_creditos["cantidad_materias_CBC_aprobadas"] = 0

        datos_creditos["creditos_requeridos_obligatorias"] = creditos.creditos_obligatorias
        datos_creditos["creditos_obtenidos_obligatorias"] = 0

        datos_creditos["creditos_requeridos_electivas"] = 0
        datos_creditos["creditos_obtenidos_electivas"] = 0

        datos_creditos["creditos_requeridos_orientacion"] = creditos.creditos_orientacion
        datos_creditos["creditos_obtenidos_orientacion"] = 0

        datos_creditos["creditos_requeridos_trabajo_final"] = 0
        datos_creditos["creditos_obtenidos_trabajo_final"] = 0

        return datos_creditos

    def guardar_porcentajes_aprobacion(self, datos_creditos):

        requerido = datos_creditos["cantidad_materias_CBC_requeridas"]
        obtenido = datos_creditos["cantidad_materias_CBC_aprobadas"]
        self.calcular_porcentaje(datos_creditos, "porcentaje_CBC", requerido, obtenido)

        requerido = datos_creditos["creditos_requeridos_obligatorias"]
        obtenido = datos_creditos["creditos_obtenidos_obligatorias"]
        self.calcular_porcentaje(datos_creditos, "porcentaje_obligatorias", requerido, obtenido)

        requerido = datos_creditos["creditos_requeridos_electivas"]
        obtenido = datos_creditos["creditos_obtenidos_electivas"]
        self.calcular_porcentaje(datos_creditos, "porcentaje_electivas", requerido, obtenido)

        requerido = datos_creditos["creditos_requeridos_orientacion"]
        obtenido = datos_creditos["creditos_obtenidos_orientacion"]
        self.calcular_porcentaje(datos_creditos, "porcentaje_orientacion", requerido, obtenido)

        requerido = datos_creditos["creditos_requeridos_trabajo_final"]
        obtenido = datos_creditos["creditos_obtenidos_trabajo_final"]
        self.calcular_porcentaje(datos_creditos, "porcentaje_trabajo_final", requerido, obtenido)

    def calcular_porcentaje(self, datos_creditos, campo, requerido, obtenido):
        datos_creditos[campo] = int((obtenido / requerido) * 100) if requerido > 0 else 0
        if datos_creditos[campo] > 100:
            datos_creditos[campo] = 100

    def guardar_avance_total(self, datos_creditos):
        requerido = datos_creditos["cantidad_materias_CBC_requeridas"]
        requerido += datos_creditos["creditos_requeridos_obligatorias"]
        requerido += datos_creditos["creditos_requeridos_electivas"]
        requerido += datos_creditos["creditos_requeridos_orientacion"]
        requerido += datos_creditos["creditos_requeridos_trabajo_final"]

        obtenido = datos_creditos["cantidad_materias_CBC_aprobadas"]
        obtenido += datos_creditos["creditos_obtenidos_obligatorias"]
        obtenido += datos_creditos["creditos_obtenidos_electivas"] if \
            (datos_creditos["creditos_obtenidos_electivas"] <= datos_creditos["creditos_requeridos_electivas"]) \
            else datos_creditos["creditos_requeridos_electivas"]
        obtenido += datos_creditos["creditos_obtenidos_orientacion"]
        obtenido += datos_creditos["creditos_obtenidos_trabajo_final"]

        self.calcular_porcentaje(datos_creditos, "porcentaje_avance_total", requerido, obtenido)

    def actualizar_creditos_materias_aprobadas(self, carrera_id, orientacion, trabajo, datos_creditos):
        servicio = AllMateriasAlumnoService()
        materias = servicio.obtener_materias_alumno_por_categorias([APROBADA], [], carrera_id)[0]["materias_alumno"]

        total_suma_notas = 0
        for materia_alumno in materias:
            total_suma_notas += int(str(materia_alumno["calificacion"]))
            materia = Materia.query.get(materia_alumno["id_materia"])
            tipo_materia = TipoMateria.query.get(materia.tipo_materia_id)

            if tipo_materia.descripcion == "CBC":
                datos_creditos["cantidad_materias_CBC_aprobadas"] += 1

            elif tipo_materia.descripcion == "OBLIGATORIA":
                datos_creditos["creditos_obtenidos_obligatorias"] += materia.creditos

            elif tipo_materia.descripcion == orientacion:
                datos_creditos["creditos_obtenidos_orientacion"] += materia.creditos

            elif tipo_materia.descripcion == "TP_PROFESIONAL":
                if trabajo == "TP_PROFESIONAL":
                    datos_creditos["creditos_obtenidos_trabajo_final"] += materia.creditos

            elif tipo_materia.descripcion == "TESIS":
                if trabajo == "TESIS":
                    datos_creditos["creditos_obtenidos_trabajo_final"] += materia.creditos

            # Electivas y orientacion no elegida (la obligatoria de orientacion es electiva para las demas orientaciones)
            else:
                datos_creditos["creditos_obtenidos_electivas"] += materia.creditos

        return "{0:.2f}".format(total_suma_notas / len(materias) if len(materias) > 0 else 0)

    def obtener_orientaciones(self, carrera_id):
        orientaciones = Orientacion.query.filter_by(carrera_id=carrera_id).all()

        ids_orientaciones = []
        for orientacion in orientaciones:
            ids_orientaciones.append(orientacion.clave_reducida)

        if not orientaciones:
            ids_orientaciones.append('GRAL')

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
