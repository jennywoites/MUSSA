from time import time
from celery import Celery
from app.API_Rest.GeneradorPlanCarreras.EstadisticasDTO import EstadisticasDTO
from app.API_Rest.GeneradorPlanCarreras.GeneradorGreedy.GeneradorPlanGreedy import generar_plan_greedy
from app.API_Rest.GeneradorPlanCarreras.ParametrosDTO import Parametros
from app.API_Rest.GeneradorPlanCarreras.my_utils import convertir_tiempo
from app.DAO.PlanDeCarreraDAO import PLAN_INCOMPATIBLE, PLAN_FINALIZADO
from app.API_Rest.GeneradorPlanCarreras.my_utils import get_str_fecha_y_hora_actual

broker_generador_greedy = Celery('broker2', broker='redis://localhost/2')
broker_generador_greedy.conf.update({
    'task_reject_on_worker_lost': True,
    'task_acks_late': True,
    'create_missing_queues': True
})


@broker_generador_greedy.task(acks_late=True)
def tarea_generar_plan_greedy(parametros_tarea, estadisticas_tarea):
    print("INICIO generación plan Greedy con id {}".format(parametros_tarea["id_plan_estudios"]))

    estadisticas = EstadisticasDTO()
    estadisticas.cargar_desde_JSON(estadisticas_tarea)
    inicio = time()
    estadisticas.fecha_inicio_generacion = get_str_fecha_y_hora_actual()

    parametros = Parametros()
    parametros.actualizar_valores_desde_JSON(parametros_tarea)

    se_genero_plan_compatible = generar_plan_greedy(parametros)

    parametros.estado_plan_de_estudios = PLAN_INCOMPATIBLE if not se_genero_plan_compatible else PLAN_FINALIZADO

    print("FIN generación plan Greedy con id {}".format(parametros_tarea["id_plan_estudios"]))

    estadisticas.fecha_fin_generacion = get_str_fecha_y_hora_actual()
    estadisticas.segundos_total_generacion = float(time() - inicio)
    estadisticas.tiempo_total_generacion = convertir_tiempo(time() - inicio)

    print("Se invoca al guardado para el plan Greedy con id {}".format(parametros_tarea["id_plan_estudios"]))

    from app.API_Rest.GeneradorPlanCarreras.broker_guardar_plan_generado import tarea_guadar_plan_de_estudios
    tarea_guadar_plan_de_estudios.delay(parametros.generar_parametros_json(), estadisticas.get_JSON())
