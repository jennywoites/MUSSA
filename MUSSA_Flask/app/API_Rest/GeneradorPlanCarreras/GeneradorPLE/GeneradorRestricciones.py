from app.API_Rest.GeneradorPlanCarreras.Constantes import *
from app.API_Rest.GeneradorPlanCarreras.my_utils import get_str_cuatrimestre, es_horario_valido_para_el_cuatrimestre


def generar_restriccion_la_materia_debe_cursarse_en_unico_cuatrimestre(arch, parametros):
    arch.write(
        "# La materia i se debe cursar en un unico cuatrimestre. Ademas, si es obligatoria, debe cursarse si o si." + ENTER + ENTER)
    for id_materia in parametros.materias:
        ecuacion = "prob += ("
        for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
            if cuatrimestre > 1:
                ecuacion += " + "
            variable = "Y_{}_{}".format(id_materia, get_str_cuatrimestre(cuatrimestre))
            ecuacion += variable

        ecuacion_complementaria = ecuacion
        ecuacion += " <= 1)"
        ecuacion_complementaria += " >= 1)"

        if parametros.materias[id_materia].tipo == OBLIGATORIA:
            arch.write(ecuacion_complementaria + ENTER)
        arch.write(ecuacion + ENTER)

        arch.write(ENTER)
    arch.write(ENTER)


def generar_restriccion_valor_cuatrimestre_en_que_se_cursa_la_materia(arch, parametros):
    arch.write("# Numero de cuatrimestre en que es cursada la materia" + ENTER + ENTER)
    for id_materia in parametros.plan:
        ecuacion = "prob += ("
        for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
            if cuatrimestre > 1:
                ecuacion += " + "
            variable = "Y_{}_{}".format(id_materia, get_str_cuatrimestre(cuatrimestre))
            ecuacion += "{}*{}".format(cuatrimestre, variable)

        variable_c_materia = "C{}".format(id_materia)
        ecuacion_complementaria = ecuacion
        ecuacion += "<= {})".format(variable_c_materia)
        ecuacion_complementaria += ">= {})".format(variable_c_materia)

        arch.write(ecuacion + ENTER)
        arch.write(ecuacion_complementaria + ENTER)
        arch.write(ENTER)
    arch.write(ENTER)


def generar_restriccion_cuatrimestre_minimo_en_que_se_puede_cursar_la_materia(arch, parametros):
    if not parametros.cuatrimestre_minimo_para_materia:
        return

    arch.write("# Valor minimo para el cuatrimestre de una materia debido a que"
               "el final de una correlativa se encuentra pendiente y sera aprobado"
               "en ese cuatrimestre minimo" + ENTER + ENTER)
    for id_materia in parametros.cuatrimestre_minimo_para_materia:
        variable_c_materia = "C{}".format(id_materia)

        # El cuatrimestre minimo es el siguiente de cuando estara aprobada la materia
        cuatrimestre_min = parametros.cuatrimestre_minimo_para_materia[id_materia] + 1

        ecuacion = "prob += ({} >= {})".format(variable_c_materia, cuatrimestre_min)
        arch.write(ecuacion + ENTER + ENTER)
    arch.write(ENTER)


def generar_restriccion_correlativas(arch, parametros):
    arch.write("# Los cuatrimestres de las correlativas deben ser menores (cuando la materia se cursa)" + ENTER + ENTER)
    for id_materia in parametros.plan:
        correlativas = parametros.plan[id_materia]
        if not correlativas:
            continue

        materia = parametros.materias[id_materia]
        for id_m_correlativa in correlativas:
            if materia.tipo == OBLIGATORIA:
                escribir_ecuacion_correlativa_depende_de_obligatoria(arch, parametros, id_materia, id_m_correlativa)
            else:
                escribir_ecuacion_correlativa_depende_de_electiva(arch, parametros, id_materia, id_m_correlativa)

    arch.write(ENTER + ENTER)


def escribir_ecuacion_correlativa_depende_de_obligatoria(arch, parametros, id_materia, id_m_correlativa):
    cuatri_materia = "C{}".format(id_materia)
    cuatri_correlativa = "C{}".format(id_m_correlativa)

    if parametros.materias[id_m_correlativa].tipo == OBLIGATORIA:
        ecuacion = "prob += ({} >= {} + 1)".format(cuatri_correlativa, cuatri_materia)
        arch.write(ecuacion + ENTER)
    else:
        sumatoria = obtener_sumatoria_Y_cuatrimestres_para_materia(parametros, parametros.materias[id_m_correlativa])
        ajuste_electiva_no_cursada = "{} * (1 - ({}))".format(INFINITO, sumatoria)
        ecuacion = "prob += ({} + {} >= {} + 1)".format(cuatri_correlativa, ajuste_electiva_no_cursada, cuatri_materia)
        arch.write(ecuacion + ENTER)


def obtener_sumatoria_Y_cuatrimestres_para_materia(parametros, materia):
    sumatoria = ""
    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        variable = "Y_{}_{}".format(materia.id_materia, get_str_cuatrimestre(cuatrimestre))
        sumatoria += variable + " + "
    return sumatoria[:-3]


def escribir_ecuacion_correlativa_depende_de_electiva(arch, parametros, id_materia, id_m_correlativa):
    cuatri_materia = "C{}".format(id_materia)
    cuatri_correlativa = "C{}".format(id_m_correlativa)

    # Si la materia electiva primera se cursa, entonces el cuatrimestre debe ser mayor
    sumatoria_correlativa = obtener_sumatoria_Y_cuatrimestres_para_materia(parametros,
                                                                           parametros.materias[id_m_correlativa])
    ajuste_electiva_no_cursada = "{} * (1 - ({}))".format(INFINITO, sumatoria_correlativa)
    ec_correlativa = "{} + {}".format(cuatri_correlativa, ajuste_electiva_no_cursada)

    sumatoria_primaria = obtener_sumatoria_Y_cuatrimestres_para_materia(parametros, parametros.materias[id_materia])
    ajuste_electiva_primaria_no_cursada = "(1 * ({}))".format(sumatoria_primaria)
    ec_primer_materia = "{} + {}".format(cuatri_materia, ajuste_electiva_primaria_no_cursada)

    ecuacion = "prob += ({} >= {})".format(ec_correlativa, ec_primer_materia)
    arch.write(ecuacion + ENTER)

    # Si la materia electiva primera no se cursa, entonces no se puede cursar la que la tiene como correlativa
    ecuacion = "prob += ({} <= {} * ({}))".format(cuatri_correlativa, INFINITO, sumatoria_primaria)
    arch.write(ecuacion + ENTER)


def generar_restriccion_maxima_cant_materias_por_cuatrimestre(arch, parametros):
    arch.write("# La cantidad de materias por cuatrimestre no puede superar un valor maximo" + ENTER + ENTER)
    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        ecuacion = "prob += ("
        for id_materia in parametros.plan:
            variable = "Y_{}_{}".format(id_materia, get_str_cuatrimestre(cuatrimestre))
            ecuacion += variable + " + "

        if not parametros.materia_trabajo_final:
            ecuacion = ecuacion[:-2]
        else:
            for materia in parametros.materia_trabajo_final:
                variable = "Y_TP_FINAL_{}_{}_{}".format(materia.id_materia, materia.codigo,
                                                        get_str_cuatrimestre(cuatrimestre))
                ecuacion += variable + " + "
            ecuacion = ecuacion[:-2]

        ecuacion += " <= {})".format(parametros.max_cant_materias_por_cuatrimestre)
        arch.write(ecuacion + ENTER)

    arch.write(ENTER + ENTER)


def generar_restriccion_maximo_cuatrimestres_para_func_objetivo(arch, parametros):
    arch.write("#TOTAL_CUATRIMESTRES es el maximo de los Ci de las materias"
               "y de lo C_TP_FINAL_i de las materias de trabajo final" + ENTER + ENTER)

    arch.write("prob += (TOTAL_CUATRIMESTRES >= 0)" + ENTER + ENTER)

    for id_materia in parametros.plan:
        var_materia = "C{}".format(id_materia)
        arch.write("prob += ({} <= TOTAL_CUATRIMESTRES)".format(var_materia) + ENTER)
        arch.write("prob += (-{} <= TOTAL_CUATRIMESTRES)".format(var_materia) + ENTER)
        arch.write(ENTER)

    for materia in parametros.materia_trabajo_final:
        var_materia = "C_TP_FINAL_{}_{}".format(materia.id_materia, materia.codigo)
        arch.write("prob += ({} <= TOTAL_CUATRIMESTRES)".format(var_materia) + ENTER)
        arch.write("prob += (-{} <= TOTAL_CUATRIMESTRES)".format(var_materia) + ENTER)
        arch.write(ENTER)

    arch.write(ENTER)


def generar_restriccion_calculo_creditos_obtenidos_por_cuatrimestre(arch, parametros):
    arch.write("# Calculo de creditos al terminar cada cuatrimestre" + ENTER + ENTER)

    for i in range(1, parametros.max_cuatrimestres + 1):
        ecuacion = "prob += ("
        for id_materia in parametros.plan:
            materia = parametros.materias[id_materia]
            variable_Y = "Y_{}_{}".format(id_materia, get_str_cuatrimestre(i))
            ecuacion += "{}*{} + ".format(materia.creditos, variable_Y)

        if not parametros.materia_trabajo_final:
            ecuacion = ecuacion[:-2]  # elimino el ultimo + agregado
        else:
            for materia in parametros.materia_trabajo_final:
                variable_Y = "Y_TP_FINAL_{}_{}_{}".format(materia.id_materia, materia.codigo, get_str_cuatrimestre(i))
                ecuacion += "{}*{} + ".format(materia.creditos, variable_Y)
            ecuacion = ecuacion[:-2]  # elimino el ultimo + agregado

        if i > 1:
            ecuacion += "+ CRED{}".format(get_str_cuatrimestre(i - 1))
        else:
            ecuacion += "+ {}".format(parametros.creditos_preacumulados)

        arch.write(ecuacion + " <= CRED{})".format(get_str_cuatrimestre(i)) + ENTER)
        arch.write(ecuacion + " >= CRED{})".format(get_str_cuatrimestre(i)) + ENTER)
    arch.write(ENTER)


def generar_restriccion_maxima_cantidad_horas_extra_cursada(arch, parametros):
    arch.write("# Maxima cantidad de horas extra cursada. El calculo es por una semana en medias"
               "horas de cursada, pero es la misma restriccion para todo el cuatrimestre" + ENTER + ENTER)

    for i in range(1, parametros.max_cuatrimestres + 1):
        ecuacion = "prob += ("
        for id_materia in parametros.plan:
            materia = parametros.materias[id_materia]
            variable_Y = "Y_{}_{}".format(id_materia, get_str_cuatrimestre(i))
            ecuacion += "{}*{} + ".format(materia.medias_horas_extras_cursada, variable_Y)

        if not parametros.materia_trabajo_final:
            ecuacion = ecuacion[:-2]  # elimino el ultimo + agregado
        else:
            for materia in parametros.materia_trabajo_final:
                variable_Y = "Y_TP_FINAL_{}_{}_{}".format(materia.id_materia, materia.codigo, get_str_cuatrimestre(i))
                ecuacion += "{}*{} + ".format(materia.medias_horas_extras_cursada, variable_Y)
            ecuacion = ecuacion[:-2]  # elimino el ultimo + agregado

        arch.write(ecuacion + " <= {})".format(parametros.max_horas_extras) + ENTER)
    arch.write(ENTER)


def generar_restriccion_creditos_minimos_ya_obtenidos_para_cursar(arch, parametros):
    arch.write(
        "# Restricciones sobre aquellas materias que requieren creditos minimos para poder cursar" + ENTER + ENTER)
    for id_materia in parametros.plan:
        materia = parametros.materias[id_materia]
        if materia.creditos_minimos_aprobados == 0:
            continue
        for i in range(1, parametros.max_cuatrimestres + 1):
            creditos = "CRED{}".format(get_str_cuatrimestre(i - 1)) if i > 1 else parametros.creditos_preacumulados
            var_Y = "Y_{}_{}".format(id_materia, get_str_cuatrimestre(i))
            arch.write("prob += ({}*{} <= {})".format(materia.creditos_minimos_aprobados, var_Y, creditos) + ENTER)
        arch.write(ENTER)
    arch.write(ENTER)


def generar_restriccion_si_se_elige_un_curso_se_cursa_su_horario_completo(arch, parametros):
    arch.write(
        "#Si la materia se cursa en ese cuatrimestre en ese curso en particular, entonces se deben cursar todos los horarios del mismo" + ENTER + ENTER)
    for cuatri in range(1, parametros.max_cuatrimestres + 1):
        for id_materia in parametros.horarios:
            cursos = parametros.horarios[id_materia]
            for curso in cursos:
                H = "H_{}_{}_{}".format(id_materia, curso.id_curso, get_str_cuatrimestre(cuatri))

                if not es_horario_valido_para_el_cuatrimestre(parametros, curso, cuatri):
                    continue

                for c_horario in curso.horarios:
                    dia = c_horario.dia
                    franjas = c_horario.get_franjas_utilizadas()
                    for franja in franjas:
                        R = "R_{}_{}_{}_{}_{}".format(id_materia, curso.id_curso, dia, franja,
                                                      get_str_cuatrimestre(cuatri))
                        arch.write("prob += ({} <= {})".format(H, R) + ENTER)
                        arch.write("prob += ({} >= {})".format(H, R) + ENTER)
    arch.write(ENTER)


def generar_restriccion_solo_puede_cursarse_en_un_lugar_al_mismo_tiempo(arch, parametros):
    arch.write(
        "#No hay giratiempos: Solo puede cursarse una materia en un unico curso en el mismo horario" + ENTER + ENTER)
    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        for dia in parametros.dias:
            for franja in range(parametros.franja_minima, parametros.franja_maxima + 1):
                ec_suma = ""
                for id_materia in parametros.horarios:
                    for curso in parametros.horarios[id_materia]:
                        if not es_horario_valido_para_el_cuatrimestre(parametros, curso, cuatrimestre):
                            continue

                        if es_horario_restriccion_valido(curso, dia, franja):
                            ec_suma += "R_{}_{}_{}_{}_{} + ".format(id_materia, curso.id_curso, dia, franja,
                                                                    get_str_cuatrimestre(cuatrimestre))
                ec_suma = ec_suma[:-3]
                if not ec_suma:
                    ec_suma = "0"
                ecuacion = "prob += ({}_{}_{} {} ".format(dia, franja, get_str_cuatrimestre(cuatrimestre),
                                                          '{}') + ec_suma + ")"
                arch.write(ecuacion.format("<=") + ENTER)
                arch.write(ecuacion.format(">=") + ENTER)
    arch.write(ENTER)


def es_horario_restriccion_valido(curso, dia, franja):
    for c_horario in curso.horarios:
        c_dia = c_horario.dia
        franjas = c_horario.get_franjas_utilizadas()
        if dia == c_dia and franja in franjas:
            return True
    return False


def generar_restriccion_si_la_materia_no_se_cursa_en_ese_cuatrimestre_no_se_cursa_ninguno_de_sus_cursos(arch,
                                                                                                        parametros):
    arch.write(
        "# Si la materia no se cursa ese cuatrimestre, entonces no puede cursarse en ninguno de los cursos de ese cuatrimestre" + ENTER + ENTER)
    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        for id_materia in parametros.horarios:
            for curso in parametros.horarios[id_materia]:
                Y = "Y_{}_{}".format(id_materia, get_str_cuatrimestre(cuatrimestre))
                R = "H_{}_{}_{}".format(id_materia, curso.id_curso, get_str_cuatrimestre(cuatrimestre))
                ecuacion = "prob += ({} >= {})".format(Y, R)
                arch.write(ecuacion + ENTER)
    arch.write(ENTER)


def generar_restriccion_la_materia_no_puede_cursarse_en_mas_de_un_curso(arch, parametros):
    arch.write("# La materia no puede cursarse en mas de un curso en el cuatrimestre" + ENTER + ENTER)
    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        for id_materia in parametros.horarios:
            ecuacion = ""
            for curso in parametros.horarios[id_materia]:
                ecuacion += "H_{}_{}_{} + ".format(id_materia, curso.id_curso, get_str_cuatrimestre(cuatrimestre))
            Y = "Y_{}_{}".format(id_materia, get_str_cuatrimestre(cuatrimestre))
            arch.write("prob += ({} <= {})".format(Y, ecuacion[:-3]) + ENTER)
            arch.write("prob += ({} >= {})".format(Y, ecuacion[:-3]) + ENTER)
    arch.write(ENTER)


def generar_restriccion_creditos_minimos_electivas(arch, parametros):
    if parametros.creditos_minimos_electivas == 0:
        return

    arch.write("#Se debe realizar un minimo de creditos de materias electivas" + ENTER + ENTER)
    ecuacion = "prob += ("
    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        for id_materia in parametros.materias:
            materia = parametros.materias[id_materia]
            if materia.tipo == OBLIGATORIA:
                continue
            Y = "Y_{}_{}".format(id_materia, get_str_cuatrimestre(cuatrimestre))
            ecuacion += Y + "*" + str(materia.creditos) + " + "

    ecuacion = ecuacion[:-3]

    # FIXME: Esto no anda por algun motivo. Solucion temporal, colocar que no supere los creditos en electivas por mas de 6
    # arch.write(ecuacion + " <= CREDITOS_ELECTIVAS)" + ENTER)
    # arch.write(ecuacion + " >= CREDITOS_ELECTIVAS)" + ENTER)
    # arch.write("prob += (CREDITOS_ELECTIVAS >= " + str(parametros.creditos_minimos_electivas) + ")" + ENTER + ENTER)

    CREDITOS_UNA_MATERIA_EXTRA = 6
    arch.write(ecuacion + " >= " + str(parametros.creditos_minimos_electivas) + ")" + ENTER + ENTER)
    arch.write(ecuacion + " <= " + str(parametros.creditos_minimos_electivas + CREDITOS_UNA_MATERIA_EXTRA) + ")"
               + ENTER + ENTER)


def generar_restriccion_creditos_minimos_por_tematica(arch, parametros):
    if not parametros.creditos_minimos_tematicas:
        return

    arch.write("#Se debe realizar un minimo de creditos de materias electivas"
               "con diferentes tematicas" + ENTER + ENTER)
    for tematica in parametros.creditos_minimos_tematicas:
        ecuacion = "prob += ("
        for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
            for id_materia in parametros.materias:
                materia = parametros.materias[id_materia]
                if materia.tipo == OBLIGATORIA or not tematica in materia.tematicas_principales:
                    continue
                Y = "Y_{}_{}".format(id_materia, get_str_cuatrimestre(cuatrimestre))
                ecuacion += Y + "*" + str(materia.creditos) + " + "

        ecuacion = ecuacion[:-3]
        arch.write(ecuacion + " >= " + str(parametros.creditos_minimos_tematicas[tematica]) + ")" + ENTER + ENTER)

    arch.write(ENTER)


def generar_restriccion_no_todos_los_cursos_se_dictan_ambos_cuatrimestres(arch, parametros):
    arch.write("# No todos los cursos se dictan ambos cuatrimestres" + ENTER + ENTER)
    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        for id_materia in parametros.horarios:
            for curso in parametros.horarios[id_materia]:
                if es_horario_valido_para_el_cuatrimestre(parametros, curso, cuatrimestre):
                    continue

                variable = "H_{}_{}_{}".format(id_materia, curso.id_curso, get_str_cuatrimestre(cuatrimestre))
                arch.write("prob += ({} <= 0)".format(variable) + ENTER)
                arch.write("prob += ({} >= 0)".format(variable) + ENTER)
    arch.write(ENTER)


def generar_restriccion_horarios_cursos(arch, parametros):
    generar_restriccion_si_se_elige_un_curso_se_cursa_su_horario_completo(arch, parametros)
    generar_restriccion_solo_puede_cursarse_en_un_lugar_al_mismo_tiempo(arch, parametros)
    generar_restriccion_si_la_materia_no_se_cursa_en_ese_cuatrimestre_no_se_cursa_ninguno_de_sus_cursos(arch,
                                                                                                        parametros)
    generar_restriccion_la_materia_no_puede_cursarse_en_mas_de_un_curso(arch, parametros)
    generar_restriccion_no_todos_los_cursos_se_dictan_ambos_cuatrimestres(arch, parametros)


def generar_restriccion_el_trabajo_debe_cursarse_en_unico_cuatrimestre(arch, parametros):
    arch.write("# La El trabajo final debe cursar (cada una de sus partes) "
               "en un unico cuatrimestre. Ademas, es obligatorio" + ENTER + ENTER)
    for materia in parametros.materia_trabajo_final:
        ecuacion = "prob += ("
        for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
            if cuatrimestre > 1:
                ecuacion += " + "
            variable = "Y_TP_FINAL_{}_{}_{}".format(materia.id_materia, materia.codigo,
                                                    get_str_cuatrimestre(cuatrimestre))
            ecuacion += variable

        arch.write(ecuacion + " <= 1)" + ENTER)
        arch.write(ecuacion + " >= 1)" + ENTER)
        arch.write(ENTER)

    arch.write(ENTER)


def generar_restriccion_valor_cuatrimestre_en_que_se_cursa_el_trabajo_final(arch, parametros):
    arch.write("# Numero de cuatrimestre en que son "
               "cursadas las partes del trabajo final" + ENTER + ENTER)
    for materia in parametros.materia_trabajo_final:
        ecuacion = "prob += ("
        for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
            if cuatrimestre > 1:
                ecuacion += " + "
            variable = "Y_TP_FINAL_{}_{}_{}".format(materia.id_materia, materia.codigo,
                                                    get_str_cuatrimestre(cuatrimestre))
            ecuacion += "{}*{}".format(cuatrimestre, variable)

        variable_c_materia = "C_TP_FINAL_{}_{}".format(materia.id_materia, materia.codigo)
        ecuacion_complementaria = ecuacion
        ecuacion += "<= {})".format(variable_c_materia)
        ecuacion_complementaria += ">= {})".format(variable_c_materia)

        arch.write(ecuacion + ENTER)
        arch.write(ecuacion_complementaria + ENTER)
        arch.write(ENTER)
    arch.write(ENTER)


def generar_restriccion_creditos_minimos_ya_obtenidos_para_cursar_el_trabajo_final(arch, parametros):
    arch.write("# Restriccion de creditos minimos para el trabajo final" + ENTER + ENTER)
    for materia in parametros.materia_trabajo_final:
        if materia.creditos_minimos_aprobados == 0:
            continue
        for i in range(1, parametros.max_cuatrimestres + 1):
            creditos = "CRED{}".format(get_str_cuatrimestre(i - 1)) if i > 1 else parametros.creditos_preacumulados
            variable_Y = "Y_TP_FINAL_{}_{}_{}".format(materia.id_materia, materia.codigo,
                                                      get_str_cuatrimestre(get_str_cuatrimestre(i)))
            arch.write("prob += ({}*{} <= {})".format(materia.creditos_minimos_aprobados, variable_Y, creditos) + ENTER)
        arch.write(ENTER)
    arch.write(ENTER)


def generar_restriccion_las_partes_del_tp_se_deben_hacer_en_cuatrimestres_consecutivos(arch, parametros):
    arch.write("# Las partes del tp se deben hacer en cuatrimestres consecutivos" + ENTER + ENTER)

    for i in range(len(parametros.materia_trabajo_final) - 1):
        materia_anterior = parametros.materia_trabajo_final[i]
        materia_actual = parametros.materia_trabajo_final[i + 1]

        variable_c_materia_anterior = "C_TP_FINAL_{}_{}".format(materia_anterior.id_materia, materia_anterior.codigo)
        variable_c_materia_actual = "C_TP_FINAL_{}_{}".format(materia_actual.id_materia, materia_actual.codigo)

        ecuacion = "prob += ({} + 1 {} {})".format(variable_c_materia_anterior, "{}", variable_c_materia_actual)

        arch.write(ecuacion.format("<=") + ENTER)
        arch.write(ecuacion.format(">=") + ENTER)
        arch.write(ENTER)
    arch.write(ENTER)


def generar_restriccion_materias_incompatibles(arch, parametros):
    arch.write("# Si una materia es incompatible con otra, solo puede "
               "cursarse una de ellas" + ENTER + ENTER)
    for id_materia in parametros.materias_incompatibles:
        incompatibles = parametros.materias_incompatibles[id_materia] + [id_materia]
        ecuacion = "prob += ("
        for id_incompatible in incompatibles:
            for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
                variable = "Y_{}_{}".format(id_incompatible, get_str_cuatrimestre(cuatrimestre))
                ecuacion += variable + " + "

        ecuacion = ecuacion[:-3]
        ecuacion += " <= 1)"
        arch.write(ecuacion + ENTER)
        arch.write(ENTER)
    arch.write(ENTER)


def generar_restriccion_trabajo_final(arch, parametros):
    if not parametros.materia_trabajo_final:
        return

    generar_restriccion_el_trabajo_debe_cursarse_en_unico_cuatrimestre(arch, parametros)
    generar_restriccion_valor_cuatrimestre_en_que_se_cursa_el_trabajo_final(arch, parametros)
    generar_restriccion_creditos_minimos_ya_obtenidos_para_cursar_el_trabajo_final(arch, parametros)
    generar_restriccion_las_partes_del_tp_se_deben_hacer_en_cuatrimestres_consecutivos(arch, parametros)


def generar_restricciones(arch, parametros):
    generar_restriccion_la_materia_debe_cursarse_en_unico_cuatrimestre(arch, parametros)
    generar_restriccion_valor_cuatrimestre_en_que_se_cursa_la_materia(arch, parametros)
    generar_restriccion_correlativas(arch, parametros)
    generar_restriccion_calculo_creditos_obtenidos_por_cuatrimestre(arch, parametros)
    generar_restriccion_creditos_minimos_ya_obtenidos_para_cursar(arch, parametros)
    generar_restriccion_maxima_cant_materias_por_cuatrimestre(arch, parametros)
    generar_restriccion_maximo_cuatrimestres_para_func_objetivo(arch, parametros)
    generar_restriccion_horarios_cursos(arch, parametros)
    generar_restriccion_creditos_minimos_electivas(arch, parametros)
    generar_restriccion_trabajo_final(arch, parametros)
    generar_restriccion_materias_incompatibles(arch, parametros)
    generar_restriccion_cuatrimestre_minimo_en_que_se_puede_cursar_la_materia(arch, parametros)
    generar_restriccion_maxima_cantidad_horas_extra_cursada(arch, parametros)
