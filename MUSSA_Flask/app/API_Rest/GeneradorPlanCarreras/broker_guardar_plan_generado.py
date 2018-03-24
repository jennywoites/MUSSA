from app import db, create_app
from app.models.plan_de_estudios_models import EstadoPlanDeEstudios, MateriaPlanDeEstudios
from celery import Celery
from app.API_Rest.GeneradorPlanCarreras.ParametrosDTO import Parametros
from app.models.plan_de_estudios_models import PlanDeEstudios, PlanDeEstudiosFinalizadoProcesar
from app.DAO.PlanDeCarreraDAO import PLAN_INCOMPATIBLE, PLAN_FINALIZADO, ESTADOS_PLAN
from time import time
from datetime import datetime
from app.API_Rest.GeneradorPlanCarreras.EstadisticasDTO import EstadisticasDTO
from app.API_Rest.GeneradorPlanCarreras.my_utils import convertir_tiempo
from app.API_Rest.GeneradorPlanCarreras.my_utils import get_str_fecha_y_hora_actual
import os
import csv

broker_guadar_plan_de_estudios = Celery('broker3', broker='redis://localhost/5')
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
            guardar_estadisticas(parametros, estadisticas, inicio)
            actualizar_plan(plan_de_estudios, PLAN_INCOMPATIBLE)
            print("FIN guardado plan con id {}: (INCOMPATIBLE)".format(parametros_tarea["id_plan_estudios"]))
            return

        agregar_materias_generadas_al_plan(parametros, plan_de_estudios)
        actualizar_plan(plan_de_estudios, PLAN_FINALIZADO)
        print("FIN guardado plan con id {} (COMPATIBLE)".format(parametros_tarea["id_plan_estudios"]))
        guardar_estadisticas(parametros, estadisticas, inicio)

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

    RUTA = "estadisticas_algoritmos.csv"
    if not os.path.isfile(RUTA):
        with open(RUTA, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(estadisticas.get_titulos_CSV())
            writer.writerow(estadisticas.get_linea_CSV())
    else:
        with open(RUTA, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(estadisticas.get_linea_CSV())


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
