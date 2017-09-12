from Constantes import *

def generar_restriccion_la_materia_debe_cursarse_en_unico_cuatrimestre(arch, materias):
    arch.write("# La materia i se debe cursar en un unico cuatrimestre. Ademas, si es obligatoria, debe cursarse si o si." + ENTER + ENTER)
    for materia in materias:
        ecuacion = "prob += ("
        for cuatrimestre in range(1,MAX_CUATRIMESTRES_TOTALES+1):
            if cuatrimestre > 1:
                ecuacion += " + "
            variable = "Y_{}_{}".format(materia, cuatrimestre)
            ecuacion += variable
        
        ecuacion_complementaria = ecuacion
        ecuacion += " <= 1)"
        ecuacion_complementaria += " >= 1)"

        if materias[materia].tipo == OBLIGATORIA:
            arch.write(ecuacion_complementaria + ENTER)
        arch.write(ecuacion + ENTER)

        arch.write(ENTER)
    arch.write(ENTER)


def generar_restriccion_valor_cuatrimestre_en_que_se_cursa_la_materia(arch, plan):
    arch.write("# Numero de cuatrimestre en que es cursada la materia" + ENTER + ENTER)
    for materia in plan:
        ecuacion = "prob += ("
        for cuatrimestre in range(1,MAX_CUATRIMESTRES_TOTALES+1):
            if cuatrimestre > 1:
                ecuacion += " + "
            variable = "Y_{}_{}".format(materia, cuatrimestre)
            ecuacion += "{}*{}".format(cuatrimestre,variable)
        
        variable_c_materia = "C{}".format(materia)
        ecuacion += " - {} ".format(variable_c_materia)
        ecuacion_complementaria = ecuacion
        ecuacion += "<= 0)"
        ecuacion_complementaria += ">= 0)"

        arch.write(ecuacion + ENTER)
        arch.write(ecuacion_complementaria + ENTER)
        arch.write(ENTER)
    arch.write(ENTER)


def generar_restriccion_correlativas(arch, plan):
    arch.write("# Los cuatrimestres de las correlativas deben ser menores" + ENTER + ENTER)
    for materia in plan:
        correlativas = plan[materia]
        if not correlativas:
            continue

        primera = "C{}".format(materia)
        for m_correlativa in correlativas:
            segunda = "C{}".format(m_correlativa)
            
            #La segunda (correlativa) se tiene que hacer despues
            arch.write("prob += ({} - {} >= 1)".format(segunda, primera) + ENTER)

    arch.write(ENTER + ENTER)


def generar_restriccion_maxima_cant_materias_por_cuatrimestre(arch, plan):
    arch.write("# La cantidad de materias por cuatrimestre no puede superar un valor maximo" + ENTER + ENTER)
    for cuatrimestre in range (1, MAX_CUATRIMESTRES_TOTALES +1):
        ecuacion = "prob += ("
        es_inicial = True        
        for materia in plan:
            ecuacion = ecuacion if es_inicial else (ecuacion + " + ") 
            if es_inicial:
                es_inicial = False

            variable = "Y_{}_{}".format(materia, cuatrimestre)
            ecuacion += variable

        ecuacion += " <= {})".format(MAX_CANTIDAD_MATERIAS_POR_CUATRIMESTRE)
        arch.write(ecuacion + ENTER)

    arch.write(ENTER + ENTER)


def generar_restriccion_maximo_cuatrimestres_para_func_objetivo(arch, plan):
    arch.write("#TOTAL_CUATRIMESTRES es el maximo de los Ci" + ENTER + ENTER)

    arch.write("prob += (TOTAL_CUATRIMESTRES >= 0)" + ENTER + ENTER)
    for materia in plan:
        var_materia = "C{}".format(materia)
        arch.write("prob += ({} <= TOTAL_CUATRIMESTRES)".format(var_materia) + ENTER)
        arch.write("prob += (-{} <= TOTAL_CUATRIMESTRES)".format(var_materia) + ENTER)
        arch.write(ENTER)
    arch.write(ENTER)


def generar_restriccion_calculo_creditos_obtenidos_por_cuatrimestre(plan, materias, arch):
    arch.write("# Calculo de creditos al terminar cada cuatrimestre" + ENTER + ENTER)
    arch.write("prob += (CRED0 <= 0)" + ENTER)
    arch.write("prob += (CRED0 >= 0)" + ENTER)
    for i in range(1, MAX_CUATRIMESTRES_TOTALES):
        ecuacion = "prob += ("
        for cod in plan:
            materia = materias[cod]
            ecuacion += "{}*Y_{}_{} + ".format(materia.creditos, cod, i)
        ecuacion = ecuacion[:-2] #elimino el ultimo + agregado
        ecuacion += "+ CRED{} - CRED{}".format(i-1, i)        
        arch.write(ecuacion + " <= 0)" + ENTER)
        arch.write(ecuacion + " >= 0)" + ENTER)
    arch.write(ENTER)          


def generar_restriccion_creditos_minimos_ya_obtenidos_para_cursar(plan, materias, arch):
    arch.write("# Restricciones sobre aquellas materias que requieren creditos minimos para poder cursar" + ENTER + ENTER)
    for cod in plan:
        materia = materias[cod]
        if materia.creditos_minimos_aprobados == 0:
            continue
        for i in range(1, MAX_CUATRIMESTRES_TOTALES + 1):
            arch.write("prob += ({}*Y_{}_{} <= CRED{})".format(materia.creditos_minimos_aprobados, cod, i, i-1) + ENTER)
        arch.write(ENTER)
    arch.write(ENTER)


def generar_restriccion_creditos_minimos_para_cursar(arch, plan, materias):
    generar_restriccion_calculo_creditos_obtenidos_por_cuatrimestre(plan, materias, arch)
    generar_restriccion_creditos_minimos_ya_obtenidos_para_cursar(plan, materias, arch)


def generar_restriccion_horarios_no_permitidos_por_el_alumno(arch, horarios_no_permitidos):
    input("Hacer horarios no permitidos por el alumno. ENTER")


def generar_restriccion_si_se_elige_un_curso_se_cursa_su_horario_completo(arch, horarios):
    arch.write("#Si la materia se cursa en ese cuatrimestre en ese curso en particular, entonces se debn cursar todos los horarios del mismo" + ENTER + ENTER)
    ecuaciones = []
    for cuatri in range(1, MAX_CUATRIMESTRES_TOTALES + 1):
        for materia in horarios:
            cursos = horarios[materia]
            for curso in cursos:
                igualdades = ["H_{}_{}_{}".format(materia, curso.nombre, cuatri)]
                for c_horario in curso.horarios:
                    dia = c_horario.dia
                    franjas = c_horario.get_franjas_utilizadas()
                    for franja in franjas:
                        igualdades.append("R_{}_{}_{}_{}_{}".format(materia, curso.nombre, dia, franja, cuatri))
                ecuaciones.append(igualdades)

    for igualdades in ecuaciones:
        for i in range(len(igualdades)):
            variable_origen = igualdades[i]
            for j in range(i+1, len(igualdades)):
                variable_sig = igualdades[j]
                arch.write("prob += ({} <= {})".format(variable_origen, variable_sig) + ENTER)
                arch.write("prob += ({} >= {})".format(variable_origen, variable_sig) + ENTER)
        arch.write(ENTER)
    arch.write(ENTER)


def generar_restriccion_solo_puede_cursarse_en_un_lugar_al_mismo_tiempo(arch, horarios):
    arch.write("#No hay giratiempos: Solo puede cursarse una materia en un unico curso en el mismo horario" + ENTER + ENTER)
    for cuatrimestre in range(1, MAX_CUATRIMESTRES_TOTALES + 1):
        for dia in DIAS:
            for franja in range(FRANJA_MIN, FRANJA_MAX +1):
                ecuacion = "prob += ({}_{}_{} >= ".format(dia, franja, cuatrimestre)
                for materia in horarios:
                    for curso in horarios[materia]:
                        if es_horario_restriccion_valido(curso, dia, franja):
                            ecuacion += "R_{}_{}_{}_{}_{} + ".format(materia, curso.nombre, dia, franja, cuatrimestre)
                ecuacion = ecuacion[:-3]
                ecuacion += ")"
                arch.write(ecuacion + ENTER)
    arch.write(ENTER)              


def es_horario_restriccion_valido(curso, dia, franja):
    for c_horario in curso.horarios:
        c_dia = c_horario.dia
        franjas = c_horario.get_franjas_utilizadas()
        if dia == c_dia and franja in franjas:
            return True
    return False


def generar_restriccion_si_la_materia_no_se_cursa_en_ese_cuatrimestre_no_se_cursa_ninguno_de_sus_cursos(arch, horarios):
    arch.write("# Si la materia no se cursa ese cuatrimestre, entonces no puede cursarse en ninguno de los cursos de ese cuatrimestre" + ENTER + ENTER)
    for cuatrimestre in range(1, MAX_CUATRIMESTRES_TOTALES + 1):
        for materia in horarios:
            for curso in horarios[materia]:
                Y = "Y_{}_{}".format(materia, cuatrimestre)
                R = "H_{}_{}_{}".format(materia, curso.nombre, cuatrimestre)
                ecuacion = "prob += ({} >= {})".format(Y, R)
                arch.write(ecuacion + ENTER)
    arch.write(ENTER)


def generar_restriccion_la_materia_no_puede_cursarse_en_mas_de_un_curso(arch, horarios):
    arch.write("# La materia no puede cursarse en mas de un curso en el cuatrimestre" + ENTER + ENTER)
    for cuatrimestre in range(1, MAX_CUATRIMESTRES_TOTALES + 1):
        for materia in horarios:
            ecuacion = ""
            for curso in horarios[materia]:
                ecuacion += "H_{}_{}_{} + ".format(materia, curso.nombre, cuatrimestre)
            Y = "Y_{}_{}".format(materia, cuatrimestre)
            arch.write("prob += ({} <= {})".format(Y, ecuacion[:-3]) + ENTER)
    arch.write(ENTER)


def generar_restriccion_creditos_minimos_electivas(arch, materias, creditos):
    arch.write("#Se debe realizar un minimo de creditos de materias electivas" + ENTER + ENTER)
    ecuacion = "prob += ("
    for cuatrimestre in range(1, MAX_CUATRIMESTRES_TOTALES + 1):
        for codigo in materias:
            materia = materias[codigo]
            if materia.tipo == OBLIGATORIA:
                continue
            Y = "Y_{}_{}".format(codigo, cuatrimestre)
            ecuacion += Y + "*" + str(materia.creditos) + " + "
    
    ecuacion = ecuacion[:-3]
    ecuacion = ecuacion + " >= " + str(creditos) + ")"
    arch.write(ecuacion + ENTER + ENTER)


def generar_restriccion_horarios_cursos(arch, plan, materias, horarios, horarios_no_permitidos):
    generar_restriccion_horarios_no_permitidos_por_el_alumno(arch, horarios_no_permitidos)
    generar_restriccion_si_se_elige_un_curso_se_cursa_su_horario_completo(arch, horarios)
    generar_restriccion_solo_puede_cursarse_en_un_lugar_al_mismo_tiempo(arch, horarios)
    generar_restriccion_si_la_materia_no_se_cursa_en_ese_cuatrimestre_no_se_cursa_ninguno_de_sus_cursos(arch, horarios)
    generar_restriccion_la_materia_no_puede_cursarse_en_mas_de_un_curso(arch, horarios)


def generar_restriccion_calcular_maxima_franja_por_dia_y_cuatrimestre(arch):
    arch.write("#Numero de franja horaria mayor por dia por cuatrimestre" + ENTER + ENTER)
    for cuatrimestre in range(1, MAX_CUATRIMESTRES_TOTALES + 1):
        for dia in DIAS:
            ecuacion = "prob += (MAXIMA_FRANJA_{}_{} >= ".format(dia, cuatrimestre)
            for franja in range(FRANJA_MIN, FRANJA_MAX +1):
                arch.write(ecuacion + "{} * {}_{}_{} )".format(franja, dia, franja, cuatrimestre) + ENTER)
    arch.write(ENTER)


def generar_restriccion_calcular_minima_franja_por_dia_y_cuatrimestre(arch):
    arch.write("#Numero de franja horaria menor por dia por cuatrimestre" + ENTER + ENTER)
    for cuatrimestre in range(1, MAX_CUATRIMESTRES_TOTALES + 1):
        for dia in DIAS:
            ecuacion = "prob += (MINIMA_FRANJA_{}_{} <= ".format(dia, cuatrimestre)
            for franja in range(FRANJA_MIN, FRANJA_MAX +1):
                var_dia = "{}_{}_{}".format(dia, franja, cuatrimestre)
                sumas = "{} * {} + (1 - {}) * {} )".format(franja, var_dia, var_dia, INFINITO) 
                arch.write(ecuacion + sumas + ENTER)
    
            arch.write("prob += (OCUPADO_{}_{} * {})".format(dia, cuatrimestre, INFINITO) + ENTER)
    
    arch.write(ENTER)


def generar_restriccion_el_dia_esta_ocupado_ese_cuatrimestre(arch):
    arch.write("#Si alguna de las franjas horarias del dia esta ocupada, entonces el dia esta ocupado" + ENTER + ENTER)
    for cuatrimestre in range(1, MAX_CUATRIMESTRES_TOTALES + 1):
        for dia in DIAS:
            ecuacion = "prob += (OCUPADO_{}_{} >= ".format(dia, cuatrimestre)
            for franja in range(FRANJA_MIN, FRANJA_MAX +1):
                arch.write(ecuacion + "{}_{}_{} )".format(dia, franja, cuatrimestre) + ENTER)
    arch.write(ENTER)


def generar_restriccion_calcular_horas_libres_por_dia_por_cuatrimestre(arch):
    arch.write("#Calcular la cantidad de franjas libres entre la primer y la ultima franja ocupada en el dia." + ENTER)
    arch.write("#Si en el dia no se cursan materias, da 0." + ENTER + ENTER)

    for cuatrimestre in range(1, MAX_CUATRIMESTRES_TOTALES + 1):
        for dia in DIAS:
            
            horas_libres = "HORAS_LIBRES_{}_{}".format(dia, cuatrimestre)
            ocupado = "OCUPADO_{}_{}".format(dia, cuatrimestre)
            maxima_fr = "MAXIMA_FRANJA_{}_{}".format(dia, cuatrimestre)
            minima_fr = "MINIMA_FRANJA_{}_{}".format(dia, cuatrimestre)

            suma_franjas = "("
            for franja in range(FRANJA_MIN, FRANJA_MAX +1):
                suma_franjas += "{}_{}_{} + ".format(dia, franja, cuatrimestre)
            suma_franjas = suma_franjas[:-3] + ")"

            ecuacion = "prob += (" + maxima_fr + " + " + ocupado + " - " + minima_fr + " - " + suma_franjas
            arch.write(ecuacion + " <= " + horas_libres + ")" + ENTER)
            arch.write(ecuacion + " >= " + horas_libres + ")" + ENTER)

    arch.write(ENTER)


def generar_restriccion_total_horas_libres(arch):
    arch.write("#Total de horas libres entre materias en el plan, es la suma de las horas libres de cada dia por cuatrimestre" + ENTER + ENTER)
    ecuacion = "prob += ("
    for cuatrimestre in range(1, MAX_CUATRIMESTRES_TOTALES + 1):
        for dia in DIAS:
            ecuacion += "HORAS_LIBRES_{}_{} + ".format(dia, cuatrimestre)
    ecuacion = ecuacion[:-3]
    arch.write(ecuacion + " <= HORAS_LIBRES_TOTALES)" + ENTER)
    arch.write(ecuacion + " >= HORAS_LIBRES_TOTALES)" + ENTER + ENTER)


def generar_restriccion_minimizar_horas_libres_entre_materias(arch):
    generar_restriccion_calcular_maxima_franja_por_dia_y_cuatrimestre(arch)
    generar_restriccion_calcular_minima_franja_por_dia_y_cuatrimestre(arch)
    generar_restriccion_el_dia_esta_ocupado_ese_cuatrimestre(arch)
    generar_restriccion_calcular_horas_libres_por_dia_por_cuatrimestre(arch)
    generar_restriccion_total_horas_libres(arch)


def generar_restricciones(arch, parametros):
    plan = parametros.plan
    materias = parametros.materias
    horarios = parametros.horarios
    horarios_no_permitidos = parametros.horarios_no_permitidos

    generar_restriccion_la_materia_debe_cursarse_en_unico_cuatrimestre(arch, materias)
    generar_restriccion_valor_cuatrimestre_en_que_se_cursa_la_materia(arch, plan)
    generar_restriccion_correlativas(arch, plan)
    generar_restriccion_maxima_cant_materias_por_cuatrimestre(arch, plan)
    generar_restriccion_maximo_cuatrimestres_para_func_objetivo(arch, plan)
    generar_restriccion_creditos_minimos_para_cursar(arch, plan, materias)
    generar_restriccion_horarios_cursos(arch, plan, materias, horarios, horarios_no_permitidos)
    generar_restriccion_creditos_minimos_electivas(arch, materias, parametros.creditos_minimos_electivas)
    generar_restriccion_minimizar_horas_libres_entre_materias(arch)