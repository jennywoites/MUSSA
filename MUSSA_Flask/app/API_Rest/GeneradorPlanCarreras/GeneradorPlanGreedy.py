from app.API_Rest.GeneradorPlanCarreras.modelos.Materia import ELECTIVA, OBLIGATORIA

PLAN_NO_GENERADO = False
PLAN_GENERADO_CORRECTAMENTE = True

MAX_COMBINACIONES = 25 * 24 * 23 * 22 * 21  # 25 cursos posibles, 5 materias max


def generar_plan_greedy(parametros):
    creditos_totales = 0
    while (not parametros.plan_esta_finalizado()):
        if len(parametros.plan_generado) == parametros.max_cuatrimestres:
            return PLAN_NO_GENERADO

        materias_cuatrimestre_actual, creditos_totales = generar_cuatrimestre_actual(parametros, creditos_totales)

        if not materias_cuatrimestre_actual:
            return PLAN_NO_GENERADO

        parametros.plan_generado.append(materias_cuatrimestre_actual)

    return PLAN_GENERADO_CORRECTAMENTE


def generar_cuatrimestre_actual(parametros, creditos_totales):
    materias_disponibles = parametros.obtener_materias_disponibles(creditos_totales)

    combinaciones = len(materias_disponibles)
    for i in range(1, parametros.max_cant_materias_por_cuatrimestre):
        combinaciones = combinaciones * (len(materias_disponibles) - i)

    if combinaciones > MAX_COMBINACIONES:
        return generar_cuatrimestre_actual_greedy(parametros, materias_disponibles, creditos_totales)

    mejor_combinacion = generar_posibles_combinaciones_cuatrimestre(parametros, materias_disponibles, creditos_totales)
    if not mejor_combinacion:
        return {}, creditos_totales

    parametros.actualizar_datos_con_parametros_seleccionados(mejor_combinacion[PARAMETROS_ACTUALES])
    return mejor_combinacion[MATERIAS_CUATRI_ACTUAL], mejor_combinacion[CREDITOS_TOTALES]


def generar_cuatrimestre_actual_greedy(parametros, materias_disponibles, creditos_totales):
    materias_cuatrimestre_actual = {}

    franjas_cuatrimestre = parametros.generar_lista_franjas_limpia()
    medias_horas_cursada = 0
    medias_horas_extras = 0

    for index, grupo_materia in enumerate(materias_disponibles):
        materia, curso = grupo_materia

        # Si el cuatrimestre esta completo en cantidad de materias, cierro el cuatrimestre
        if combinacion_esta_completa(parametros, len(materias_cuatrimestre_actual), medias_horas_extras,
                                     medias_horas_cursada):
            break

        franjas_curso, horas_cursada = curso.obtener_franjas_curso() if curso else ([], 0)

        if not es_posible_agregar_materia_y_curso(materia, franjas_curso, horas_cursada,
                                                  materia.medias_horas_extras_cursada, franjas_cuatrimestre,
                                                  medias_horas_cursada, medias_horas_extras, parametros,
                                                  materias_cuatrimestre_actual):
            continue

        creditos_totales += materia.creditos
        medias_horas_cursada += horas_cursada
        medias_horas_extras += materia.medias_horas_extras_cursada
        agregar_materia_y_actualizar_creditos(materia, curso, franjas_curso, parametros,
                                              materias_cuatrimestre_actual, franjas_cuatrimestre)

    return materias_cuatrimestre_actual, creditos_totales


PARAMETROS_ACTUALES = "parametros_actuales"
CREDITOS_TOTALES = "creditos_totales"
FRANJAS_CUATRIMESTRE = "franjas_cuatrimestre"
MEDIAS_HORAS_CURSADA = "medias_horas_cursada"
MEDIAS_HORAS_EXTRAS = "medias_horas_extras"
MATERIAS_CUATRI_ACTUAL = "materias_cuatrimestre_actual"
CANT_OBLIGATORIAS_QUE_LIBERA = "cant_obligatorias_que_libera"
CANT_CREDITOS_TEMATICAS = "cant_creditos_tematicas"
CANT_CREDITOS_ELECTIVAS = "cant_creditos_electivas"


def generar_posibles_combinaciones_cuatrimestre(parametros, materias_disponibles, creditos_totales):
    mejor_combinacion = None

    posibles_combinaciones = [{
        PARAMETROS_ACTUALES: parametros.copia_profunda(),
        FRANJAS_CUATRIMESTRE: parametros.generar_lista_franjas_limpia(),
        MEDIAS_HORAS_CURSADA: 0,
        MEDIAS_HORAS_EXTRAS: 0,
        CREDITOS_TOTALES: creditos_totales,
        CANT_OBLIGATORIAS_QUE_LIBERA: 0,
        CANT_CREDITOS_TEMATICAS: 0,
        CANT_CREDITOS_ELECTIVAS: 0,
        MATERIAS_CUATRI_ACTUAL: {}
    }]

    for index, grupo_materia in enumerate(materias_disponibles):
        materia, curso = grupo_materia
        nuevas_posibles_combinaciones = []

        for combinacion in posibles_combinaciones:

            nueva_combinacion = copiar_combinacion(combinacion)
            parametros = nueva_combinacion[PARAMETROS_ACTUALES]

            # Si el cuatrimestre esta completo en cantidad de materias, cierro el cuatrimestre
            if combinacion_esta_completa(parametros, nueva_combinacion[MATERIAS_CUATRI_ACTUAL],
                                         nueva_combinacion[MEDIAS_HORAS_EXTRAS],
                                         nueva_combinacion[MEDIAS_HORAS_CURSADA]):
                break

            franjas_curso, horas_cursada = curso.obtener_franjas_curso() if curso else ([], 0)

            if not es_posible_agregar_materia_y_curso(materia, franjas_curso, horas_cursada,
                                                      materia.medias_horas_extras_cursada,
                                                      nueva_combinacion[FRANJAS_CUATRIMESTRE],
                                                      nueva_combinacion[MEDIAS_HORAS_CURSADA],
                                                      nueva_combinacion[MEDIAS_HORAS_EXTRAS],
                                                      parametros, nueva_combinacion[MATERIAS_CUATRI_ACTUAL]):
                continue

            nueva_combinacion[CREDITOS_TOTALES] += materia.creditos
            nueva_combinacion[MEDIAS_HORAS_CURSADA] += horas_cursada
            nueva_combinacion[MEDIAS_HORAS_EXTRAS] += materia.medias_horas_extras_cursada

            if materia.tipo == ELECTIVA:
                nueva_combinacion[CANT_CREDITOS_ELECTIVAS] += materia.creditos
                nueva_combinacion[CANT_CREDITOS_TEMATICAS] += parametros.calcular_creditos_aportados_tematicas(materia)

            if materia.codigo in parametros.plan:
                for cod_correlativa_liberada in parametros.plan[materia.codigo]:
                    if parametros.materias[cod_correlativa_liberada].tipo == OBLIGATORIA:
                        nueva_combinacion[CANT_OBLIGATORIAS_QUE_LIBERA] += 1

            agregar_materia_y_actualizar_creditos(materia, curso, franjas_curso, parametros,
                                                  nueva_combinacion[MATERIAS_CUATRI_ACTUAL],
                                                  nueva_combinacion[FRANJAS_CUATRIMESTRE])

            nuevas_posibles_combinaciones.append(nueva_combinacion)

        for combinacion in nuevas_posibles_combinaciones:
            posibles_combinaciones.append(combinacion)

        for i in range(len(posibles_combinaciones) - 1, -1, -1):
            combinacion = posibles_combinaciones.pop()
            if combinacion_esta_completa(combinacion[PARAMETROS_ACTUALES], combinacion[MATERIAS_CUATRI_ACTUAL],
                                         combinacion[MEDIAS_HORAS_EXTRAS], combinacion[MEDIAS_HORAS_CURSADA]):
                mejor_combinacion = obtener_mejor_combinacion(mejor_combinacion, combinacion)
            else:
                posibles_combinaciones.insert(0, combinacion)

    if not mejor_combinacion:
        for i in range(len(posibles_combinaciones)):
            mejor_combinacion = obtener_mejor_combinacion(mejor_combinacion, posibles_combinaciones.pop())

    return mejor_combinacion


def combinacion_esta_completa(parametros, cantidad_materias, medias_horas_extra, medias_horas_cursada):
    return (parametros.max_cant_materias_por_cuatrimestre == cantidad_materias or
            parametros.max_horas_extras == medias_horas_extra or
            parametros.max_horas_cursada == medias_horas_cursada)


def obtener_mejor_combinacion(mejor_combinacion_actual, combinacion_nueva):
    if not mejor_combinacion_actual:
        return combinacion_nueva

    if len(mejor_combinacion_actual[MATERIAS_CUATRI_ACTUAL]) > len(combinacion_nueva[MATERIAS_CUATRI_ACTUAL]):
        return mejor_combinacion_actual

    if len(mejor_combinacion_actual[MATERIAS_CUATRI_ACTUAL]) < len(combinacion_nueva[MATERIAS_CUATRI_ACTUAL]):
        return combinacion_nueva

    if mejor_combinacion_actual[CANT_OBLIGATORIAS_QUE_LIBERA] > combinacion_nueva[CANT_OBLIGATORIAS_QUE_LIBERA]:
        return mejor_combinacion_actual

    if mejor_combinacion_actual[CANT_OBLIGATORIAS_QUE_LIBERA] < combinacion_nueva[CANT_OBLIGATORIAS_QUE_LIBERA]:
        return combinacion_nueva

    if mejor_combinacion_actual[CANT_CREDITOS_TEMATICAS] > combinacion_nueva[CANT_CREDITOS_TEMATICAS]:
        return mejor_combinacion_actual

    if mejor_combinacion_actual[CANT_CREDITOS_TEMATICAS] < combinacion_nueva[CANT_CREDITOS_TEMATICAS]:
        return combinacion_nueva

    if mejor_combinacion_actual[CANT_CREDITOS_ELECTIVAS] > combinacion_nueva[CANT_CREDITOS_ELECTIVAS]:
        return mejor_combinacion_actual

    if mejor_combinacion_actual[CANT_CREDITOS_ELECTIVAS] < combinacion_nueva[CANT_CREDITOS_ELECTIVAS]:
        return combinacion_nueva

    if mejor_combinacion_actual[CREDITOS_TOTALES] > combinacion_nueva[CREDITOS_TOTALES]:
        return mejor_combinacion_actual

    if mejor_combinacion_actual[CREDITOS_TOTALES] < combinacion_nueva[CREDITOS_TOTALES]:
        return combinacion_nueva

    if mejor_combinacion_actual[MEDIAS_HORAS_CURSADA] < combinacion_nueva[MEDIAS_HORAS_CURSADA]:
        return mejor_combinacion_actual

    if mejor_combinacion_actual[MEDIAS_HORAS_CURSADA] > combinacion_nueva[MEDIAS_HORAS_CURSADA]:
        return combinacion_nueva

    if mejor_combinacion_actual[MEDIAS_HORAS_EXTRAS] < combinacion_nueva[MEDIAS_HORAS_EXTRAS]:
        return mejor_combinacion_actual

    if mejor_combinacion_actual[MEDIAS_HORAS_EXTRAS] > combinacion_nueva[MEDIAS_HORAS_EXTRAS]:
        return combinacion_nueva

    return mejor_combinacion_actual


def copiar_combinacion(combinacion):
    franjas = {}
    for dia in combinacion[FRANJAS_CUATRIMESTRE]:
        franjas[dia] = combinacion[FRANJAS_CUATRIMESTRE][dia][:]

    materias = {}
    for cod in combinacion[MATERIAS_CUATRI_ACTUAL]:
        materias[cod] = combinacion[MATERIAS_CUATRI_ACTUAL][cod]

    return {
        PARAMETROS_ACTUALES: combinacion[PARAMETROS_ACTUALES].copia_profunda(),
        FRANJAS_CUATRIMESTRE: franjas,
        MEDIAS_HORAS_CURSADA: combinacion[MEDIAS_HORAS_CURSADA],
        MEDIAS_HORAS_EXTRAS: combinacion[MEDIAS_HORAS_EXTRAS],
        CREDITOS_TOTALES: combinacion[CREDITOS_TOTALES],
        CANT_OBLIGATORIAS_QUE_LIBERA: combinacion[CANT_OBLIGATORIAS_QUE_LIBERA],
        CANT_CREDITOS_TEMATICAS: combinacion[CANT_CREDITOS_TEMATICAS],
        CANT_CREDITOS_ELECTIVAS: combinacion[CANT_CREDITOS_ELECTIVAS],
        MATERIAS_CUATRI_ACTUAL: materias
    }


def es_posible_agregar_materia_y_curso(materia, franjas_curso, horas_cursada,
                                       horas_extras_del_curso, franjas_cuatrimestre, medias_horas_cursada,
                                       medias_horas_extras, parametros, materias_cuatrimestre_actual):
    # Verifico que no se haya agregado ya la materia en este cuatrimestre y este sea otro de los horarios
    # disponibles para el mismo código de materia
    if (materia.codigo in materias_cuatrimestre_actual):
        return False

    # Si ya alcance la cantidad de materias en el cuatrimestre, no se puede agregar
    if (parametros.max_cant_materias_por_cuatrimestre == len(materias_cuatrimestre_actual)):
        return False

    # Verifico que las horas de cursada sean aceptables
    if (horas_cursada + medias_horas_cursada) > parametros.max_horas_cursada:
        return False

    # Verifico que las horas extra sean aceptables
    if (horas_extras_del_curso + medias_horas_extras) > parametros.max_horas_extras:
        return False

    # Verifico que si es una materia electiva no haya cumplido ya con los creditos requeridos
    # para electivas en general y los creditos por temáticas para las electivas
    if materia.tipo == ELECTIVA and parametros.creditos_en_electivas_estan_completos():
        return False

    # Verifico que la materia no sea incompatible con otras que ya han sido agregadas:
    if materia.codigo in parametros.materias_incompatibles:
        for cod_incompatible in parametros.materias_incompatibles[materia.codigo]:
            if parametros.se_encuentra_materia_en_plan_generado(cod_incompatible, materias_cuatrimestre_actual):
                return False

    # Verifico que el horario sea compatible
    for dia in franjas_curso:
        for franja_curso in franjas_curso[dia]:
            # Si la franja esta ocupada ese cuatrimestre el if da True
            if franjas_cuatrimestre[dia][franja_curso - 1]:
                return False
    return True


def agregar_materia_y_actualizar_creditos(materia, curso, franjas_curso, parametros, materias_cuatrimestre_actual,
                                          franjas_cuatrimestre):
    materias_cuatrimestre_actual[materia.codigo] = {
        "id_materia": materia.id_materia,
        "id_curso": curso.id_curso if curso else -1
    }

    if not curso:
        actualizar_datos_al_agregar_materia_trabajo_final(parametros, materia)
    else:
        actualizar_datos_al_agregar_materia_con_curso(parametros, materia, franjas_curso, franjas_cuatrimestre)


def actualizar_datos_al_agregar_materia_trabajo_final(parametros, materia):
    index = -1
    codigo = materia.codigo
    for i, materia_tp in enumerate(parametros.materia_trabajo_final):
        if materia_tp.codigo == materia.codigo:
            index = i
        if codigo in materia_tp.correlativas:
            materia_tp.correlativas.remove(codigo)

    if index >= 0:
        parametros.materia_trabajo_final.pop(index)


def actualizar_datos_al_agregar_materia_con_curso(parametros, materia, franjas_curso, franjas_cuatrimestre):
    ocupar_franjas_del_curso(franjas_curso, franjas_cuatrimestre)

    if materia.codigo in parametros.materias_incompatibles:
        for cod_incompatible in parametros.materias_incompatibles[materia.codigo]:
            parametros.quitar_materia_por_codigo(cod_incompatible, False)

    parametros.actualizar_creditos_tematicas_electivas(materia)
    parametros.quitar_materia_por_codigo(materia.codigo, True)


def ocupar_franjas_del_curso(franjas_curso, franjas_cuatrimestre):
    for dia in franjas_curso:
        for franja_curso in franjas_curso[dia]:
            franjas_cuatrimestre[dia][franja_curso - 1] = True
