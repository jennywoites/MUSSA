from app.API_Rest.GeneradorPlanCarreras.Constantes import *
from app.API_Rest.GeneradorPlanCarreras.my_utils import get_str_cuatrimestre, es_horario_valido_para_el_cuatrimestre

LINEA_GUARDAR = """    arch.write("{};{}".format(int(value({}))) + "\\n")"""


def guardar_variable_materia_i_en_cuatri_j(arch, parametros):
    for id_materia in parametros.plan:
        for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
            variable = "Y_{}_{}".format(id_materia, get_str_cuatrimestre(cuatrimestre))
            arch.write(LINEA_GUARDAR.format(variable, '{}', variable) + ENTER)


def guardar_variable_materia_trabajo_final_en_cuatri_j(arch, parametros):
    for materia in parametros.materia_trabajo_final:
        for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
            variable = "Y_TP_FINAL_{}_{}_{}".format(materia.id_materia, materia.codigo,
                                                    get_str_cuatrimestre(cuatrimestre))
            arch.write(LINEA_GUARDAR.format(variable, '{}', variable) + ENTER)


def guardar_variable_numero_cuatrimestre_materia(arch, parametros):
    for id_materia in parametros.plan:
        variable = "C{}".format(id_materia)
        arch.write(LINEA_GUARDAR.format(variable, '{}', variable) + ENTER)


def guardar_variable_numero_cuatrimestre_materia_trabajo_final(arch, parametros):
    for materia in parametros.materia_trabajo_final:
        variable = "C_TP_FINAL_{}_{}".format(materia.id_materia, materia.codigo)
        arch.write(LINEA_GUARDAR.format(variable, '{}', variable) + ENTER)


def guardar_total_cuatrimestres(arch):
    arch.write(LINEA_GUARDAR.format("TOTAL_CUATRIMESTRES", '{}', "TOTAL_CUATRIMESTRES") + ENTER)


def guardar_variable_cantidad_creditos_por_cuatrimestre(arch, parametros):
    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        variable = "CRED{}".format(get_str_cuatrimestre(cuatrimestre))
        arch.write(LINEA_GUARDAR.format(variable, '{}', variable) + ENTER)


def guardar_variables_horarios_cada_curso_por_materia(arch, parametros):
    horarios = parametros.horarios

    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        for materia in horarios:
            for curso in horarios[materia]:
                variable = "H_{}_{}_{}".format(materia, curso.id_curso, get_str_cuatrimestre(cuatrimestre))
                arch.write(LINEA_GUARDAR.format(variable, '{}', variable) + ENTER)


def guardar_variables_dias_y_franja_por_cuatrimestre(arch, parametros):
    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        for dia in parametros.dias:
            for franja in range(parametros.franja_minima, parametros.franja_maxima + 1):
                variable = "{}_{}_{}".format(dia, franja, get_str_cuatrimestre(cuatrimestre))
                arch.write(LINEA_GUARDAR.format(variable, '{}', variable) + ENTER)


def guardar_variables_horario_de_la_materia_en_dia_y_cuatrimestre(arch, parametros):
    horarios = parametros.horarios

    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        for materia in horarios:
            for curso in horarios[materia]:
                for c_horario in curso.horarios:

                    if not es_horario_valido_para_el_cuatrimestre(parametros, curso, cuatrimestre):
                        continue

                    dia = c_horario.dia
                    franjas = c_horario.get_franjas_utilizadas()
                    for franja in franjas:
                        variable = "R_{}_{}_{}_{}_{}".format(materia, curso.id_curso, dia, franja,
                                                             get_str_cuatrimestre(cuatrimestre))
                        arch.write(LINEA_GUARDAR.format(variable, '{}', variable) + ENTER)


def guardar_variables_horarios_de_materias(arch, parametros):
    guardar_variables_horarios_cada_curso_por_materia(arch, parametros)
    guardar_variables_dias_y_franja_por_cuatrimestre(arch, parametros)
    guardar_variables_horario_de_la_materia_en_dia_y_cuatrimestre(arch, parametros)


def guardar_variables_trabajo_final(arch, parametros):
    if not parametros.materia_trabajo_final:
        return

    guardar_variable_materia_trabajo_final_en_cuatri_j(arch, parametros)
    guardar_variable_numero_cuatrimestre_materia_trabajo_final(arch, parametros)


def guardar_variables(arch, parametros):
    arch.write("with open('{}', 'w') as arch:".format(parametros.nombre_archivo_resultados_pulp) + ENTER)
    arch.write(
        """    arch.write("{};{}".format({}) + "\\n")""".format("tiempo", '{}', "DURACION_EJECUCION_PULP") + ENTER)

    guardar_variable_materia_i_en_cuatri_j(arch, parametros)
    guardar_variable_numero_cuatrimestre_materia(arch, parametros)
    guardar_total_cuatrimestres(arch)
    guardar_variable_cantidad_creditos_por_cuatrimestre(arch, parametros)
    guardar_variables_horarios_de_materias(arch, parametros)
    guardar_variables_trabajo_final(arch, parametros)
