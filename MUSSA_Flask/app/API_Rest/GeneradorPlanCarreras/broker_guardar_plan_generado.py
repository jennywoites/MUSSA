from app import db, create_app
from celery import Celery
from app.API_Rest.GeneradorPlanCarreras.ParametrosDTO import Parametros
from app.models.plan_de_estudios_models import PlanDeEstudios, PlanDeEstudiosFinalizadoProcesar, PlanDeEstudiosCache, \
    MateriaPlanDeEstudiosCache, EstadoPlanDeEstudios, MateriaPlanDeEstudios
from app.DAO.PlanDeCarreraDAO import PLAN_INCOMPATIBLE, PLAN_FINALIZADO, ESTADOS_PLAN
from time import time
from datetime import datetime
from app.API_Rest.GeneradorPlanCarreras.EstadisticasDTO import EstadisticasDTO
from app.API_Rest.GeneradorPlanCarreras.my_utils import convertir_tiempo
from app.API_Rest.GeneradorPlanCarreras.my_utils import get_str_fecha_y_hora_actual

broker_guadar_plan_de_estudios = Celery('broker3', broker='redis://redis/5')
broker_guadar_plan_de_estudios.conf.update({
    'task_reject_on_worker_lost': True,
    'task_acks_late': True,
    'create_missing_queues': True,
})


@broker_guadar_plan_de_estudios.task(acks_late=True)
def tarea_guadar_plan_de_estudios(parametros_tarea, estadisticas_tarea):
    print("INICIO guardado plan con id {}".format(parametros_tarea["id_plan_estudios"]))

    estadisticas = EstadisticasDTO()
    estadisticas.cargar_desde_JSON(estadisticas_tarea)
    inicio = time()
    estadisticas.fecha_inicio_guardado = get_str_fecha_y_hora_actual()

    parametros = Parametros()
    parametros.actualizar_valores_desde_JSON(parametros_tarea)

    if estadisticas.tipo_solicitud == "Testing":
        guardado_en_testing(parametros, estadisticas, inicio)
        return

    app = create_app()
    with app.app_context():
        plan_de_estudios = PlanDeEstudios.query.get(parametros_tarea["id_plan_estudios"])

        if not plan_de_estudios:
            print("FIN: El plan con id {} ya no existe. No se guardan los resultados".format(
                parametros_tarea["id_plan_estudios"]))
            return

        if parametros.estado_plan_de_estudios == PLAN_INCOMPATIBLE:
            guardar_y_actualizar_datos_plan(plan_de_estudios, parametros, estadisticas, PLAN_INCOMPATIBLE, inicio)
            print("FIN guardado plan con id {}: (INCOMPATIBLE)".format(parametros_tarea["id_plan_estudios"]))
            return

        agregar_materias_generadas_al_plan(parametros, plan_de_estudios)
        guardar_y_actualizar_datos_plan(plan_de_estudios, parametros, estadisticas, PLAN_FINALIZADO, inicio)
        print("FIN guardado plan con id {} (COMPATIBLE)".format(parametros_tarea["id_plan_estudios"]))


def guardar_y_actualizar_datos_plan(plan_de_estudios, parametros, estadisticas, estado, tiempo_inicial):
    actualizar_plan(plan_de_estudios, estado)
    generar_plan_cache(plan_de_estudios, parametros)
    guardar_estadisticas(parametros, estadisticas, tiempo_inicial)


def guardado_en_testing(parametros, estadisticas, tiempo_inicial):
    if parametros.estado_plan_de_estudios == PLAN_INCOMPATIBLE:
        guardar_estadisticas(parametros, estadisticas, tiempo_inicial)
        print("FIN guardado TESTING plan con id {}: (INCOMPATIBLE)".format(parametros.id_plan_estudios))
        return

    agregar_materias_CBC_al_plan_generado(parametros)
    print("FIN guardado TESTING plan con id {} (COMPATIBLE)".format(parametros.id_plan_estudios))
    guardar_estadisticas(parametros, estadisticas, tiempo_inicial)


def guardar_estadisticas(parametros, estadisticas, tiempo_inicial):
    estadisticas.estado_plan = ESTADOS_PLAN[parametros.estado_plan_de_estudios]
    estadisticas.cantidad_cuatrimestres_plan = len(parametros.plan_generado)
    estadisticas.fecha_fin_guardado = get_str_fecha_y_hora_actual()
    estadisticas.tiempo_total_guardado = convertir_tiempo(time() - tiempo_inicial)
    estadisticas.guardar_en_archivo()


def generar_plan_cache(plan_de_estudios, parametros):
    plan_cacheado = PlanDeEstudiosCache(
        hash_parametros=parametros.hash_precalculado,
        estado_id=plan_de_estudios.estado_id
    )
    db.session.add(plan_cacheado)
    db.session.commit()

    materias_a_copiar = MateriaPlanDeEstudios.query.filter_by(plan_estudios_id=plan_de_estudios.id).all()
    for materia_plan in materias_a_copiar:
        db.session.add(MateriaPlanDeEstudiosCache(
            plan_estudios_cache_id=plan_cacheado.id,
            materia_id=materia_plan.materia_id,
            curso_id=materia_plan.curso_id,
            orden=materia_plan.orden
        ))
    db.session.commit()


def actualizar_plan(plan_de_estudios, nuevo_estado):
    estado = EstadoPlanDeEstudios.query.filter_by(numero=nuevo_estado).first()

    plan_de_estudios.fecha_ultima_actualizacion = datetime.today()
    plan_de_estudios.estado_id = estado.id

    db.session.add(PlanDeEstudiosFinalizadoProcesar(
        alumno_id=plan_de_estudios.alumno_id,
        plan_estudios_id=plan_de_estudios.id
    ))

    db.session.commit()


def agregar_materia_al_plan(plan_de_estudios, id_materia, id_curso, cuatrimestre):
    materia_plan = MateriaPlanDeEstudios(
        plan_estudios_id=plan_de_estudios.id,
        materia_id=id_materia,
        orden=cuatrimestre
    )

    if id_curso and id_curso > 0:
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
