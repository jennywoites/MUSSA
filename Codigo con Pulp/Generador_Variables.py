from Constantes import *

def definir_variable_materia_i_en_cuatri_j(plan, arch):
    arch.write("#Yij: La materia i se realiza en el cuatrimestre j" + ENTER + ENTER)
    for materia in plan:
        for cuatrimestre in range(1,MAX_CUATRIMESTRES_TOTALES+1):
            variable = "Y_{}_{}".format(materia, cuatrimestre)
            arch.write("{} = LpVariable(name='{}', cat='Binary')".format(variable, variable) + ENTER)
    arch.write(ENTER + ENTER)


def definir_variable_numero_cuatrimestre_materia(plan, arch):
    arch.write("#Ci: Numero de cuatrimestre en que se hace la materia i. Ejemplo, si Ci=3 es que la materia i se hace el cuatrimestre numero 3" + ENTER + ENTER)
    for materia in plan:
        variable = "C{}".format(materia)
        arch.write("{} = LpVariable(name='{}', cat='Integer')".format(variable, variable) + ENTER)
    arch.write(ENTER + ENTER)


def definir_auxiliar_para_maximo_cuatrimestres(arch):
    arch.write("#TOTAL_CUATRIMESTRES: Total de cuatrimestres a cursar. Utilizada para escribir el maximo entre Ci MAX(CA, CB..)" + ENTER + ENTER)
    arch.write("TOTAL_CUATRIMESTRES = LpVariable(name='TOTAL_CUATRIMESTRES', cat='Integer')" + ENTER + ENTER)


def definir_variable_cantidad_creditos_por_cuatrimestre(arch):
    arch.write("#CREDi: Cantidad de creditos al final del cuatrimestre i" + ENTER + ENTER)
    for cuatrimestre in range(0,MAX_CUATRIMESTRES_TOTALES):
        variable = "CRED{}".format(cuatrimestre)
        arch.write("{} = LpVariable(name='{}', cat='Integer')".format(variable, variable) + ENTER)
    arch.write(ENTER + ENTER)


def definir_variables_horarios_cada_curso_por_materia(arch, plan, horarios):
    arch.write("#H_{materia i}_{nombre del curso j}_{cuatrimestre k}: La materia i se cursa en el curso j en el cuatrimestre k" + ENTER + ENTER)
    for cuatrimestre in range(1, MAX_CUATRIMESTRES_TOTALES + 1):
        for materia in horarios:
            for curso in horarios[materia]:
                variable = "H_{}_{}_{}".format(materia, curso.nombre, cuatrimestre)
                arch.write("{} = LpVariable(name='{}', cat='Binary')".format(variable, variable) + ENTER)
    arch.write(ENTER + ENTER)


def definir_variables_dias_y_franja_por_cuatrimestre(arch, plan, horarios):
    arch.write("#{Dia i}_{Franja j}_{cuatrimestre k}: El dia i (LUNES; MARTES, etc) en la franja horaria j en el cuatrimestre k se esta cursando" + ENTER + ENTER)
    for cuatrimestre in range(1, MAX_CUATRIMESTRES_TOTALES + 1):
        for dia in DIAS:
            for franja in range(FRANJA_MIN, FRANJA_MAX +1):
                variable = "{}_{}_{}".format(dia, franja, cuatrimestre)
                arch.write("{} = LpVariable(name='{}', cat='Binary')".format(variable, variable) + ENTER)
    arch.write(ENTER + ENTER)


def definir_variables_horario_de_la_materia_en_dia_y_cuatrimestre(arch, plan, horarios):
    arch.write("#R_{materia}_{nombre curso}_{dia}_{franja}_{cuatrimestre}: El horario para la materia y curso en ese cuatrimestre esta habilitado" + ENTER + ENTER)
    for cuatrimestre in range(1, MAX_CUATRIMESTRES_TOTALES + 1):
        for materia in horarios:
            for curso in horarios[materia]:
                for c_horario in curso.horarios:
                    dia = c_horario.dia
                    franjas = c_horario.get_franjas_utilizadas()
                    for franja in franjas:
                        variable= "R_{}_{}_{}_{}_{}".format(materia, curso.nombre, dia, franja, cuatrimestre)
                        arch.write("{} = LpVariable(name='{}', cat='Binary')".format(variable, variable) + ENTER)
    arch.write(ENTER + ENTER)


def definir_variables_horarios_de_materias(arch, plan, horarios):
    definir_variables_horarios_cada_curso_por_materia(arch, plan, horarios)
    definir_variables_dias_y_franja_por_cuatrimestre(arch, plan, horarios)
    definir_variables_horario_de_la_materia_en_dia_y_cuatrimestre(arch, plan, horarios)


def definir_variables_esta_el_dia_ocupado_en_un_cuatrimestre(arch):
    arch.write("#OCUPADO_{dia}_{cuatrimestre}: Vale 1 si el {dia} en el {cuatrimestre} tiene al menos un horario ocupado" + ENTER + ENTER)
    for cuatrimestre in range(1, MAX_CUATRIMESTRES_TOTALES + 1):
        for dia in DIAS:
            variable = "OCUPADO_{}_{}".format(dia, cuatrimestre)
            arch.write("{} = LpVariable(name='{}', cat='Binary')".format(variable, variable) + ENTER)
    arch.write(ENTER + ENTER)


def definir_variables_maximo_y_minimo_numero_franja_ocupada_por_dia_por_cuatrimestre(arch):
    arch.write("#MAXIMA_FRANJA_{dia}_{cuatrimestre}: Numero de la maxima franja ocupada en el {dia} en el {cuatrimestre}." + ENTER)
    arch.write("#MINIMA_FRANJA_{dia}_{cuatrimestre}: Numero de la minima franja ocupada en el {dia} en el {cuatrimestre}." + ENTER + ENTER)
    for cuatrimestre in range(1, MAX_CUATRIMESTRES_TOTALES + 1):
        for dia in DIAS:
            variable_max = "MAXIMA_FRANJA_{}_{}".format(dia, cuatrimestre)
            variable_min = "MINIMA_FRANJA_{}_{}".format(dia, cuatrimestre)
            definicion = "{} = LpVariable(name='{}', cat='Integer')"
            arch.write(definicion.format(variable_max, variable_max) + ENTER)
            arch.write(definicion.format(variable_min, variable_min) + ENTER)
    arch.write(ENTER + ENTER)


def definir_variables_horas_libres_entre_materias_por_dia_por_cuatrimestre(arch):
    arch.write("#HORAS_LIBRES_{dia}_{cuatrimestre}: Cantidad de horas libres entre materias el {dia} en el {cuatrimestre}." + ENTER + ENTER)
    for cuatrimestre in range(1, MAX_CUATRIMESTRES_TOTALES + 1):
        for dia in DIAS:
            variable = "HORAS_LIBRES_{}_{}".format(dia, cuatrimestre)
            arch.write("{} = LpVariable(name='{}', cat='Integer')".format(variable, variable) + ENTER)
    arch.write(ENTER + ENTER)


def definir_variable_horas_libres_totales(arch):
    arch.write("#HORAS_LIBRES_TOTALES: Cantidad de horas libres en todo el plan" + ENTER + ENTER)
    variable = "HORAS_LIBRES_TOTALES"
    arch.write("{} = LpVariable(name='{}', cat='Integer')".format(variable, variable) + ENTER)
    arch.write(ENTER + ENTER)


def definir_variables_horas_libres_entre_materias(arch, plan):
    definir_variables_esta_el_dia_ocupado_en_un_cuatrimestre(arch)
    definir_variables_maximo_y_minimo_numero_franja_ocupada_por_dia_por_cuatrimestre(arch)
    definir_variables_horas_libres_entre_materias_por_dia_por_cuatrimestre(arch)
    definir_variable_horas_libres_totales(arch)

def definir_variables(arch, parametros):
    plan = parametros.plan
    horarios = parametros.horarios

    definir_variable_materia_i_en_cuatri_j(plan, arch)
    definir_variable_numero_cuatrimestre_materia(plan, arch)
    definir_auxiliar_para_maximo_cuatrimestres(arch)
    definir_variable_cantidad_creditos_por_cuatrimestre(arch)    
    definir_variables_horarios_de_materias(arch, plan, horarios)
    #definir_variables_horas_libres_entre_materias(arch, plan)

