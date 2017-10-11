from Constantes import *

from my_utils import get_str_cuatrimestre

LINEA_GUARDAR = """    arch.write("{};{}".format(value({})) + "\\n")"""


def guardar_variable_materia_i_en_cuatri_j(arch, parametros):
    for materia in parametros.plan:
        for cuatrimestre in range(1,parametros.max_cuatrimestres + 1):
            variable = "Y_{}_{}".format(materia, get_str_cuatrimestre(cuatrimestre))
            arch.write(LINEA_GUARDAR.format(variable, '{}', variable) + ENTER)


def guardar_variable_numero_cuatrimestre_materia(arch, parametros):
    for materia in parametros.plan:
        variable = "C{}".format(materia)
        arch.write(LINEA_GUARDAR.format(variable, '{}', variable) + ENTER)


def guardar_total_cuatrimestres(arch):
    arch.write(LINEA_GUARDAR.format("TOTAL_CUATRIMESTRES", '{}', "TOTAL_CUATRIMESTRES") + ENTER)


def guardar_variable_cantidad_creditos_por_cuatrimestre(arch, parametros):
    for cuatrimestre in range(1,parametros.max_cuatrimestres + 1):
        variable = "CRED{}".format(get_str_cuatrimestre(cuatrimestre))
        arch.write(LINEA_GUARDAR.format(variable, '{}', variable) + ENTER)


def guardar_variables_horarios_cada_curso_por_materia(arch, parametros):
    horarios = parametros.horarios

    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        for materia in horarios:
            for curso in horarios[materia]:
                variable = "H_{}_{}_{}".format(materia, curso.nombre, get_str_cuatrimestre(cuatrimestre))
                arch.write(LINEA_GUARDAR.format(variable, '{}', variable) + ENTER)


def guardar_variables_dias_y_franja_por_cuatrimestre(arch, parametros):    
    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        for dia in parametros.dias:
            for franja in range(parametros.franja_minima, parametros.franja_maxima +1):
                variable = "{}_{}_{}".format(dia, franja, get_str_cuatrimestre(cuatrimestre))
                arch.write(LINEA_GUARDAR.format(variable, '{}', variable) + ENTER)


def guardar_variables_horario_de_la_materia_en_dia_y_cuatrimestre(arch, parametros):
    horarios = parametros.horarios

    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        for materia in horarios:
            for curso in horarios[materia]:
                for c_horario in curso.horarios:
                    dia = c_horario.dia
                    franjas = c_horario.get_franjas_utilizadas()
                    for franja in franjas:
                        variable= "R_{}_{}_{}_{}_{}".format(materia, curso.nombre, dia, franja, get_str_cuatrimestre(cuatrimestre))
                        arch.write(LINEA_GUARDAR.format(variable, '{}', variable) + ENTER)


def guardar_variables_horarios_de_materias(arch, parametros):
    guardar_variables_horarios_cada_curso_por_materia(arch, parametros)
    guardar_variables_dias_y_franja_por_cuatrimestre(arch, parametros)
    guardar_variables_horario_de_la_materia_en_dia_y_cuatrimestre(arch, parametros)


def guardar_variables_esta_el_dia_ocupado_en_un_cuatrimestre(arch, parametros):
    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        for dia in parametros.dias:
            variable = "OCUPADO_{}_{}".format(dia, get_str_cuatrimestre(cuatrimestre))
            arch.write(LINEA_GUARDAR.format(variable, '{}', variable) + ENTER)


def guardar_variables_maximo_y_minimo_numero_franja_ocupada_por_dia_por_cuatrimestre(arch, parametros):
    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        for dia in parametros.dias:
            variable_max = "MAXIMA_FRANJA_{}_{}".format(dia, get_str_cuatrimestre(cuatrimestre))
            variable_min = "MINIMA_FRANJA_{}_{}".format(dia, get_str_cuatrimestre(cuatrimestre))
            arch.write(LINEA_GUARDAR.format(variable_max, '{}', variable_max) + ENTER)
            arch.write(LINEA_GUARDAR.format(variable_min, '{}', variable_min) + ENTER)


def guardar_variables_horas_libres_entre_materias_por_dia_por_cuatrimestre(arch, parametros):
    for cuatrimestre in range(1, parametros.max_cuatrimestres + 1):
        for dia in parametros.dias:
            variable = "HORAS_LIBRES_{}_{}".format(dia, get_str_cuatrimestre(cuatrimestre))
            arch.write(LINEA_GUARDAR.format(variable, '{}', variable) + ENTER)


def guardar_variable_horas_libres_totales(arch):
    variable = "HORAS_LIBRES_TOTALES"
    arch.write(LINEA_GUARDAR.format(variable, '{}', variable) + ENTER)


def guardar_variables_horas_libres_entre_materias(arch, parametros):
    guardar_variables_esta_el_dia_ocupado_en_un_cuatrimestre(arch, parametros)
    guardar_variables_maximo_y_minimo_numero_franja_ocupada_por_dia_por_cuatrimestre(arch, parametros)
    guardar_variables_horas_libres_entre_materias_por_dia_por_cuatrimestre(arch, parametros)
    guardar_variable_horas_libres_totales(arch)

def guardar_variables(arch, parametros):
    arch.write("with open('{}', 'w') as arch:".format(parametros.nombre_archivo_resultados_pulp) + ENTER)
    arch.write("""    arch.write("{};{}".format({}) + "\\n")""".format("tiempo", '{}', "DURACION_EJECUCION_PULP") + ENTER)

    guardar_variable_materia_i_en_cuatri_j(arch, parametros)
    guardar_variable_numero_cuatrimestre_materia(arch, parametros)
    guardar_total_cuatrimestres(arch)
    guardar_variable_cantidad_creditos_por_cuatrimestre(arch, parametros)    
    guardar_variables_horarios_de_materias(arch, parametros)
    guardar_variables_horas_libres_entre_materias(arch, parametros)