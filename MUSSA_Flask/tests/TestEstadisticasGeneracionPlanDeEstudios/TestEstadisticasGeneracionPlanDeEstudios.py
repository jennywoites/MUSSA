if __name__ == '__main__':
    import sys

    sys.path.append("../..")

import os
import json
from app.API_Rest.GeneradorPlanCarreras.my_utils import get_str_fecha_y_hora_actual
from AsyncTasks.broker_generador_greedy import tarea_generar_plan_greedy


class TestEstadisticasGeneracionPlanDeEstudios():
    def __init__(self):
        self.ID_USUARIO = 150
        self.id_plan = 0

    def get_next_plan_id(self):
        self.id_plan += 1
        return self.id_plan

    def test_ejecutar_diferentes_pedidos_de_generacion_de_planes_de_estudios(self):
        archivos_parametros, archivos_estadisticas = self.obtener_rutas_de_archivos()
        for numero_prueba in archivos_parametros:
            if not numero_prueba in archivos_estadisticas:
                continue

            with open(archivos_parametros[numero_prueba], 'r') as file:
                parametros = json.loads(file.read())

            with open(archivos_estadisticas[numero_prueba], 'r') as file:
                estadisticas = json.loads(file.read())

            self.invocar_servicios_generacion_plan(parametros, estadisticas)

    def invocar_servicios_generacion_plan(self, parametros, estadisticas):
        parametros["user_id"] = self.ID_USUARIO
        estadisticas["tipo_solicitud"] = "Testing"

        self.invocar_servicio_generacion_plan_greedy(parametros, estadisticas)
        self.invocar_servicio_generacion_plan_ple(parametros, estadisticas)

    def invocar_servicio_generacion_plan_greedy(self, parametros, estadisticas):
        parametros["id_plan_estudios"] = self.get_next_plan_id()

        estadisticas["algoritmo"] = "GREEDY"
        estadisticas["fecha_solicitado"] = get_str_fecha_y_hora_actual()

        tarea = tarea_generar_plan_greedy.delay(parametros, estadisticas)
        assert (tarea is not None)

    def invocar_servicio_generacion_plan_ple(self, parametros, estadisticas):
        id_plan = self.get_next_plan_id()
        parametros["id_plan_estudios"] = id_plan
        parametros["nombre_archivo_pulp"] = "pulp_generado_plan_{}.py".format(id_plan)
        parametros["nombre_archivo_resultados_pulp"] = "pulp_resultados_plan_{}.py".format(id_plan)
        parametros["nombre_archivo_pulp_optimizado"] = "pulp_optimizado_plan_{}.py".format(id_plan)

        estadisticas["algoritmo"] = "PLE"
        estadisticas["fecha_solicitado"] = get_str_fecha_y_hora_actual()

        # FIXME: Hacer la invocacion del servicio

    def obtener_rutas_de_archivos(self):
        ruta_archivo = os.path.join(os.getcwd(), 'DatosEstadisticas')
        archivos_parametros = {}
        archivos_estadisticas = {}
        for ruta in os.listdir(ruta_archivo):
            numero, tipo = ruta.split("_")
            if tipo == "parametros":
                archivos_parametros[numero] = os.path.join('DatosEstadisticas', ruta)
            elif tipo == "estadisticas":
                archivos_estadisticas[numero] = os.path.join('DatosEstadisticas', ruta)
        return archivos_parametros, archivos_estadisticas


if __name__ == '__main__':
    tests = TestEstadisticasGeneracionPlanDeEstudios()
    tests.test_ejecutar_diferentes_pedidos_de_generacion_de_planes_de_estudios()
