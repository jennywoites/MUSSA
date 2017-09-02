from Constantes import *

from Materia import Materia
from Horario import Horario
from Curso import Curso

from Generador_Restricciones import generar_restricciones
from Generador_Variables import definir_variables

from MateriasDAO import get_materias, get_plan_carrera
from HorariosDAO import get_horarios, get_horarios_no_permitidos

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
    arch.write("# Definicion de la funcion objetivo a minimizar. Es el max de los valores de los cuatrimestres MAX(CA, CB..)" + ENTER + ENTER)
    arch.write("prob += y" + ENTER + ENTER)


def resolver_problema(arch):
    arch.write("# Resolucion del problema" + ENTER + ENTER)
    arch.write("tiempo_inicial = time()" + ENTER)
    arch.write("status = prob.solve(GLPK(msg=0))" + ENTER + ENTER)
    arch.write("tiempo_final = time()" + ENTER)
    arch.write("print('Duracion: {}'.format(tiempo_final - tiempo_inicial))" + ENTER)


def imprimir_resultados(arch, plan, horarios):
    arch.write("# Impresion de resultados por pantalla" + ENTER + ENTER)
    arch.write("print('Total de cuatrimestres: {}'.format(value(y)))" + ENTER + ENTER)
    
    arch.write("plan_final = []" + ENTER)
    arch.write("for i in range(value(y)):" + ENTER)
    arch.write("    plan_final.append([])" + ENTER)

    arch.write("msj = 'Materia {} se hace en el cuatrimestre {}'" + ENTER)
    for materia in plan:
        arch.write("plan_final[value(C{})-1].append('{}')".format(materia, materia) + ENTER)
        arch.write("print(msj.format('{}', value(C{})))".format(materia, materia) + ENTER)
    arch.write("print(plan_final)" + ENTER)

    arch.write("msj = 'Cuatrimestre: {} - Creditos acumulados: {}'" + ENTER)
    for i in range(MAX_CUATRIMESTRES_TOTALES):
        arch.write("print(msj.format({}, value(CRED{})))".format(i, i) + ENTER)

    for materia in horarios:
        for i in range(1, MAX_CUATRIMESTRES_TOTALES + 1):
            for curso in horarios[materia]:
                H = "H_{}_{}_{}".format(materia, curso.nombre, i)
                arch.write("if value({}):".format(H) + ENTER)
                arch.write("    print('Valor de {} en cuatrimestre {}: {}'.format(value({})))".format(H, i, "{}", H) + ENTER)


def generar_codigo(arch, plan, materias, horarios, horarios_no_permitidos):
    importar_pulp(arch)
    importar_time(arch)
    definir_variables(arch, plan, horarios)
    definir_problema_minimizacion(arch)
    generar_restricciones(arch, plan, materias, horarios, horarios_no_permitidos)
    definir_funcion_objetivo(arch)    
    resolver_problema(arch)
    imprimir_resultados(arch, plan, horarios)


def main():
    plan_carrera = get_plan_carrera()
    materias = get_materias()
    horarios = get_horarios()
    horarios_no_permitidos = get_horarios_no_permitidos()

    with open("pulp_001.py", "w") as f:
        generar_codigo(f, plan_carrera, materias, horarios, horarios_no_permitidos)        


main()
