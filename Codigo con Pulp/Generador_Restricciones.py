from Constantes import *

def generar_restriccion_la_materia_debe_cursarse_en_unico_cuatrimestre(plan, arch):
    arch.write("# La materia i se debe cursar en un unico cuatrimestre y debe cursarse si o si (por ser obligatoria)" + ENTER + ENTER)
    for materia in plan:
        ecuacion = "prob += ("
        for cuatrimestre in range(1,MAX_CUATRIMESTRES_TOTALES+1):
            if cuatrimestre > 1:
                ecuacion += " + "
            variable = "Y{}{}".format(materia, cuatrimestre)
            ecuacion += variable
        
        ecuacion_complementaria = ecuacion
        ecuacion += " <= 1)"
        ecuacion_complementaria += " >= 1)"

        arch.write(ecuacion + ENTER)
        arch.write(ecuacion_complementaria + ENTER)
        arch.write(ENTER)
    arch.write(ENTER)


def generar_restriccion_valor_cuatrimestre_en_que_se_cursa_la_materia(plan,arch):
    arch.write("# Numero de cuatrimestre en que es cursada la materia" + ENTER + ENTER)
    for materia in plan:
        ecuacion = "prob += ("
        for cuatrimestre in range(1,MAX_CUATRIMESTRES_TOTALES+1):
            if cuatrimestre > 1:
                ecuacion += " + "
            variable = "Y{}{}".format(materia, cuatrimestre)
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


def generar_restriccion_correlativas(plan, arch):
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


def generar_restriccion_maxima_cant_materias_por_cuatrimestre(plan,arch):
    arch.write("# La cantidad de materias por cuatrimestre no puede superar un valor maximo" + ENTER + ENTER)
    for cuatrimestre in range (1, MAX_CUATRIMESTRES_TOTALES +1):
        ecuacion = "prob += ("
        es_inicial = True        
        for materia in plan:
            ecuacion = ecuacion if es_inicial else (ecuacion + " + ") 
            if es_inicial:
                es_inicial = False

            variable = "Y{}{}".format(materia, cuatrimestre)
            ecuacion += variable

        ecuacion += " <= {})".format(MAX_CANTIDAD_MATERIAS_POR_CUATRIMESTRE)
        arch.write(ecuacion + ENTER)

    arch.write(ENTER + ENTER)


def generar_restriccion_maximo_cuatrimestres_para_func_objetivo(plan, arch):
    arch.write("# Funcion objetivo es el maximo de los Ci" + ENTER + ENTER)

    arch.write("prob += (y >= 0)" + ENTER + ENTER)
    for materia in plan:
        var_materia = "C{}".format(materia)
        arch.write("prob += ({} <= y)".format(var_materia) + ENTER)
        arch.write("prob += (-{} <= y)".format(var_materia) + ENTER)
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
            ecuacion += "{}*Y{}{} + ".format(materia.creditos, cod, i)
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
            arch.write("prob += ({}*Y{}{} <= CRED{})".format(materia.creditos_minimos_aprobados, cod, i, i-1) + ENTER)
        arch.write(ENTER)
    arch.write(ENTER)


def generar_restriccion_creditos_minimos_para_cursar(plan, materias, arch):
    generar_restriccion_calculo_creditos_obtenidos_por_cuatrimestre(plan, materias, arch)
    generar_restriccion_creditos_minimos_ya_obtenidos_para_cursar(plan, materias, arch)


def generar_restriccion_horarios_no_permitidos_por_el_alumno(arch, horarios_no_permitidos):
    input("HAcer horarios no permitidos por el alumno. ENTER")


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


def generar_restriccion_horarios_no_dictados_para_el_curso(arch, horarios):
    arch.write("#Si el curso no se dicta en la franja horaria, entonces esta vale 0" + ENTER + ENTER)
    ecuaciones = []
    for cuatri in range(1, MAX_CUATRIMESTRES_TOTALES + 1):
        for materia in horarios:
            cursos = horarios[materia]
            for curso in cursos:
                for c_horario in curso.horarios:
                    dia = c_horario.dia
                    franjas = c_horario.get_franjas_utilizadas()
                    franjas_no_utilizadas = [x for x in range(1,franjas[0])] + [x for x in range(franjas[-1]+1,FRANJA_MAX+1)]
                    for franja in franjas_no_utilizadas:
                        variable = "R_{}_{}_{}_{}_{}".format(materia, curso.nombre, dia, franja, cuatri)
                        arch.write("prob += ({} >= 0)".format(variable) + ENTER)
                        arch.write("prob += ({} <= 0)".format(variable) + ENTER)
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
                        ecuacion += "R_{}_{}_{}_{}_{} + ".format(materia, curso.nombre, dia, franja, cuatrimestre)
                ecuacion = ecuacion[:-3]
                ecuacion += ")"
                arch.write(ecuacion + ENTER)
    arch.write(ENTER)              


def generar_restriccion_si_la_materia_no_se_cursa_en_ese_cuatrimestre_no_se_cursa_ninguno_de_sus_cursos(arch, horarios):
    arch.write("# Si la materia no se cursa ese cuatrimestre, entonces no puede cursarse en ninguno de los cursos de ese cuatrimestre" + ENTER + ENTER)
    for cuatrimestre in range(1, MAX_CUATRIMESTRES_TOTALES + 1):
        for materia in horarios:
            for curso in horarios[materia]:
                Y = "Y{}{}".format(materia, cuatrimestre)
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
            Y = "Y{}{}".format(materia, cuatrimestre)
            arch.write("prob += ({} <= {})".format(Y, ecuacion[:-3]) + ENTER)
    arch.write(ENTER)

def generar_restriccion_horarios_cursos(arch, plan, materias, horarios, horarios_no_permitidos):
    generar_restriccion_horarios_no_permitidos_por_el_alumno(arch, horarios_no_permitidos)
    generar_restriccion_horarios_no_dictados_para_el_curso(arch, horarios)
    generar_restriccion_si_se_elige_un_curso_se_cursa_su_horario_completo(arch, horarios)
    generar_restriccion_solo_puede_cursarse_en_un_lugar_al_mismo_tiempo(arch, horarios)
    generar_restriccion_si_la_materia_no_se_cursa_en_ese_cuatrimestre_no_se_cursa_ninguno_de_sus_cursos(arch, horarios)
    generar_restriccion_la_materia_no_puede_cursarse_en_mas_de_un_curso(arch, horarios)

def generar_restricciones(arch, plan, materias, horarios, horarios_no_permitidos):
    generar_restriccion_la_materia_debe_cursarse_en_unico_cuatrimestre(plan, arch)
    generar_restriccion_valor_cuatrimestre_en_que_se_cursa_la_materia(plan,arch)
    generar_restriccion_correlativas(plan, arch)
    generar_restriccion_maxima_cant_materias_por_cuatrimestre(plan,arch)
    generar_restriccion_maximo_cuatrimestres_para_func_objetivo(plan, arch)
    generar_restriccion_creditos_minimos_para_cursar(plan, materias, arch)
    generar_restriccion_horarios_cursos(arch, plan, materias, horarios, horarios_no_permitidos)


