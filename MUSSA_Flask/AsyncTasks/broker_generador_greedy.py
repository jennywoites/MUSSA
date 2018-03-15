from celery import Celery

from app.API_Rest.GeneradorPlanCarreras.GeneradorGreedy.GeneradorPlanGreedy import generar_plan_greedy
from app.API_Rest.GeneradorPlanCarreras.GeneradorGreedy.broker_guardar_plan_generado import \
    tarea_guadar_plan_de_estudios
from app.API_Rest.GeneradorPlanCarreras.ParametrosDTO import Parametros
from app.DAO.PlanDeCarreraDAO import PLAN_INCOMPATIBLE, PLAN_FINALIZADO

broker_generador_greedy = Celery('broker', broker='redis://localhost')
broker_generador_greedy.conf.update({
    'task_reject_on_worker_lost': True,
    'task_acks_late': True,
})


@broker_generador_greedy.task(acks_late=True)
def tarea_generar_plan_greedy(parametros_tarea):
    print("INICIO generación plan Greedy con id {}".format(parametros_tarea["id_plan_estudios"]))

    parametros = Parametros()
    parametros.actualizar_valores_desde_JSON(parametros_tarea)

    se_genero_plan_compatible = generar_plan_greedy(parametros)

    parametros.estado_plan_de_estudios = PLAN_INCOMPATIBLE if not se_genero_plan_compatible else PLAN_FINALIZADO

    print("FIN generación plan Greedy con id {}".format(parametros_tarea["id_plan_estudios"]))

    print("Se invoca al guardado para el plan Greedy con id {}".format(parametros_tarea["id_plan_estudios"]))
    tarea_guadar_plan_de_estudios.delay(parametros.generar_parametros_json())
