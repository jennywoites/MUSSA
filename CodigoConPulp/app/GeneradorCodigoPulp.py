from Constantes import *

from ParametrosDAO import Parametros

from GeneradorRestricciones import generar_restricciones
from GeneradorVariables import definir_variables
from ResultadosPulpDAO import guardar_variables

import sys
sys.path.append("../app/modelos")

from Materia import Materia
from Horario import Horario
from Curso import Curso


#############################################################################################
def importar_pulp(arch):
    arch.write("from pulp import *" + ENTER)


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


def escribir_funcion_de_conversion_de_tiempo(arch):
    arch.write("def convertir_tiempo(tiempo):" + ENTER)
    arch.write("    segundos = tiempo" + ENTER)
    arch.write("    minutos = segundos // 60" + ENTER)
    arch.write("    segundos = tiempo - minutos * 60" + ENTER)
    arch.write("    horas = minutos // 60" + ENTER)
    arch.write("    minutos = minutos - horas * 60" + ENTER)
    arch.write("    msj = ''" + ENTER)
    arch.write("    if horas > 0:" + ENTER)
    arch.write("        msj += 'Horas: {} '.format(horas)" + ENTER)
    arch.write("    if minutos > 0:" + ENTER)
    arch.write("        msj += 'Minutos: {} '.format(minutos)" + ENTER)
    arch.write("    msj += 'Segundos: {0:.2f}'.format(segundos)" + ENTER)
    arch.write("    return msj" + ENTER + ENTER)


def resolver_problema(arch):
    arch.write("# Resolucion del problema" + ENTER + ENTER)
    arch.write("tiempo_inicial = time()" + ENTER)
    arch.write("status = prob.solve(GLPK(msg=0))" + ENTER)
    arch.write("tiempo_final = time()" + ENTER)

    arch.write("DURACION_EJECUCION_PULP = tiempo_final - tiempo_inicial" + ENTER)
    arch.write("print('Duracion: {}'.format(convertir_tiempo(DURACION_EJECUCION_PULP)))" + ENTER + ENTER)


def generar_codigo(arch, parametros):
    importar_pulp(arch)
    importar_time(arch)
    escribir_funcion_de_conversion_de_tiempo(arch)
    definir_variables(arch, parametros)
    definir_problema_minimizacion(arch)
    generar_restricciones(arch, parametros)
    definir_funcion_objetivo(arch)    
    resolver_problema(arch)
    guardar_variables(arch, parametros)


def generar_archivo_pulp(parametros):
    ruta = parametros.nombre_archivo_pulp
    with open(ruta, "w") as f:
        generar_codigo(f, parametros)        


def main():
    parametros = Parametros()
    generar_archivo_pulp(parametros)


if __name__ == "__main__":
    main()