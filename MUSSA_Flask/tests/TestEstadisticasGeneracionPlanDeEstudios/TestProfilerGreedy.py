if __name__ == '__main__':
    import sys

    sys.path.append("../..")

import json
import os
from app.API_Rest.GeneradorPlanCarreras.GeneradorGreedy.GeneradorPlanGreedy import generar_plan_greedy
from app.API_Rest.GeneradorPlanCarreras.ParametrosDTO import Parametros
import cProfile
import pstats

class TestProfilerGreedy():
    def __init__(self):
        self.ID_USUARIO = 150
        self.id_plan = 0

    def get_next_plan_id(self):
        self.id_plan += 1
        return self.id_plan

    def test_ejecutar_multiples_pedidos_de_generacion_de_planes_de_estudios_greedy(self):
        archivos_parametros = self.obtener_rutas_de_archivos()
        for numero_prueba in archivos_parametros:
            with open(archivos_parametros[numero_prueba], 'r') as file:
                parametros = json.loads(file.read())

            self.invocar_servicio_generacion_plan(parametros)

    def invocar_servicio_generacion_plan(self, parametros_tarea):
        id_plan = self.get_next_plan_id()
        parametros_tarea["user_id"] = self.ID_USUARIO
        parametros_tarea["id_plan_estudios"] = id_plan

        parametros = Parametros()
        parametros.actualizar_valores_desde_JSON(parametros_tarea)

        print("INICIO generación plan Greedy con id {}".format(id_plan))

        se_genero_plan_compatible = generar_plan_greedy(parametros)

        estado_plan = "es INCOMPATIBLE" if not se_genero_plan_compatible else "está FINALIZADO"
        print("FIN generación plan Greedy con id {}. El plan {}".format(id_plan, estado_plan))

    def obtener_rutas_de_archivos(self):
        ruta_archivo = os.path.join(os.getcwd(), 'DatosEstadisticas')
        archivos_parametros = {}
        for ruta in os.listdir(ruta_archivo):
            numero, tipo = ruta.split("_")
            if tipo == "parametros":
                archivos_parametros[numero] = os.path.join('DatosEstadisticas', ruta)
        return archivos_parametros


if __name__ == '__main__':
    RESULTADOS_PROFILER = 'resultados_profiler'

    cProfile.run(
        'TestProfilerGreedy().test_ejecutar_multiples_pedidos_de_generacion_de_planes_de_estudios_greedy()',
        RESULTADOS_PROFILER
    )
    resultados = pstats.Stats(RESULTADOS_PROFILER)
    resultados.sort_stats('time', 'cumulative')
    resultados.print_stats()