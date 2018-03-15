from app.API_Rest.GeneradorPlanCarreras.Constantes import *
from app.API_Rest.GeneradorPlanCarreras.my_utils import get_str_cuatrimestre, es_horario_valido_para_el_cuatrimestre


def definir_variable_materia_i_en_cuatri_j(arch, parametros):
    arch.write("#Y_i_j: La materia con id i se realiza en el cuatrimestre j" + ENTER + ENTER)
    for id_materia in parametros.plan:
        for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
            variable = "Y_{}_{}".format(id_materia, get_str_cuatrimestre(cuatrimestre))
            arch.write("{} = LpVariable(name='{}', cat='Binary')".format(variable, variable) + ENTER)
    arch.write(ENTER + ENTER)


def definir_variable_numero_cuatrimestre_materia(arch, parametros):
    arch.write(
        "#Ci: Numero de cuatrimestre en que se hace la materia con id i. Ejemplo, si Ci=3 es que la materia i se hace el cuatrimestre numero 3" + ENTER + ENTER)
    for id_materia in parametros.plan:
        variable = "C{}".format(id_materia)
        arch.write("{} = LpVariable(name='{}', lowBound=0, upBound={}, cat='Integer')".format(variable, variable,
                                                                                              parametros.max_cuatrimestres) + ENTER)
    arch.write(ENTER + ENTER)


def definir_auxiliar_para_maximo_cuatrimestres(arch, parametros):
    arch.write(
        "#TOTAL_CUATRIMESTRES: Total de cuatrimestres a cursar. Utilizada para escribir el maximo entre Ci MAX(CA, CB..)" + ENTER + ENTER)
    variable = "TOTAL_CUATRIMESTRES"
    arch.write("{} = LpVariable(name='{}', lowBound=0, upBound={}, cat='Integer')".format(variable, variable,
                                                                                          parametros.max_cuatrimestres) + ENTER)


def definir_variable_cantidad_creditos_por_cuatrimestre(arch, parametros):
    arch.write("#CREDi: Cantidad de creditos al final del cuatrimestre i" + ENTER + ENTER)
    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        variable = "CRED{}".format(get_str_cuatrimestre(cuatrimestre))
        arch.write("{} = LpVariable(name='{}', lowBound=0, upBound={}, cat='Integer')".format(variable, variable,
                                                                                              INFINITO) + ENTER)
    arch.write(ENTER + ENTER)


def definir_variables_horarios_cada_curso_por_materia(arch, parametros):
    arch.write(
        "#H_{id_materia i}_{id curso j}_{cuatrimestre k}: La materia i se cursa en el curso j en el cuatrimestre k" + ENTER + ENTER)
    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        for id_materia in parametros.horarios:
            for curso in parametros.horarios[id_materia]:
                variable = "H_{}_{}_{}".format(id_materia, curso.id_curso, get_str_cuatrimestre(cuatrimestre))
                arch.write("{} = LpVariable(name='{}', cat='Binary')".format(variable, variable) + ENTER)
    arch.write(ENTER + ENTER)


def definir_variables_dias_y_franja_por_cuatrimestre(arch, parametros):
    arch.write(
        "#{Dia i}_{Franja j}_{cuatrimestre k}: El dia i (LUNES; MARTES, etc) en la franja horaria j en el cuatrimestre k se esta cursando" + ENTER + ENTER)
    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        for dia in parametros.dias:
            for franja in range(parametros.franja_minima, parametros.franja_maxima + 1):
                variable = "{}_{}_{}".format(dia, franja, get_str_cuatrimestre(cuatrimestre))
                arch.write("{} = LpVariable(name='{}', cat='Binary')".format(variable, variable) + ENTER)
    arch.write(ENTER + ENTER)


def definir_variables_horario_de_la_materia_en_dia_y_cuatrimestre(arch, parametros):
    arch.write("#R_{id_materia}_{id curso}_{dia}_{franja}_{cuatrimestre}: "
               "El horario para la materia y curso en ese cuatrimestre esta habilitado" + ENTER + ENTER)
    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        for id_materia in parametros.horarios:
            for curso in parametros.horarios[id_materia]:
                for c_horario in curso.horarios:

                    if not es_horario_valido_para_el_cuatrimestre(parametros, curso, cuatrimestre):
                        continue

                    dia = c_horario.dia
                    franjas = c_horario.get_franjas_utilizadas()
                    for franja in franjas:
                        variable = "R_{}_{}_{}_{}_{}".format(id_materia, curso.id_curso, dia, franja,
                                                             get_str_cuatrimestre(cuatrimestre))
                        arch.write("{} = LpVariable(name='{}', cat='Binary')".format(variable, variable) + ENTER)
    arch.write(ENTER + ENTER)


def definir_variables_horarios_de_materias(arch, parametros):
    definir_variables_horarios_cada_curso_por_materia(arch, parametros)
    definir_variables_dias_y_franja_por_cuatrimestre(arch, parametros)
    definir_variables_horario_de_la_materia_en_dia_y_cuatrimestre(arch, parametros)


def definir_variables(arch, parametros):
    definir_variable_materia_i_en_cuatri_j(arch, parametros)
    definir_variable_numero_cuatrimestre_materia(arch, parametros)
    definir_auxiliar_para_maximo_cuatrimestres(arch, parametros)
    definir_variable_cantidad_creditos_por_cuatrimestre(arch, parametros)
    definir_variables_horarios_de_materias(arch, parametros)
