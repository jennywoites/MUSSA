from app.API_Rest.GeneradorPlanCarreras.modelos.Materia import ELECTIVA

PLAN_NO_GENERADO = False
PLAN_GENERADO_CORRECTAMENTE = True


def generar_plan_greedy(parametros):
    planes_pendientes = []
    resultado = generar_plan_greedy_recursivo(planes_pendientes, parametros, [], {}, [], 0, 0, 0)

    if resultado == PLAN_GENERADO_CORRECTAMENTE:
        return PLAN_GENERADO_CORRECTAMENTE

    total_planes = 0
    while (planes_pendientes):
        total_planes += 1
        plan_nuevo = planes_pendientes.pop(0)

        parametros_actuales = plan_nuevo["parametros"]
        materias_disponibles = plan_nuevo["materias_disponibles"]
        materias_cuatrimestre_actual = plan_nuevo["materias_cuatrimestre_actual"]
        franjas_cuatrimestre = plan_nuevo["franjas_cuatrimestre"]
        creditos_totales = plan_nuevo["creditos_totales"]
        medias_horas_cursada = plan_nuevo["medias_horas_cursada"]
        medias_horas_extras = plan_nuevo["medias_horas_extras"]

        resultado = generar_plan_greedy_recursivo(planes_pendientes, parametros_actuales, materias_disponibles,
                                                  materias_cuatrimestre_actual,
                                                  franjas_cuatrimestre, creditos_totales, medias_horas_cursada,
                                                  medias_horas_extras)

        if resultado == PLAN_GENERADO_CORRECTAMENTE:
            # actualizar el parametro a como esta actualmente
            return PLAN_GENERADO_CORRECTAMENTE

    return resultado


def generar_plan_greedy_recursivo(planes_pendientes, parametros, materias_disponibles, materias_cuatrimestre_actual,
                                  franjas_cuatrimestre,
                                  creditos_totales, medias_horas_cursada, medias_horas_extras):
    es_primera_vez = True
    while (not parametros.plan_esta_finalizado()):
        if len(parametros.plan_generado) == parametros.max_cuatrimestres:
            return PLAN_NO_GENERADO

        # Cuando no es el paso inicial debo reiniciar los datos. En el caso de que sea la
        # primer llamada del paso recursivo, debo iniciar los datos y por ello materias_disponibles
        # estará vacío.
        if not materias_disponibles or not es_primera_vez:
            materias_disponibles = parametros.obtener_materias_disponibles(creditos_totales)
            materias_cuatrimestre_actual = {}

        es_primera_vez = False

        if not materias_cuatrimestre_actual:
            franjas_cuatrimestre = parametros.generar_lista_franjas_limpia()
            medias_horas_cursada = 0
            medias_horas_extras = 0

        for index, grupo_materia in enumerate(materias_disponibles):
            materia, curso = grupo_materia
            # Si el cuatrimestre esta completo en cantidad de materias, cierro el cuatrimestre
            if (parametros.max_cant_materias_por_cuatrimestre == len(materias_cuatrimestre_actual) or
                        parametros.max_horas_extras == medias_horas_extras or
                        parametros.max_horas_cursada == medias_horas_cursada):
                break

            franjas_curso, horas_cursada = obtener_franjas_curso(curso) if curso else ([], 0)

            if not es_posible_agregar_materia_y_curso(materia, franjas_curso, horas_cursada,
                                                      materia.medias_horas_extras_cursada, franjas_cuatrimestre,
                                                      medias_horas_cursada,
                                                      medias_horas_extras, parametros, materias_cuatrimestre_actual):
                continue

            agregar_plan_sin_opcion_actual(planes_pendientes, parametros, materias_disponibles, index,
                                           materias_cuatrimestre_actual, franjas_cuatrimestre,
                                           creditos_totales, medias_horas_cursada, medias_horas_extras)

            creditos_totales += materia.creditos
            medias_horas_cursada += horas_cursada
            medias_horas_extras += materia.medias_horas_extras_cursada
            agregar_materia_y_actualizar_creditos(materia, curso, franjas_curso, parametros,
                                                  materias_cuatrimestre_actual, franjas_cuatrimestre)

        if materias_cuatrimestre_actual:
            parametros.plan_generado.append(materias_cuatrimestre_actual)
        else:
            return PLAN_NO_GENERADO

    return PLAN_GENERADO_CORRECTAMENTE


def agregar_plan_sin_opcion_actual(planes_pendientes, parametros, materias_disponibles, index_materia_ignorar,
                                   materias_cuatrimestre_actual, franjas_cuatrimestre,
                                   creditos_totales, medias_horas_cursada, medias_horas_extras):
    materias = []
    for index, grupo_materia in enumerate(materias_disponibles):
        if index <= index_materia_ignorar:
            continue
        materia, curso = grupo_materia
        copia_curso = curso.copia_profunda() if curso else None
        materias.append((materia.copia_profunda(), copia_curso))

    # No hay combinaciones nuevas para probar
    if not materias:
        return

    materias_cuatrimestre = {}
    for cod in materias_cuatrimestre_actual:
        materias_cuatrimestre[cod] = materias_cuatrimestre_actual[cod]

    planes_pendientes.append({
        "parametros": parametros.copia_profunda_datos_mas_relevantes(),
        "materias_disponibles": materias,
        "materias_cuatrimestre_actual": materias_cuatrimestre,
        "franjas_cuatrimestre": franjas_cuatrimestre,
        "creditos_totales": creditos_totales,
        "medias_horas_cursada": medias_horas_cursada,
        "medias_horas_extras": medias_horas_extras
    })


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


def obtener_franjas_curso(curso):
    franjas_totales = {}
    total_horas = 0
    for horario in curso.horarios:
        franjas = horario.get_franjas_utilizadas()
        franjas_dia = franjas_totales.get(horario.dia, [])
        for franja in franjas:
            franjas_dia.append(franja)
        franjas_totales[horario.dia] = franjas_dia
        total_horas += len(franjas_dia)

    return franjas_totales, total_horas


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
