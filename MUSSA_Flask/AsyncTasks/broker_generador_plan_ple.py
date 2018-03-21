import os
from celery import Celery
from app.API_Rest.GeneradorPlanCarreras.GeneradorPLE.GeneradorCodigoPulp import generar_archivo_pulp
from app.API_Rest.GeneradorPlanCarreras.GeneradorPLE.OptimizadorCodigoPulp import optimizar_codigo_pulp
from app.API_Rest.GeneradorPlanCarreras.ParametrosDTO import Parametros
from app.API_Rest.GeneradorPlanCarreras.broker_guardar_plan_generado import \
    tarea_guadar_plan_de_estudios
from app.DAO.PlanDeCarreraDAO import PLAN_INCOMPATIBLE, PLAN_FINALIZADO
from app.API_Rest.GeneradorPlanCarreras.my_utils import get_str_fecha_y_hora_actual
from time import time as tiempo
import time
from app.API_Rest.GeneradorPlanCarreras.EstadisticasDTO import EstadisticasDTO
from app.API_Rest.GeneradorPlanCarreras.my_utils import convertir_tiempo

broker_generador_ple = Celery('broker', broker='redis://localhost')
broker_generador_ple.conf.update({
    'task_reject_on_worker_lost': True,
    'task_acks_late': True,
})
broker_generador_ple.conf.broker_transport_options = {'visibility_timeout': 14400}  # 3hs

OPTIMAL = "Optimal"


@broker_generador_ple.task(acks_late=True)
def tarea_generar_plan_ple(parametros_tarea, estadisticas_tarea):
    print("INICIO generación plan PLE con id {}".format(parametros_tarea["id_plan_estudios"]))

    estadisticas = EstadisticasDTO()
    estadisticas.cargar_desde_JSON(estadisticas_tarea)
    inicio = tiempo()
    estadisticas.fecha_inicio_generacion = get_str_fecha_y_hora_actual()

    parametros = Parametros()
    parametros.actualizar_valores_desde_JSON(parametros_tarea)

    generar_y_ejecutar_codigo_PULP(parametros)

    estadisticas.fecha_fin_generacion = get_str_fecha_y_hora_actual()
    estadisticas.tiempo_total_generacion = convertir_tiempo(tiempo() - inicio)

    print("FIN generación plan PLE con id {}".format(parametros_tarea["id_plan_estudios"]))

    print("Se invoca al guardado para el plan PLE con id {}".format(parametros_tarea["id_plan_estudios"]))
    tarea_guadar_plan_de_estudios.delay(parametros.generar_parametros_json(), estadisticas.get_JSON())


def generar_y_ejecutar_codigo_PULP(parametros):
    generar_ruta_archivo_pulp(parametros)

    print("Generando archivo PULP para plan con id {}".format(parametros.id_plan_estudios))
    generar_archivo_pulp(parametros)

    print("Generando archivo PULP OPTIMIZADO para plan con id {}".format(parametros.id_plan_estudios))
    optimizar_codigo_pulp(parametros)

    print("Ejecutando codigo PULP OPTIMIZADO para plan con id {}".format(parametros.id_plan_estudios))
    ejecutar_codigo_pulp(parametros)

    print("Obteniendo resultados PULP para plan con id {}".format(parametros.id_plan_estudios))
    resultados = obtener_resultados_pulp(parametros)

    parametros.estado_plan_de_estudios = PLAN_FINALIZADO if resultados["status"] == OPTIMAL else PLAN_INCOMPATIBLE

    if parametros.estado_plan_de_estudios == PLAN_FINALIZADO:
        armar_plan(parametros, resultados)


def generar_ruta_archivo_pulp(parametros):
    os.chdir(os.path.join(os.getcwd(), 'app'))

    if not os.path.isdir('tmp'):
        os.mkdir('tmp')
    os.chdir(os.path.join(os.getcwd(), 'tmp'))

    if not os.path.isdir(str(parametros.user_id)):
        os.mkdir(str(parametros.user_id))

    os.chdir(os.path.join(os.getcwd(), '..', '..'))

    # Actualizo la ruta de los archivos a la nueva ruta creada
    ruta_archivos = os.path.join('app', 'tmp', str(parametros.user_id))
    parametros.nombre_archivo_pulp = os.path.join(ruta_archivos, parametros.nombre_archivo_pulp)
    parametros.nombre_archivo_pulp_optimizado = os.path.join(ruta_archivos, parametros.nombre_archivo_pulp_optimizado)
    parametros.nombre_archivo_resultados_pulp = os.path.join(ruta_archivos, parametros.nombre_archivo_resultados_pulp)


def ejecutar_codigo_pulp(parametros):
    os.system('python3 ' + parametros.nombre_archivo_pulp_optimizado)
    time.sleep(2)  # Porque a veces no termina de liberar el archivo y el otro no lo encuentra


def obtener_resultados_pulp(parametros):
    resultados = {}

    with open(parametros.nombre_archivo_resultados_pulp, 'r') as arch:
        primera = True
        for linea in arch:

            if primera:
                primera = False
                continue

            linea = linea.rstrip("\n")
            variable, valor = linea.split(";")
            try:
                resultados[variable] = int(valor)
            except:
                resultados[variable] = valor

    return resultados


def armar_plan(parametros, resultados):
    if not resultados:
        return

    VARIABLE = 0
    ID_MATERIA = 1
    ID_CURSO = 2
    CUATRIMESTRE = 3

    materias_por_cuatrimestre = {}
    max_cuatrimestre = 0
    for variable in resultados:
        valor = resultados[variable]
        if (not "H_" in variable) or (valor == 0):
            continue
        datos_variable = variable.split("_")

        id_materia = int(datos_variable[ID_MATERIA])
        id_curso = int(datos_variable[ID_CURSO])
        cuatri = int(datos_variable[CUATRIMESTRE])

        materias_cuatri = materias_por_cuatrimestre.get(cuatri, {})
        materias_cuatri[id_materia] = id_curso
        max_cuatrimestre = max(max_cuatrimestre, cuatri)
        materias_por_cuatrimestre[cuatri] = materias_cuatri

    for materia in parametros.materia_trabajo_final:
        variable = "C_TP_FINAL_{}_{}".format(materia.id_materia, materia.codigo)
        if variable in resultados:
            cuatrimestre = int(resultados[variable])

            materias_cuatri = materias_por_cuatrimestre.get(cuatrimestre, {})
            materias_cuatri[materia.id_materia] = -1  # No hay cursos
            max_cuatrimestre = max(max_cuatrimestre, cuatrimestre)
            materias_por_cuatrimestre[cuatrimestre] = materias_cuatri

    parametros.plan_generado = []
    for i in range(max_cuatrimestre):
        parametros.plan_generado.append({})

    for cuatrimestre in materias_por_cuatrimestre:
        parametros.plan_generado[cuatrimestre - 1] = materias_por_cuatrimestre[cuatrimestre]
