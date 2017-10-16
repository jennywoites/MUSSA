from Constantes import *

from my_utils import get_str_cuatrimestre

def generar_restriccion_la_materia_debe_cursarse_en_unico_cuatrimestre(arch, parametros):
    materias = parametros.materias

    arch.write("# La materia i se debe cursar en un unico cuatrimestre. Ademas, si es obligatoria, debe cursarse si o si." + ENTER + ENTER)
    for materia in materias:
        ecuacion = "prob += ("
        for cuatrimestre in range(1,parametros.max_cuatrimestres + 1):
            if cuatrimestre > 1:
                ecuacion += " + "
            variable = "Y_{}_{}".format(materia, get_str_cuatrimestre(cuatrimestre))
            ecuacion += variable
        
        ecuacion_complementaria = ecuacion
        ecuacion += " <= 1)"
        ecuacion_complementaria += " >= 1)"

        if materias[materia].tipo == OBLIGATORIA:
            arch.write(ecuacion_complementaria + ENTER)
        arch.write(ecuacion + ENTER)

        arch.write(ENTER)
    arch.write(ENTER)


def generar_restriccion_valor_cuatrimestre_en_que_se_cursa_la_materia(arch, parametros):
    plan = parametros.plan

    arch.write("# Numero de cuatrimestre en que es cursada la materia" + ENTER + ENTER)
    for materia in plan:
        ecuacion = "prob += ("
        for cuatrimestre in range(1,parametros.max_cuatrimestres + 1):
            if cuatrimestre > 1:
                ecuacion += " + "
            variable = "Y_{}_{}".format(materia, get_str_cuatrimestre(cuatrimestre))
            ecuacion += "{}*{}".format(cuatrimestre,variable)
        
        variable_c_materia = "C{}".format(materia)
        ecuacion_complementaria = ecuacion
        ecuacion += "<= {})".format(variable_c_materia)
        ecuacion_complementaria += ">= {})".format(variable_c_materia)

        arch.write(ecuacion + ENTER)
        arch.write(ecuacion_complementaria + ENTER)
        arch.write(ENTER)
    arch.write(ENTER)


def generar_restriccion_correlativas(arch, parametros):
    plan = parametros.plan
    materias = parametros.materias

    arch.write("# Los cuatrimestres de las correlativas deben ser menores (cuando la materia se cursa)" + ENTER + ENTER)
    for cod_materia in plan:
        correlativas = plan[cod_materia]
        if not correlativas:
            continue

        materia = materias[cod_materia]

        for cod_m_correlativa in correlativas:
            
            if materia.tipo == OBLIGATORIA:
                escribir_ecuacion_correlativa_depende_de_obligatoria(arch, parametros, cod_materia, cod_m_correlativa)
            else:
                escribir_ecuacion_correlativa_depende_de_electiva(arch, parametros, cod_materia, cod_m_correlativa)

    arch.write(ENTER + ENTER)


def escribir_ecuacion_correlativa_depende_de_obligatoria(arch, parametros, cod_materia, cod_m_correlativa):
    materias = parametros.materias

    cuatri_materia = "C{}".format(cod_materia)
    cuatri_correlativa = "C{}".format(cod_m_correlativa)

    if materias[cod_m_correlativa].tipo == OBLIGATORIA:
        ecuacion = "prob += ({} >= {} + 1)".format(cuatri_correlativa, cuatri_materia)
        arch.write(ecuacion + ENTER)
    else:
        sumatoria = obtener_sumatoria_Y_cuatrimestres_para_materia(parametros, materias[cod_m_correlativa])
        ajuste_electiva_no_cursada = "{} * (1 - ({}))".format(INFINITO, sumatoria)
        ecuacion = "prob += ({} + {} >= {} + 1)".format(cuatri_correlativa, ajuste_electiva_no_cursada, cuatri_materia)
        arch.write(ecuacion + ENTER)


def obtener_sumatoria_Y_cuatrimestres_para_materia(parametros, materia):
    sumatoria = ""
    for cuatrimestre in range (1, parametros.max_cuatrimestres + 1):
        variable = "Y_{}_{}".format(materia.codigo, get_str_cuatrimestre(cuatrimestre))
        sumatoria += variable + " + "
    return sumatoria[:-3]


def escribir_ecuacion_correlativa_depende_de_electiva(arch, parametros, cod_materia, cod_m_correlativa):
    materias = parametros.materias

    cuatri_materia = "C{}".format(cod_materia)
    cuatri_correlativa = "C{}".format(cod_m_correlativa)

    #Si la materia electiva primera se cursa, entonces el cuatrimestre debe ser mayor
    sumatoria_correlativa = obtener_sumatoria_Y_cuatrimestres_para_materia(parametros, materias[cod_m_correlativa])
    ajuste_electiva_no_cursada = "{} * (1 - ({}))".format(INFINITO, sumatoria_correlativa)
    ec_correlativa = "{} + {}".format(cuatri_correlativa, ajuste_electiva_no_cursada)

    sumatoria_primaria = obtener_sumatoria_Y_cuatrimestres_para_materia(parametros, materias[cod_materia])    
    ajuste_electiva_primaria_no_cursada = "(1 * ({}))".format(sumatoria_primaria) 
    ec_primer_materia = "{} + {}".format(cuatri_materia, ajuste_electiva_primaria_no_cursada)

    ecuacion = "prob += ({} >= {})".format(ec_correlativa, ec_primer_materia)
    arch.write(ecuacion + ENTER)

    #Si la materia electiva primera no se cursa, entonces no se puede cursar la que la tiene como correlativa
    ecuacion = "prob += ({} <= {} * ({}))".format(cuatri_correlativa, INFINITO, sumatoria_primaria)    
    arch.write(ecuacion + ENTER)


def generar_restriccion_maxima_cant_materias_por_cuatrimestre(arch, parametros):
    plan = parametros.plan

    arch.write("# La cantidad de materias por cuatrimestre no puede superar un valor maximo" + ENTER + ENTER)
    for cuatrimestre in range (1, parametros.max_cuatrimestres + 1):
        ecuacion = "prob += ("
        es_inicial = True        
        for materia in plan:
            ecuacion = ecuacion if es_inicial else (ecuacion + " + ")
            if es_inicial:
                es_inicial = False

            variable = "Y_{}_{}".format(materia, get_str_cuatrimestre(cuatrimestre))
            ecuacion += variable

        ecuacion += " <= {})".format(parametros.max_cant_materias_por_cuatrimestre)
        arch.write(ecuacion + ENTER)

    arch.write(ENTER + ENTER)


def generar_restriccion_maximo_cuatrimestres_para_func_objetivo(arch, parametros):
    plan = parametros.plan

    arch.write("#TOTAL_CUATRIMESTRES es el maximo de los Ci" + ENTER + ENTER)

    arch.write("prob += (TOTAL_CUATRIMESTRES >= 0)" + ENTER + ENTER)
    for materia in plan:
        var_materia = "C{}".format(materia)
        arch.write("prob += ({} <= TOTAL_CUATRIMESTRES)".format(var_materia) + ENTER)
        arch.write("prob += (-{} <= TOTAL_CUATRIMESTRES)".format(var_materia) + ENTER)
        arch.write(ENTER)
    arch.write(ENTER)


def generar_restriccion_calculo_creditos_obtenidos_por_cuatrimestre(arch, parametros):
    materias = parametros.materias
    plan = parametros.plan

    arch.write("# Calculo de creditos al terminar cada cuatrimestre" + ENTER + ENTER)
    for i in range(1, parametros.max_cuatrimestres + 1):
        ecuacion = "prob += ("
        for cod in plan:
            materia = materias[cod]
            ecuacion += "{}*Y_{}_{} + ".format(materia.creditos, cod, get_str_cuatrimestre(i))
        ecuacion = ecuacion[:-2] #elimino el ultimo + agregado

        if i > 1:
            ecuacion += "+ CRED{}".format(get_str_cuatrimestre(i-1))        

        arch.write(ecuacion + " <= CRED{})".format(get_str_cuatrimestre(i)) + ENTER)
        arch.write(ecuacion + " >= CRED{})".format(get_str_cuatrimestre(i)) + ENTER)
    arch.write(ENTER)          


def generar_restriccion_creditos_minimos_ya_obtenidos_para_cursar(arch, parametros):
    plan = parametros.plan
    materias = parametros.materias

    arch.write("# Restricciones sobre aquellas materias que requieren creditos minimos para poder cursar" + ENTER + ENTER)
    for cod in plan:
        materia = materias[cod]
        if materia.creditos_minimos_aprobados == 0:
            continue
        for i in range(1, parametros.max_cuatrimestres + 1):
            creditos = "CRED{}".format(get_str_cuatrimestre(i-1)) if i > 1 else "0"
            arch.write("prob += ({}*Y_{}_{} <= {})".format(materia.creditos_minimos_aprobados, cod, get_str_cuatrimestre(i), creditos) + ENTER)
        arch.write(ENTER)
    arch.write(ENTER)


def generar_restriccion_creditos_minimos_para_cursar(arch, parametros):
    generar_restriccion_calculo_creditos_obtenidos_por_cuatrimestre(arch, parametros)
    generar_restriccion_creditos_minimos_ya_obtenidos_para_cursar(arch, parametros)


def generar_restriccion_horarios_no_permitidos_por_el_alumno(arch, parametros):
    print("Hacer horarios no permitidos por el alumno.")


def generar_restriccion_si_se_elige_un_curso_se_cursa_su_horario_completo(arch, parametros):
    horarios = parametros.horarios

    arch.write("#Si la materia se cursa en ese cuatrimestre en ese curso en particular, entonces se deben cursar todos los horarios del mismo" + ENTER + ENTER)
    for cuatri in range(1, parametros.max_cuatrimestres + 1):
        for materia in horarios:
            cursos = horarios[materia]
            for curso in cursos:
                H = "H_{}_{}_{}".format(materia, curso.nombre, get_str_cuatrimestre(cuatri))
                for c_horario in curso.horarios:
                    dia = c_horario.dia
                    franjas = c_horario.get_franjas_utilizadas()
                    for franja in franjas:
                        R = "R_{}_{}_{}_{}_{}".format(materia, curso.nombre, dia, franja, get_str_cuatrimestre(cuatri))
                        arch.write("prob += ({} <= {})".format(H, R) + ENTER)
                        arch.write("prob += ({} >= {})".format(H, R) + ENTER)
    arch.write(ENTER)


def generar_restriccion_solo_puede_cursarse_en_un_lugar_al_mismo_tiempo(arch, parametros):
    horarios = parametros.horarios

    arch.write("#No hay giratiempos: Solo puede cursarse una materia en un unico curso en el mismo horario" + ENTER + ENTER)
    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        for dia in parametros.dias:
            for franja in range(parametros.franja_minima, parametros.franja_maxima +1):
                ec_suma = ""
                for materia in horarios:
                    for curso in horarios[materia]:
                        if es_horario_restriccion_valido(curso, dia, franja):
                            ec_suma += "R_{}_{}_{}_{}_{} + ".format(materia, curso.nombre, dia, franja, get_str_cuatrimestre(cuatrimestre))
                ec_suma = ec_suma[:-3]
                if not ec_suma:
                    ec_suma = "0"
                ecuacion = "prob += ({}_{}_{} {} ".format(dia, franja, get_str_cuatrimestre(cuatrimestre), '{}') + ec_suma + ")"
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


def generar_restriccion_si_la_materia_no_se_cursa_en_ese_cuatrimestre_no_se_cursa_ninguno_de_sus_cursos(arch, parametros):
    horarios = parametros.horarios

    arch.write("# Si la materia no se cursa ese cuatrimestre, entonces no puede cursarse en ninguno de los cursos de ese cuatrimestre" + ENTER + ENTER)
    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        for materia in horarios:
            for curso in horarios[materia]:
                Y = "Y_{}_{}".format(materia, get_str_cuatrimestre(cuatrimestre))
                R = "H_{}_{}_{}".format(materia, curso.nombre, get_str_cuatrimestre(cuatrimestre))
                ecuacion = "prob += ({} >= {})".format(Y, R)
                arch.write(ecuacion + ENTER)
    arch.write(ENTER)


def generar_restriccion_la_materia_no_puede_cursarse_en_mas_de_un_curso(arch, parametros):
    horarios = parametros.horarios

    arch.write("# La materia no puede cursarse en mas de un curso en el cuatrimestre" + ENTER + ENTER)
    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        for materia in horarios:
            ecuacion = ""
            for curso in horarios[materia]:
                ecuacion += "H_{}_{}_{} + ".format(materia, curso.nombre, get_str_cuatrimestre(cuatrimestre))
            Y = "Y_{}_{}".format(materia, get_str_cuatrimestre(cuatrimestre))
            arch.write("prob += ({} <= {})".format(Y, ecuacion[:-3]) + ENTER)
            arch.write("prob += ({} >= {})".format(Y, ecuacion[:-3]) + ENTER)
    arch.write(ENTER)


def generar_restriccion_creditos_minimos_electivas(arch, parametros):
    materias = parametros.materias
    creditos = parametros.creditos_minimos_electivas

    if creditos == 0:
        return

    arch.write("#Se debe realizar un minimo de creditos de materias electivas" + ENTER + ENTER)
    ecuacion = "prob += ("
    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        for codigo in materias:
            materia = materias[codigo]
            if materia.tipo == OBLIGATORIA:
                continue
            Y = "Y_{}_{}".format(codigo, get_str_cuatrimestre(cuatrimestre))
            ecuacion += Y + "*" + str(materia.creditos) + " + "
    
    ecuacion = ecuacion[:-3]
    ecuacion = ecuacion + " >= " + str(creditos) + ")"
    arch.write(ecuacion + ENTER + ENTER)


def generar_restriccion_horarios_cursos(arch, parametros):
    generar_restriccion_horarios_no_permitidos_por_el_alumno(arch, parametros)
    generar_restriccion_si_se_elige_un_curso_se_cursa_su_horario_completo(arch, parametros)
    generar_restriccion_solo_puede_cursarse_en_un_lugar_al_mismo_tiempo(arch, parametros)
    generar_restriccion_si_la_materia_no_se_cursa_en_ese_cuatrimestre_no_se_cursa_ninguno_de_sus_cursos(arch, parametros)
    generar_restriccion_la_materia_no_puede_cursarse_en_mas_de_un_curso(arch, parametros)


def generar_restriccion_calcular_maxima_franja_por_dia_y_cuatrimestre(arch, parametros):
    arch.write("#Numero de franja horaria mayor por dia por cuatrimestre" + ENTER + ENTER)
    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        for dia in parametros.dias:
            ecuacion = "prob += (MAXIMA_FRANJA_{}_{} >= ".format(dia, get_str_cuatrimestre(cuatrimestre))
            for franja in range(parametros.franja_minima, parametros.franja_maxima +1):
                arch.write(ecuacion + "{} * {}_{}_{})".format(franja, dia, franja, get_str_cuatrimestre(cuatrimestre)) + ENTER)
    arch.write(ENTER)


def generar_restriccion_calcular_minima_franja_por_dia_y_cuatrimestre(arch, parametros):
    arch.write("#Numero de franja horaria menor por dia por cuatrimestre" + ENTER + ENTER)
    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        for dia in parametros.dias:
            var_min_franja = "MINIMA_FRANJA_{}_{}".format(dia, get_str_cuatrimestre(cuatrimestre))
            ecuacion = "prob += ({} <= ".format(var_min_franja)
            for franja in range(parametros.franja_minima, parametros.franja_maxima +1):
                var_dia = "{}_{}_{}".format(dia, franja, get_str_cuatrimestre(cuatrimestre))
                sumas = "{} * {} + (1 - {}) * {})".format(franja, var_dia, var_dia, INFINITO) 
                arch.write(ecuacion + sumas + ENTER)
    
            arch.write("prob += ({} <= OCUPADO_{}_{} * {})".format(var_min_franja, dia, get_str_cuatrimestre(cuatrimestre), INFINITO) + ENTER)
    
    arch.write(ENTER)


def generar_restriccion_el_dia_esta_ocupado_ese_cuatrimestre(arch, parametros):
    arch.write("#Si alguna de las franjas horarias del dia esta ocupada, entonces el dia esta ocupado" + ENTER + ENTER)
    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        for dia in parametros.dias:
            ecuacion = "prob += (OCUPADO_{}_{} >= ".format(dia, get_str_cuatrimestre(cuatrimestre))
            ec_sumatoria = "prob += (OCUPADO_{}_{} <= ".format(dia, get_str_cuatrimestre(cuatrimestre))
            for franja in range(parametros.franja_minima, parametros.franja_maxima +1):
                var_dia = "{}_{}_{}".format(dia, franja, get_str_cuatrimestre(cuatrimestre))
                arch.write(ecuacion + "{})".format(var_dia) + ENTER)
                ec_sumatoria += "{} + ".format(var_dia)
            ec_sumatoria = ec_sumatoria[:-3] + ")"
            arch.write(ec_sumatoria + ENTER + ENTER)


def generar_restriccion_calcular_horas_libres_por_dia_por_cuatrimestre(arch, parametros):
    arch.write("#Calcular la cantidad de franjas libres entre la primer y la ultima franja ocupada en el dia." + ENTER)
    arch.write("#Si en el dia no se cursan materias, da 0." + ENTER + ENTER)

    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        for dia in parametros.dias:
            
            horas_libres = "HORAS_LIBRES_{}_{}".format(dia, get_str_cuatrimestre(cuatrimestre))
            ocupado = "OCUPADO_{}_{}".format(dia, get_str_cuatrimestre(cuatrimestre))
            maxima_fr = "MAXIMA_FRANJA_{}_{}".format(dia, get_str_cuatrimestre(cuatrimestre))
            minima_fr = "MINIMA_FRANJA_{}_{}".format(dia, get_str_cuatrimestre(cuatrimestre))

            suma_franjas = "("
            for franja in range(parametros.franja_minima, parametros.franja_maxima +1):
                suma_franjas += "{}_{}_{} + ".format(dia, franja, get_str_cuatrimestre(cuatrimestre))
            suma_franjas = suma_franjas[:-3] + ")"

            ecuacion = "prob += (" + maxima_fr + " + " + ocupado + " - " + minima_fr + " - " + suma_franjas
            arch.write(ecuacion + " <= " + horas_libres + ")" + ENTER)
            arch.write(ecuacion + " >= " + horas_libres + ")" + ENTER)

    arch.write(ENTER)


def generar_restriccion_total_horas_libres(arch, parametros):
    arch.write("#Total de horas libres entre materias en el plan, es la suma de las horas libres de cada dia por cuatrimestre" + ENTER + ENTER)
    ecuacion = "prob += ("
    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        for dia in parametros.dias:
            ecuacion += "HORAS_LIBRES_{}_{} + ".format(dia, get_str_cuatrimestre(cuatrimestre))
    ecuacion = ecuacion[:-3]
    arch.write(ecuacion + " <= HORAS_LIBRES_TOTALES)" + ENTER)
    arch.write(ecuacion + " >= HORAS_LIBRES_TOTALES)" + ENTER + ENTER)


def generar_restriccion_minimizar_horas_libres_entre_materias(arch, parametros):
    generar_restriccion_calcular_maxima_franja_por_dia_y_cuatrimestre(arch, parametros)
    generar_restriccion_calcular_minima_franja_por_dia_y_cuatrimestre(arch, parametros)
    generar_restriccion_el_dia_esta_ocupado_ese_cuatrimestre(arch, parametros)
    generar_restriccion_calcular_horas_libres_por_dia_por_cuatrimestre(arch, parametros)
    generar_restriccion_total_horas_libres(arch, parametros)


def generar_restricciones(arch, parametros):
    generar_restriccion_la_materia_debe_cursarse_en_unico_cuatrimestre(arch, parametros)
    generar_restriccion_valor_cuatrimestre_en_que_se_cursa_la_materia(arch, parametros)
    generar_restriccion_correlativas(arch, parametros)
    generar_restriccion_maxima_cant_materias_por_cuatrimestre(arch, parametros)
    generar_restriccion_maximo_cuatrimestres_para_func_objetivo(arch, parametros)
    generar_restriccion_creditos_minimos_para_cursar(arch, parametros)
    generar_restriccion_horarios_cursos(arch, parametros)
    generar_restriccion_creditos_minimos_electivas(arch, parametros)
    generar_restriccion_minimizar_horas_libres_entre_materias(arch, parametros)