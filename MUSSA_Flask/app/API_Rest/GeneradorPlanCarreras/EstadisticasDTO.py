class EstadisticasDTO:
    def __init__(self):
        self.cantidad_cuatrimestres_plan = 0  # Cuentan los del CBC
        self.estado_plan = -1

        # Tiempos
        self.fecha_solicitado = ""
        self.fecha_inicio_generacion = ""
        self.fecha_fin_generacion = ""
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
        self.algoritmo = -1
        self.tipo_solicitud = "Normal"

    def get_titulos_CSV(self):
        return [
            "Total cuatrimestres plan",
            "Estado del plan",
            "Fecha solicitud",
            "Fecha inicio de generación del plan",
            "Fecha finalización de generación del plan",
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
            "Algoritmo",
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
            self.algoritmo,
            self.tipo_solicitud
        ]

    def get_JSON(self):
        return {
            "cantidad_cuatrimestres_plan": self.cantidad_cuatrimestres_plan,
            "estado_plan": self.estado_plan,

            "fecha_solicitado": self.fecha_solicitado,
            "fecha_inicio_generacion": self.fecha_inicio_generacion,
            "fecha_fin_generacion": self.fecha_fin_generacion,
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
            "algoritmo": self.algoritmo,
            "tipo_solicitud": self.tipo_solicitud
        }

    def cargar_desde_JSON(self, datosJSON):
        self.cantidad_cuatrimestres_plan = datosJSON["cantidad_cuatrimestres_plan"]
        self.estado_plan = datosJSON["estado_plan"]

        # Tiempos
        self.fecha_solicitado = datosJSON["fecha_solicitado"]
        self.fecha_inicio_generacion = datosJSON["fecha_inicio_generacion"]
        self.fecha_fin_generacion = datosJSON["fecha_fin_generacion"]
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
        self.algoritmo = datosJSON["algoritmo"]
        self.tipo_solicitud = datosJSON["tipo_solicitud"]
