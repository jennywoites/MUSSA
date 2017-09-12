from Constantes import *

from ParametrosDAO import Parametros

from Materia import Materia
from Horario import Horario
from Curso import Curso

from Generador_Restricciones import generar_restricciones
from Generador_Variables import definir_variables

#############################################################################################
def importar_pulp(arch):
    arch.write("from pulp import *" + ENTER)
    arch.write(ENTER + ENTER)


def importar_time(arch):
    arch.write("from time import time" + ENTER)
    arch.write(ENTER + ENTER)


def definir_problema_minimizacion(arch):
    arch.write("# Definicion del problema" + ENTER + ENTER)
    arch.write("prob = LpProblem('{}', LpMinimize)".format(NOMBRE_PROBLEMA) + ENTER)
    arch.write(ENTER + ENTER)


def definir_funcion_objetivo(arch):
    arch.write("# Definicion de la funcion objetivo a minimizar." + ENTER + ENTER)
    funciones = [] #[(factor, variable)]
    funciones.append((1, "TOTAL_CUATRIMESTRES"))
    funciones.append((1,"HORAS_LIBRES_TOTALES"))
    
    ecuacion = "prob += "
    for (factor, variable) in funciones:
        ecuacion += str(factor) + "*" + variable + " + "

    ecuacion = ecuacion[:-3]
    arch.write(ecuacion + ENTER + ENTER)


def resolver_problema(arch):
    arch.write("# Resolucion del problema" + ENTER + ENTER)
    arch.write("tiempo_inicial = time()" + ENTER)
    arch.write("status = prob.solve(GLPK(msg=0))" + ENTER + ENTER)
    arch.write("tiempo_final = time()" + ENTER)
    arch.write("print('Duracion: {}'.format(tiempo_final - tiempo_inicial))" + ENTER)


def imprimir_resultados(arch, parametros):
    plan = parametros.plan
    horarios = parametros.horarios

    arch.write("# Impresion de resultados por pantalla" + ENTER + ENTER)
    arch.write("print('Total de cuatrimestres: {}'.format(value(TOTAL_CUATRIMESTRES)))" + ENTER + ENTER)
    
    imprimir_materias_plan(arch, plan)

    arch.write("print('Total de horas libres: {}'.format(value(HORAS_LIBRES_TOTALES)))" + ENTER)

    arch.write("msj = 'Cuatrimestre: {} - Creditos acumulados: {}'" + ENTER)
    for i in range(MAX_CUATRIMESTRES_TOTALES):
        arch.write("print(msj.format({}, value(CRED{})))".format(i, i) + ENTER)

    imprimir_datos_franjas(arch)

    for materia in horarios:
        for i in range(1, MAX_CUATRIMESTRES_TOTALES + 1):
            for curso in horarios[materia]:
                H = "H_{}_{}_{}".format(materia, curso.nombre, i)
                arch.write("if value({}):".format(H) + ENTER)
                arch.write("    print('Valor de {} en cuatrimestre {}: {}'.format(value({})))".format(H, i, "{}", H) + ENTER)


def imprimir_datos_franjas(arch):
    msj = "print('{}: {}'.format(value({})))"
    for cuatri in range(1, MAX_CUATRIMESTRES_TOTALES+1):
        for dia in DIAS:
            ocupado = "OCUPADO_{}_{}".format(dia, cuatri)
            arch.write(msj.format(ocupado, '{}', ocupado) + ENTER)

            maxima_f = "MAXIMA_FRANJA_{}_{}".format(dia, cuatri)
            arch.write(msj.format(maxima_f, '{}', maxima_f) + ENTER)

            minima_f = "MINIMA_FRANJA_{}_{}".format(dia, cuatri)
            arch.write(msj.format(minima_f, '{}', minima_f) + ENTER)

            horas_libres = "HORAS_LIBRES_{}_{}".format(dia, cuatri)
            arch.write(msj.format(horas_libres, '{}', horas_libres) + ENTER)

    arch.write(msj.format("HORAS_LIBRES_TOTALES", '{}', "HORAS_LIBRES_TOTALES") + ENTER)

    for cuatri in range(1, MAX_CUATRIMESTRES_TOTALES+1):
        for dia in DIAS:
            for franja in range(FRANJA_MIN, FRANJA_MAX +1):
                variable = "{}_{}_{}".format(dia, franja, cuatri)
                arch.write("print('{}: {}'.format(value({})))".format(variable, '{}', variable) + ENTER)


def imprimir_materias_plan(arch, plan):
    arch.write("plan_final = []" + ENTER)
    arch.write("for i in range(value(TOTAL_CUATRIMESTRES)):" + ENTER)
    arch.write("    plan_final.append([])" + ENTER)

    arch.write("msj = 'Materia {} se hace en el cuatrimestre {}'" + ENTER)
    for materia in plan:
        cuatri = "value(C{})".format(materia)
        arch.write("if {} > 0:".format(cuatri) + ENTER)
        arch.write("    plan_final[{}-1].append('{}')".format(cuatri, materia) + ENTER)
        arch.write("    print(msj.format('{}', {}))".format(materia, cuatri) + ENTER)
        arch.write("else:" + ENTER)
        arch.write("    print('La materia {} no se hace')".format(materia) + ENTER)
    arch.write("print(plan_final)" + ENTER)


def generar_codigo(arch, parametros):
    importar_pulp(arch)
    importar_time(arch)
    definir_variables(arch, parametros)
    definir_problema_minimizacion(arch)
    generar_restricciones(arch, parametros)
    definir_funcion_objetivo(arch)    
    resolver_problema(arch)
    imprimir_resultados(arch, parametros)


def main():
    parametros = Parametros()
    with open("pulp_001.py", "w") as f:
        generar_codigo(f, parametros)        


main()
