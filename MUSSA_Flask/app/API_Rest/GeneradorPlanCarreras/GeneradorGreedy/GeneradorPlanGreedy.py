from app.API_Rest.GeneradorPlanCarreras.modelos.Materia import ELECTIVA, OBLIGATORIA

PLAN_NO_GENERADO = False
PLAN_GENERADO_CORRECTAMENTE = True

MAX_COMBINACIONES = 15 * 14 * 13 * 12 * 11  # 15 cursos posibles, 5 materias max

PARAMETROS_ACTUALES = "parametros_actuales"
CREDITOS_TOTALES = "creditos_totales"
FRANJAS_CUATRIMESTRE = "franjas_cuatrimestre"
MEDIAS_HORAS_CURSADA = "medias_horas_cursada"
MEDIAS_HORAS_EXTRAS = "medias_horas_extras"
MATERIAS_CUATRI_ACTUAL = "materias_cuatrimestre_actual"
CANT_OBLIGATORIAS_QUE_LIBERA = "cant_obligatorias_que_libera"
CANT_CREDITOS_TEMATICAS = "cant_creditos_tematicas"
CANT_CREDITOS_ELECTIVAS = "cant_creditos_electivas"


def generar_plan_greedy(parametros):
    creditos_totales = parametros.creditos_preacumulados
    while (not parametros.plan_esta_finalizado()):
        ultimo_cuatrimestre_generado = len(parametros.plan_generado)
        if ultimo_cuatrimestre_generado == parametros.max_cuatrimestres:
            return PLAN_NO_GENERADO

        materias_cuatrimestre_actual, creditos_totales = generar_cuatrimestre_actual(
            parametros, creditos_totales, ultimo_cuatrimestre_generado
        )

        if not materias_cuatrimestre_actual:
            return PLAN_NO_GENERADO

        parametros.plan_generado.append(materias_cuatrimestre_actual)

    return PLAN_GENERADO_CORRECTAMENTE

def calcular_combinaciones(parametros, materias_disponibles):
    combinaciones = len(materias_disponibles)
    for i in range(1, parametros.max_cant_materias_por_cuatrimestre):
        combinaciones = combinaciones * (len(materias_disponibles) - i)
    return combinaciones

def generar_cuatrimestre_actual(parametros, creditos_totales, ultimo_cuatrimestre_generado):
    materias_disponibles = parametros.obtener_materias_disponibles(creditos_totales, ultimo_cuatrimestre_generado)

    combinaciones = calcular_combinaciones(parametros, materias_disponibles)

    posibles_combinaciones = [generar_combinacion_base(parametros, creditos_totales)]

    agregar_segunda_parte_del_trabajo_final_consecutiva_a_la_primera_parte(parametros, posibles_combinaciones[0])

    generar_todas_las_combinaciones_posibles = (combinaciones < MAX_COMBINACIONES)
    mejor_combinacion = obtener_combinacion_materias_cuatrimestre(materias_disponibles, posibles_combinaciones,
                                                                  generar_todas_las_combinaciones_posibles)

    if not mejor_combinacion:
        return {}, creditos_totales

    parametros.actualizar_datos_con_parametros_seleccionados(mejor_combinacion[PARAMETROS_ACTUALES])
    return mejor_combinacion[MATERIAS_CUATRI_ACTUAL], mejor_combinacion[CREDITOS_TOTALES]


def generar_combinacion_base(parametros, creditos_totales):
    return {
        PARAMETROS_ACTUALES: parametros.copia_profunda(),
        FRANJAS_CUATRIMESTRE: parametros.generar_lista_franjas_limpia(),
        MEDIAS_HORAS_CURSADA: 0,
        MEDIAS_HORAS_EXTRAS: 0,
        CREDITOS_TOTALES: creditos_totales,
        CANT_OBLIGATORIAS_QUE_LIBERA: 0,
        CANT_CREDITOS_TEMATICAS: 0,
        CANT_CREDITOS_ELECTIVAS: 0,
        MATERIAS_CUATRI_ACTUAL: {}
    }


def agregar_segunda_parte_del_trabajo_final_consecutiva_a_la_primera_parte(parametros, combinacion_actual):
    # Si el tp o tesis fue agregado el cuatrimestre anterior, se lo agrega para este cuatrimestre
    if len(parametros.materia_trabajo_final) == 1:
        id_parte_a = parametros.materia_trabajo_final[0].id_materia  # es el mismo id que la parte b
        if id_parte_a in parametros.plan_generado[-1]:
            materia_tp = parametros.materia_trabajo_final[0]
            agregar_materia_a_combinacion_actualizar_creditos_y_horas(combinacion_actual, materia_tp)


def obtener_combinacion_materias_cuatrimestre(materias_disponibles, posibles_combinaciones,
                                              generar_todas_las_combinaciones_posibles):
    """
    Se obtiene la combinación para el cuatrimestre actual.

    - Si el parámetro "generar_todas_las_combinaciones_posibles" es True, entonces se generan todas
    las combinaciones válidas de las materias disponibles y se elige la mejor.

    - Si es False, entonces se colocan las materias disponibles ordenadas por prioridad y se las agrega
    una a una mientras que la combinación sea válida. Cuando no se pueden agregar más materias porque
    el cuatrimestre está completo o no hay disponibles, se devuelve esa cobinación como la mejor. En este
    caso solo se genera una única combinación.
    """
    mejor_combinacion = None

    for index, grupo_materia in enumerate(materias_disponibles):
        materia, curso = grupo_materia
        nuevas_posibles_combinaciones = []

        for combinacion in posibles_combinaciones:

            nueva_combinacion = copiar_combinacion(
                combinacion) if generar_todas_las_combinaciones_posibles else combinacion

            parametros = nueva_combinacion[PARAMETROS_ACTUALES]

            # Si el cuatrimestre esta completo en cantidad de materias, cierro el cuatrimestre
            if combinacion_esta_completa(parametros, nueva_combinacion):
                if not generar_todas_las_combinaciones_posibles:
                    return nueva_combinacion
                else:
                    break

            franjas_curso = []
            medias_horas_cursada = 0
            if curso:
                franjas_curso, medias_horas_cursada = curso.obtener_franjas_curso(), curso.medias_horas_cursada

            if not es_posible_agregar_materia_y_curso(materia, franjas_curso, medias_horas_cursada, nueva_combinacion):
                continue

            agregar_materia_a_combinacion_actualizar_creditos_y_horas(nueva_combinacion, materia, curso, franjas_curso,
                                                                      medias_horas_cursada)

            if generar_todas_las_combinaciones_posibles:
                nuevas_posibles_combinaciones.append(nueva_combinacion)

        if generar_todas_las_combinaciones_posibles:
            for combinacion in nuevas_posibles_combinaciones:
                posibles_combinaciones.append(combinacion)

            for i in range(len(posibles_combinaciones) - 1, -1, -1):
                combinacion = posibles_combinaciones.pop()
                if combinacion_esta_completa(combinacion[PARAMETROS_ACTUALES], combinacion):
                    mejor_combinacion = obtener_mejor_combinacion(mejor_combinacion, combinacion)
                else:
                    posibles_combinaciones.insert(0, combinacion)

    if not mejor_combinacion:
        for i in range(len(posibles_combinaciones)):
            mejor_combinacion = obtener_mejor_combinacion(mejor_combinacion, posibles_combinaciones.pop())

    return mejor_combinacion


def agregar_materia_a_combinacion_actualizar_creditos_y_horas(combinacion_actual, materia, curso=None, franjas_curso=[],
                                                              horas_cursada=0):
    parametros = combinacion_actual[PARAMETROS_ACTUALES]

    combinacion_actual[CREDITOS_TOTALES] += materia.creditos
    combinacion_actual[MEDIAS_HORAS_CURSADA] += horas_cursada
    combinacion_actual[MEDIAS_HORAS_EXTRAS] += materia.medias_horas_extras_cursada

    if materia.tipo == ELECTIVA:
        combinacion_actual[CANT_CREDITOS_ELECTIVAS] += materia.creditos
        combinacion_actual[CANT_CREDITOS_TEMATICAS] += parametros.calcular_creditos_aportados_tematicas(materia)

    if materia.id_materia in parametros.plan:
        for id_correlativa_liberada in parametros.plan[materia.id_materia]:
            if parametros.materias[id_correlativa_liberada].tipo == OBLIGATORIA:
                combinacion_actual[CANT_OBLIGATORIAS_QUE_LIBERA] += 1

    agregar_materia_y_actualizar_creditos(materia, curso, franjas_curso, parametros,
                                          combinacion_actual[MATERIAS_CUATRI_ACTUAL],
                                          combinacion_actual[FRANJAS_CUATRIMESTRE])


def combinacion_esta_completa(parametros, combinacion):
    return (parametros.max_cant_materias_por_cuatrimestre == combinacion[MATERIAS_CUATRI_ACTUAL] or
            parametros.max_horas_extras == combinacion[MEDIAS_HORAS_EXTRAS] or
            parametros.max_horas_cursada == combinacion[MEDIAS_HORAS_CURSADA])


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
    for id_materia in combinacion[MATERIAS_CUATRI_ACTUAL]:
        materias[id_materia] = combinacion[MATERIAS_CUATRI_ACTUAL][id_materia]

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


def es_posible_agregar_materia_y_curso(materia, franjas_curso, horas_cursada, combinacion):
    horas_extras_del_curso = materia.medias_horas_extras_cursada
    franjas_cuatrimestre = combinacion[FRANJAS_CUATRIMESTRE]
    medias_horas_cursada = combinacion[MEDIAS_HORAS_CURSADA]
    medias_horas_extras = combinacion[MEDIAS_HORAS_EXTRAS]
    parametros = combinacion[PARAMETROS_ACTUALES]
    materias_cuatrimestre_actual = combinacion[MATERIAS_CUATRI_ACTUAL]

    # Verifico que no se haya agregado ya la materia en este cuatrimestre y este sea otro de los horarios
    # disponibles para el mismo código de materia
    if (materia.id_materia in materias_cuatrimestre_actual):
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
    if materia.id_materia in parametros.materias_incompatibles:
        for id_incompatible in parametros.materias_incompatibles[materia.id_materia]:
            if parametros.se_encuentra_materia_en_plan_generado(id_incompatible, materias_cuatrimestre_actual):
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
    # No hay problema con las materias de trabajo final ya que si bien tienen el mismo id SIEMPRE estaran
    # en cuatrimestres separados
    materias_cuatrimestre_actual[materia.id_materia] = curso.id_curso if curso else -1

    if not curso:
        actualizar_datos_al_agregar_materia_trabajo_final(parametros, materia)
    else:
        actualizar_datos_al_agregar_materia_con_curso(parametros, materia, franjas_curso, franjas_cuatrimestre)


def actualizar_datos_al_agregar_materia_trabajo_final(parametros, materia):
    index = -1
    for i, materia_tp in enumerate(parametros.materia_trabajo_final):
        if materia_tp.codigo == materia.codigo:
            index = i
        if materia.id_materia in materia_tp.correlativas:
            materia_tp.correlativas.remove(materia.id_materia)

    if index >= 0:
        parametros.materia_trabajo_final.pop(index)


def actualizar_datos_al_agregar_materia_con_curso(parametros, materia, franjas_curso, franjas_cuatrimestre):
    ocupar_franjas_del_curso(franjas_curso, franjas_cuatrimestre)

    if materia.id_materia in parametros.materias_incompatibles:
        for id_incompatible in parametros.materias_incompatibles[materia.id_materia]:
            parametros.quitar_materia_por_id(id_incompatible, False)

    parametros.actualizar_creditos_tematicas_electivas(materia)
    parametros.quitar_materia_por_id(materia.id_materia, True)


def ocupar_franjas_del_curso(franjas_curso, franjas_cuatrimestre):
    for dia in franjas_curso:
        for franja_curso in franjas_curso[dia]:
            franjas_cuatrimestre[dia][franja_curso - 1] = True
