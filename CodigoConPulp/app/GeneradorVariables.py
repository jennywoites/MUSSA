from Constantes import *

def definir_variable_materia_i_en_cuatri_j(arch, parametros):
    plan = parametros.plan

    arch.write("#Yij: La materia i se realiza en el cuatrimestre j" + ENTER + ENTER)
    for materia in plan:
        for cuatrimestre in range(1,parametros.max_cuatrimestres + 1):
            variable = "Y_{}_{}".format(materia, cuatrimestre)
            arch.write("{} = LpVariable(name='{}', cat='Binary')".format(variable, variable) + ENTER)
    arch.write(ENTER + ENTER)


def definir_variable_numero_cuatrimestre_materia(arch, parametros):
    plan = parametros.plan

    arch.write("#Ci: Numero de cuatrimestre en que se hace la materia i. Ejemplo, si Ci=3 es que la materia i se hace el cuatrimestre numero 3" + ENTER + ENTER)
    for materia in plan:
        variable = "C{}".format(materia)
        arch.write("{} = LpVariable(name='{}', lowBound=0, upBound={}, cat='Integer')".format(variable, variable, INFINITO) + ENTER)
    arch.write(ENTER + ENTER)


def definir_auxiliar_para_maximo_cuatrimestres(arch):
    arch.write("#TOTAL_CUATRIMESTRES: Total de cuatrimestres a cursar. Utilizada para escribir el maximo entre Ci MAX(CA, CB..)" + ENTER + ENTER)
    variable = "TOTAL_CUATRIMESTRES"
    arch.write("{} = LpVariable(name='{}', lowBound=0, upBound={}, cat='Integer')".format(variable, variable, INFINITO) + ENTER)


def definir_variable_cantidad_creditos_por_cuatrimestre(arch, parametros):
    arch.write("#CREDi: Cantidad de creditos al final del cuatrimestre i" + ENTER + ENTER)
    for cuatrimestre in range(1,parametros.max_cuatrimestres + 1):
        variable = "CRED{}".format(cuatrimestre)
        arch.write("{} = LpVariable(name='{}', lowBound=0, upBound={}, cat='Integer')".format(variable, variable, INFINITO) + ENTER)
    arch.write(ENTER + ENTER)


def definir_variables_horarios_cada_curso_por_materia(arch, parametros):
    horarios = parametros.horarios

    arch.write("#H_{materia i}_{nombre del curso j}_{cuatrimestre k}: La materia i se cursa en el curso j en el cuatrimestre k" + ENTER + ENTER)
    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        for materia in horarios:
            for curso in horarios[materia]:
                variable = "H_{}_{}_{}".format(materia, curso.nombre, cuatrimestre)
                arch.write("{} = LpVariable(name='{}', cat='Binary')".format(variable, variable) + ENTER)
    arch.write(ENTER + ENTER)


def definir_variables_dias_y_franja_por_cuatrimestre(arch, parametros):    
    arch.write("#{Dia i}_{Franja j}_{cuatrimestre k}: El dia i (LUNES; MARTES, etc) en la franja horaria j en el cuatrimestre k se esta cursando" + ENTER + ENTER)
    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        for dia in parametros.dias:
            for franja in range(parametros.franja_minima, parametros.franja_maxima +1):
                variable = "{}_{}_{}".format(dia, franja, cuatrimestre)
                arch.write("{} = LpVariable(name='{}', cat='Binary')".format(variable, variable) + ENTER)
    arch.write(ENTER + ENTER)


def definir_variables_horario_de_la_materia_en_dia_y_cuatrimestre(arch, parametros):
    horarios = parametros.horarios

    arch.write("#R_{materia}_{nombre curso}_{dia}_{franja}_{cuatrimestre}: El horario para la materia y curso en ese cuatrimestre esta habilitado" + ENTER + ENTER)
    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        for materia in horarios:
            for curso in horarios[materia]:
                for c_horario in curso.horarios:
                    dia = c_horario.dia
                    franjas = c_horario.get_franjas_utilizadas()
                    for franja in franjas:
                        variable= "R_{}_{}_{}_{}_{}".format(materia, curso.nombre, dia, franja, cuatrimestre)
                        arch.write("{} = LpVariable(name='{}', cat='Binary')".format(variable, variable) + ENTER)
    arch.write(ENTER + ENTER)


def definir_variables_horarios_de_materias(arch, parametros):
    definir_variables_horarios_cada_curso_por_materia(arch, parametros)
    definir_variables_dias_y_franja_por_cuatrimestre(arch, parametros)
    definir_variables_horario_de_la_materia_en_dia_y_cuatrimestre(arch, parametros)


def definir_variables_esta_el_dia_ocupado_en_un_cuatrimestre(arch, parametros):
    arch.write("#OCUPADO_{dia}_{cuatrimestre}: Vale 1 si el {dia} en el {cuatrimestre} tiene al menos un horario ocupado" + ENTER + ENTER)
    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        for dia in parametros.dias:
            variable = "OCUPADO_{}_{}".format(dia, cuatrimestre)
            arch.write("{} = LpVariable(name='{}', cat='Binary')".format(variable, variable) + ENTER)
    arch.write(ENTER + ENTER)


def definir_variables_maximo_y_minimo_numero_franja_ocupada_por_dia_por_cuatrimestre(arch, parametros):
    arch.write("#MAXIMA_FRANJA_{dia}_{cuatrimestre}: Numero de la maxima franja ocupada en el {dia} en el {cuatrimestre}." + ENTER)
    arch.write("#MINIMA_FRANJA_{dia}_{cuatrimestre}: Numero de la minima franja ocupada en el {dia} en el {cuatrimestre}." + ENTER + ENTER)
    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        for dia in parametros.dias:
            variable_max = "MAXIMA_FRANJA_{}_{}".format(dia, cuatrimestre)
            variable_min = "MINIMA_FRANJA_{}_{}".format(dia, cuatrimestre)
            definicion = "{} = LpVariable(name='{}', lowBound=0, upBound={}, cat='Integer')"
            arch.write(definicion.format(variable_max, variable_max, INFINITO) + ENTER)
            arch.write(definicion.format(variable_min, variable_min, INFINITO) + ENTER)
    arch.write(ENTER + ENTER)


def definir_variables_horas_libres_entre_materias_por_dia_por_cuatrimestre(arch, parametros):
    arch.write("#HORAS_LIBRES_{dia}_{cuatrimestre}: Cantidad de horas libres entre materias el {dia} en el {cuatrimestre}." + ENTER + ENTER)
    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        for dia in parametros.dias:
            variable = "HORAS_LIBRES_{}_{}".format(dia, cuatrimestre)
            arch.write("{} = LpVariable(name='{}', lowBound=0, upBound={}, cat='Integer')".format(variable, variable, INFINITO) + ENTER)
    arch.write(ENTER + ENTER)


def definir_variable_horas_libres_totales(arch):
    arch.write("#HORAS_LIBRES_TOTALES: Cantidad de horas libres en todo el plan" + ENTER + ENTER)
    variable = "HORAS_LIBRES_TOTALES"
    arch.write("{} = LpVariable(name='{}', lowBound=0, upBound={}, cat='Integer')".format(variable, variable, INFINITO) + ENTER)
    arch.write(ENTER + ENTER)


def definir_variables_horas_libres_entre_materias(arch, parametros):
    definir_variables_esta_el_dia_ocupado_en_un_cuatrimestre(arch, parametros)
    definir_variables_maximo_y_minimo_numero_franja_ocupada_por_dia_por_cuatrimestre(arch, parametros)
    definir_variables_horas_libres_entre_materias_por_dia_por_cuatrimestre(arch, parametros)
    definir_variable_horas_libres_totales(arch)

def definir_variables(arch, parametros):
    definir_variable_materia_i_en_cuatri_j(arch, parametros)
    definir_variable_numero_cuatrimestre_materia(arch, parametros)
    definir_auxiliar_para_maximo_cuatrimestres(arch)
    definir_variable_cantidad_creditos_por_cuatrimestre(arch, parametros)    
    definir_variables_horarios_de_materias(arch, parametros)
    definir_variables_horas_libres_entre_materias(arch, parametros)