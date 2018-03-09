from app import db, create_app
from app.models.plan_de_estudios_models import EstadoPlanDeEstudios, MateriaPlanDeEstudios
from datetime import datetime
from celery import Celery
from app.API_Rest.GeneradorPlanCarreras.ParametrosDTO import Parametros
from app.models.plan_de_estudios_models import PlanDeEstudios
from app.DAO.PlanDeCarreraDAO import PLAN_INCOMPATIBLE, PLAN_FINALIZADO

broker_guadar_plan_de_estudios = Celery('broker', broker='redis://localhost')
broker_guadar_plan_de_estudios.conf.update({
    'task_reject_on_worker_lost': True,
    'task_acks_late': True,
})


@broker_guadar_plan_de_estudios.task(acks_late=True)
def tarea_guadar_plan_de_estudios(parametros_tarea):
    print("INICIO guardado plan con id {}".format(parametros_tarea["id_plan_estudios"]))
    app = create_app()

    parametros = Parametros()
    parametros.actualizar_valores_desde_JSON(parametros_tarea)

    with app.app_context():
        plan_de_estudios = PlanDeEstudios.query.get(parametros_tarea["id_plan_estudios"])

        if parametros.estado_plan_de_estudios == PLAN_INCOMPATIBLE:
            actualizar_plan(plan_de_estudios, PLAN_INCOMPATIBLE)
            print("FIN guardado plan con id {}: (INCOMPATIBLE)".format(parametros_tarea["id_plan_estudios"]))
            return

        agregar_materias_generadas_al_plan(parametros, plan_de_estudios)
        actualizar_plan(plan_de_estudios, PLAN_FINALIZADO)
        print("FIN guardado plan con id {} (COMPATIBLE)".format(parametros_tarea["id_plan_estudios"]))


def actualizar_plan(plan_de_estudios, nuevo_estado):
    estado = EstadoPlanDeEstudios.query.filter_by(numero=nuevo_estado).first()

    plan_de_estudios.fecha_ultima_actualizacion = datetime.today()
    plan_de_estudios.estado_id = estado.id

    db.session.commit()


def agregar_materia_al_plan(plan_de_estudios, id_materia, id_curso, cuatrimestre):
    materia_plan = MateriaPlanDeEstudios(
        plan_estudios_id=plan_de_estudios.id,
        materia_id=id_materia,
        orden=cuatrimestre
    )

    if id_curso:
        materia_plan.curso_id = id_curso

    db.session.add(materia_plan)
    db.session.commit()


def agregar_materias_CBC_al_plan_generado(parametros):
    if not parametros.materias_CBC_pendientes:
        return

    grupos_CBC = []
    grupo_actual = {}
    for index, id_materia in enumerate(parametros.materias_CBC_pendientes):
        id_curso = None
        grupo_actual[id_materia] = id_curso

        if (index + 1) % 3 == 0:
            grupos_CBC.append(grupo_actual)
            grupo_actual = {}

    if grupo_actual:  # En caso de tener menos materias por cuatrimestre
        grupos_CBC.append(grupo_actual)

    for i in range(len(grupos_CBC) - 1, -1, -1):
        grupo_cuatrimestre = grupos_CBC[i]
        parametros.plan_generado.insert(0, grupo_cuatrimestre)


def agregar_materias_generadas_al_plan(parametros, plan_de_estudios):
    agregar_materias_CBC_al_plan_generado(parametros)

    for cuatrimestre, grupo_materias in enumerate(parametros.plan_generado):
        for id_materia in grupo_materias:
            id_curso = grupo_materias[id_materia]
            agregar_materia_al_plan(plan_de_estudios, id_materia, id_curso, cuatrimestre)
