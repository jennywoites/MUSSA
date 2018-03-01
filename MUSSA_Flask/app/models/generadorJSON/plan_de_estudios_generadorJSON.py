from app.models.plan_de_estudios_models import EstadoPlanDeEstudios, MateriaPlanDeEstudios
from app.models.carreras_models import Materia, Carrera
from app.models.horarios_models import Curso
from app.models.alumno_models import MateriasAlumno, EstadoMateria
from app.DAO.MateriasDAO import ESTADO_MATERIA, DESAPROBADA, PENDIENTE, FINAL_PENDIENTE, EN_CURSO, APROBADA
from app.models.generadorJSON.alumno_generadorJSON import generar_string_curso
from app.models.generadorJSON.horarios_generadorJSON import obtener_horarios_response
from app.models.filtros.alumno_filter import filtrar_materias_alumno


def generarJSON_plan_de_estudios(plan_de_estudios):
    estado = EstadoPlanDeEstudios.query.get(plan_de_estudios.estado_id)
    fecha = plan_de_estudios.fecha_generacion
    return {
        'id_plan': plan_de_estudios.id,
        'fecha_generacion': "{}/{}/{}".format(fecha.day, fecha.month, fecha.year),
        'estado_id': estado.id,
        'estado_numero': estado.numero,
        'estado': estado.descripcion,
    }


def generarJSON_materias_plan_de_estudios(plan_de_estudios):
    datos_plan = generarJSON_plan_de_estudios(plan_de_estudios)

    materias_por_cuatrimestre = {}
    ids_a_excluir_materias_aprobadas = []

    min_cuatri_anio, max_cuatri_anio = agregar_materias_plan_de_estudios(plan_de_estudios, materias_por_cuatrimestre,
                                                                         ids_a_excluir_materias_aprobadas)

    materiasJSON = agregar_materias_no_pendientes_no_contempladas_en_plan(plan_de_estudios, materias_por_cuatrimestre,
                                                                          ids_a_excluir_materias_aprobadas,
                                                                          min_cuatri_anio,
                                                                          max_cuatri_anio)

    datos_plan["materias_por_cuatrimestre"] = materiasJSON
    return datos_plan


def agregar_materias_plan_de_estudios(plan_de_estudios, materias_por_cuatrimestre, ids_a_excluir_materias_aprobadas):
    min_cuatri_anio, max_cuatri_anio = None, None
    for materia_plan in MateriaPlanDeEstudios.query.filter_by(plan_estudios_id=plan_de_estudios.id).all():
        materia = Materia.query.get(materia_plan.materia_id)
        curso = Curso.query.get(materia_plan.curso_id) if materia_plan.curso_id else None

        materias_alumno = MateriasAlumno.query.filter_by(alumno_id=plan_de_estudios.alumno_id) \
            .filter_by(materia_id=materia.id).all()
        estado_desaprobada = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[DESAPROBADA]).first().id
        estado_pendiente = EstadoMateria.query.filter_by(estado=ESTADO_MATERIA[PENDIENTE]).first().id

        for materia_alumno in materias_alumno:
            if materia_alumno.estado_id != estado_desaprobada:
                ids_a_excluir_materias_aprobadas.append(materia_alumno.id)

            if materia_alumno.estado_id == estado_pendiente:
                curso_actual = curso
                anio, cuatrimestre = obtener_anio_y_cuatrimestre(plan_de_estudios, materia_plan)
            else:
                curso_actual = Curso.query.get(materia_alumno.curso_id) if materia_alumno.curso_id else None
                anio, cuatrimestre = int(materia_alumno.anio_aprobacion_cursada), \
                                     int(materia_alumno.cuatrimestre_aprobacion_cursada)

            json_materia = generarJSON_materia_plan(materia, materia_alumno, curso_actual)
            materias_cuatrimestre = materias_por_cuatrimestre.get((anio, cuatrimestre), [])
            materias_cuatrimestre.append(json_materia)
            materias_por_cuatrimestre[(anio, cuatrimestre)] = materias_cuatrimestre

            if not min_cuatri_anio and not max_cuatri_anio:
                min_cuatri_anio = (anio, cuatrimestre)
                max_cuatri_anio = (anio, cuatrimestre)

            min_cuatri_anio = min(min_cuatri_anio, (anio, cuatrimestre))
            max_cuatri_anio = max(max_cuatri_anio, (anio, cuatrimestre))

    return min_cuatri_anio, max_cuatri_anio


def agregar_materias_no_pendientes_no_contempladas_en_plan(plan_de_estudios, materias_por_cuatrimestre,
                                                           ids_a_excluir_materias_aprobadas, min_cuatri_anio,
                                                           max_cuatri_anio):
    filtro = {}
    filtro["id_alumno"] = plan_de_estudios.alumno_id
    filtro["estados"] = [APROBADA, DESAPROBADA, FINAL_PENDIENTE, EN_CURSO]
    filtro["ids_a_excluir"] = ids_a_excluir_materias_aprobadas

    for materia_alumno in filtrar_materias_alumno(filtro):
        materia = Materia.query.get(materia_alumno.materia_id)
        curso_actual = Curso.query.get(materia_alumno.curso_id) if materia_alumno.curso_id else None
        anio, cuatrimestre = int(materia_alumno.anio_aprobacion_cursada), \
                             int(materia_alumno.cuatrimestre_aprobacion_cursada)

        json_materia = generarJSON_materia_plan(materia, materia_alumno, curso_actual)

        materias_cuatrimestre = materias_por_cuatrimestre.get((anio, cuatrimestre), [])
        materias_cuatrimestre.append(json_materia)
        materias_por_cuatrimestre[(anio, cuatrimestre)] = materias_cuatrimestre

        min_cuatri_anio = min(min_cuatri_anio, (anio, cuatrimestre))
        max_cuatri_anio = max(max_cuatri_anio, (anio, cuatrimestre))

    return normalizar_materias_y_completar_cuatrimestres_vacios(materias_por_cuatrimestre, min_cuatri_anio,
                                                                max_cuatri_anio)


def normalizar_materias_y_completar_cuatrimestres_vacios(materias_por_cuatrimestre, min_cuatri_anio, max_cuatri_anio):
    materiasJSON = []
    POS_ANIO = 0
    agregados = 0
    for anio in range(min_cuatri_anio[POS_ANIO], max_cuatri_anio[POS_ANIO] + 1):
        for cuatrimestre in range(1, 2 + 1):
            materias = materias_por_cuatrimestre.get((anio, cuatrimestre), [])
            if materias:
                agregados += 1
            if materias or (agregados != 0 and agregados != len(materias_por_cuatrimestre)):
                materiasJSON.append({
                    "cuatrimestre": cuatrimestre,
                    "anio": anio,
                    "materias": materias
                })

    return materiasJSON


def obtener_anio_y_cuatrimestre(plan_de_estudios, materia_plan):
    anio_inicio = int(plan_de_estudios.anio_inicio_plan)
    cuatri_inicio = int(plan_de_estudios.cuatrimestre_inicio_plan)
    orden = materia_plan.orden + 1 #Para los calculos se requiere que el orden comience en 1 en lugar de en 0

    if orden < cuatri_inicio:
        anio = anio_inicio + (1 if orden == 2 else 0)
    else:
        anios_extras = (orden - cuatri_inicio) // 2 + (1 if cuatri_inicio == 2 and orden > 1 else 0)
        anio = anio_inicio + anios_extras

    siguiente = 2 if cuatri_inicio == 1 else 1
    cuatrimestre = siguiente if (orden % 2 == 0) else cuatri_inicio

    return anio, cuatrimestre


def generarJSON_materia_plan(materia, materia_alumno, curso):
    carrera = Carrera.query.get(materia.carrera_id)
    return {
        'id_materia': materia.id,
        'codigo': materia.codigo,
        'nombre': materia.nombre,
        'id_carrera': carrera.id,
        'codigo_carrera': carrera.codigo,
        'id_curso': curso.id if curso else -1,
        'carrera': carrera.get_descripcion_carrera(),
        'curso': generar_string_curso(curso),
        'estado': EstadoMateria.query.get(materia_alumno.estado_id).estado,
        'codigo_curso': curso.codigo if curso else '',
        'horarios': obtener_horarios_response(curso),
        'puntaje': curso.calcular_puntaje() if curso else "-",
    }
