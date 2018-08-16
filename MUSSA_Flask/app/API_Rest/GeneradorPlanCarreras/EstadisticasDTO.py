import fcntl
import os
import csv


class EstadisticasDTO:
    def __init__(self):
        self.cantidad_cuatrimestres_plan = 0  # Cuentan los del CBC
        self.estado_plan = -1

        # Tiempos
        self.fecha_solicitado = ""
        self.fecha_inicio_generacion = ""
        self.fecha_fin_generacion = ""
        self.segundos_total_generacion = 0
        self.tiempo_total_generacion = ""
        self.fecha_inicio_guardado = ""
        self.fecha_fin_guardado = ""
        self.tiempo_total_guardado = ""

        # Materias a utilizar
        self.cantidad_materias_disponibles_totales = 0
        self.cantidad_cursos_disponibles_totales = 0
        self.cantidad_materias_CBC = 0

        # Configuracion
        self.cantidad_materias_por_cuatrimestre_max = 0
        self.cantidad_horas_cursada_max = 0
        self.cantidad_horas_extras_max = 0
        self.orientacion = ""
        self.carrera = ""
        self.trabajo_final = ""
        self.tipo_solicitud = "Normal"

    def guardar_en_archivo(self):
        RUTA = "estadisticas_algoritmos.csv"
        if not os.path.isfile(RUTA):
            self._guardar_en_archivo('w', RUTA, self._guardar_estadisticas_y_titulo)
        else:
            self._guardar_en_archivo('a', RUTA, self._guardar_estadisticas)

    def _guardar_en_archivo(self, modo, ruta, f_escritura):
        try:
            handle = open(ruta, modo)

            # Solicita el Lock del archivo
            fcntl.flock(handle, fcntl.LOCK_EX)

            writer = csv.writer(handle)
            f_escritura(writer)

            # Libera el Lock del archivo
            fcntl.flock(handle, fcntl.LOCK_UN)
            handle.close()
        except:
            handle.close()

    def _guardar_estadisticas_y_titulo(self, writer):
        writer.writerow(self.get_titulos_CSV())
        writer.writerow(self.get_linea_CSV())

    def _guardar_estadisticas(self, writer):
        writer.writerow(self.get_linea_CSV())

    def get_titulos_CSV(self):
        return [
            "Total cuatrimestres plan",
            "Estado del plan",
            "Fecha solicitud",
            "Fecha inicio de generación del plan",
            "Fecha finalización de generación del plan",
            "Segundos tiempo de generación",
            "Total tiempo de generación",
            "Fecha inicio de guardado del plan",
            "Fecha finalización de guardado del plan",
            "Total tiempo de guardado",
            "Total Materias disponibles",
            "Total Cursos disponibles",
            "Total Materias CBC",
            "Max cantidad materias por cuatrimestre",
            "Max cantidad horas de cursada",
            "Max cantidad horas extra",
            "Orientacion",
            "Carrera",
            "Trabajo Final",
            "Tipo de Solicitud"
        ]

    def get_linea_CSV(self):
        return [
            self.cantidad_cuatrimestres_plan,
            self.estado_plan,

            # Tiempos
            self.fecha_solicitado,
            self.fecha_inicio_generacion,
            self.fecha_fin_generacion,
            self.segundos_total_generacion,
            self.tiempo_total_generacion,
            self.fecha_inicio_guardado,
            self.fecha_fin_guardado,
            self.tiempo_total_guardado,

            # Materias a utilizar
            self.cantidad_materias_disponibles_totales,
            self.cantidad_cursos_disponibles_totales,
            self.cantidad_materias_CBC,

            # Configuracion
            self.cantidad_materias_por_cuatrimestre_max,
            self.cantidad_horas_cursada_max,
            self.cantidad_horas_extras_max,
            self.orientacion,
            self.carrera,
            self.trabajo_final,
            self.tipo_solicitud
        ]

    def get_JSON(self):
        return {
            "cantidad_cuatrimestres_plan": self.cantidad_cuatrimestres_plan,
            "estado_plan": self.estado_plan,

            "fecha_solicitado": self.fecha_solicitado,
            "fecha_inicio_generacion": self.fecha_inicio_generacion,
            "fecha_fin_generacion": self.fecha_fin_generacion,
            "segundos_total_generacion": self.segundos_total_generacion,
            "tiempo_total_generacion": self.tiempo_total_generacion,
            "fecha_inicio_guardado": self.fecha_inicio_guardado,
            "fecha_fin_guardado": self.fecha_fin_guardado,
            "tiempo_total_guardado": self.tiempo_total_guardado,

            "cantidad_materias_disponibles_totales": self.cantidad_materias_disponibles_totales,
            "cantidad_cursos_disponibles_totales": self.cantidad_cursos_disponibles_totales,
            "cantidad_materias_CBC": self.cantidad_materias_CBC,

            "cantidad_materias_por_cuatrimestre_max": self.cantidad_materias_por_cuatrimestre_max,
            "cantidad_horas_cursada_max": self.cantidad_horas_cursada_max,
            "cantidad_horas_extras_max": self.cantidad_horas_extras_max,
            "orientacion": self.orientacion,
            "carrera": self.carrera,
            "trabajo_final": self.trabajo_final,
            "tipo_solicitud": self.tipo_solicitud
        }

    def cargar_desde_JSON(self, datosJSON):
        self.cantidad_cuatrimestres_plan = datosJSON["cantidad_cuatrimestres_plan"]
        self.estado_plan = datosJSON["estado_plan"]

        # Tiempos
        self.fecha_solicitado = datosJSON["fecha_solicitado"]
        self.fecha_inicio_generacion = datosJSON["fecha_inicio_generacion"]
        self.fecha_fin_generacion = datosJSON["fecha_fin_generacion"]
        self.segundos_total_generacion = datosJSON["segundos_total_generacion"]
        self.tiempo_total_generacion = datosJSON["tiempo_total_generacion"]
        self.fecha_inicio_guardado = datosJSON["fecha_inicio_guardado"]
        self.fecha_fin_guardado = datosJSON["fecha_fin_guardado"]
        self.tiempo_total_guardado = datosJSON["tiempo_total_guardado"]

        # Materias a utilizar
        self.cantidad_materias_disponibles_totales = datosJSON["cantidad_materias_disponibles_totales"]
        self.cantidad_cursos_disponibles_totales = datosJSON["cantidad_cursos_disponibles_totales"]
        self.cantidad_materias_CBC = datosJSON["cantidad_materias_CBC"]

        # Configuracion
        self.cantidad_materias_por_cuatrimestre_max = datosJSON["cantidad_materias_por_cuatrimestre_max"]
        self.cantidad_horas_cursada_max = datosJSON["cantidad_horas_cursada_max"]
        self.cantidad_horas_extras_max = datosJSON["cantidad_horas_extras_max"]
        self.orientacion = datosJSON["orientacion"]
        self.carrera = datosJSON["carrera"]
        self.trabajo_final = datosJSON["trabajo_final"]
        self.tipo_solicitud = datosJSON["tipo_solicitud"]
