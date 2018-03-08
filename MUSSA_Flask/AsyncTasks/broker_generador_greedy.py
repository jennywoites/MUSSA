from celery import Celery
from app.API_Rest.GeneradorPlanCarreras.ParametrosDTO import Parametros
from app.models.plan_de_estudios_models import PlanDeEstudios
from app.API_Rest.GeneradorPlanCarreras.GeneradorPlanGreedy import generar_plan_greedy
from AsyncTasks.utils_generador_plan import actualizar_plan, agregar_materias_generadas_al_plan
from app.DAO.PlanDeCarreraDAO import PLAN_EN_CURSO, PLAN_INCOMPATIBLE, PLAN_FINALIZADO

broker_generador_greedy = Celery('broker', broker='redis://localhost')
broker_generador_greedy.conf.update({
    'task_reject_on_worker_lost': True,
    'task_acks_late': True,
})
# broker_generador_greedy.conf.broker_transport_options = {'visibility_timeout': 40}


@broker_generador_greedy.task(acks_late=True)
def tarea_generar_plan_greedy(parametros_tarea):
    print("INICIO generación plan Greedy con id {}".format(parametros_tarea["id_plan_de_estudios"]))

    parametros = Parametros()
    parametros.actualizar_valores_desde_JSON(parametros_tarea)

    se_genero_plan_compatible = generar_plan_greedy(parametros)
    print(se_genero_plan_compatible)

    plan_de_estudios = PlanDeEstudios.query.get(parametros_tarea["id_plan_de_estudios"])

    if not se_genero_plan_compatible:
        actualizar_plan(plan_de_estudios, PLAN_INCOMPATIBLE)
        print("FIN generación plan Greedy con id {}: (INCOMPATIBLE)".format(parametros_tarea["id_plan_de_estudios"]))
        return

    agregar_materias_generadas_al_plan(parametros, plan_de_estudios)
    actualizar_plan(plan_de_estudios, PLAN_FINALIZADO)

    print("FIN generación plan Greedy con id {} (COMPATIBLE)".format(parametros_tarea["id_plan_de_estudios"]))
