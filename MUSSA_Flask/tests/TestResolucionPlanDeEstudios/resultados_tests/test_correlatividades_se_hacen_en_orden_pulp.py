from pulp import *
from time import time


def convertir_tiempo(tiempo):
    segundos = tiempo
    minutos = segundos // 60
    segundos = tiempo - minutos * 60
    horas = minutos // 60
    minutos = minutos - horas * 60
    msj = ''
    if horas > 0:
        msj += 'Horas: {} '.format(horas)
    if minutos > 0:
        msj += 'Minutos: {} '.format(minutos)
    msj += 'Segundos: {0:.2f}'.format(segundos)
    return msj

#Yij: La materia i se realiza en el cuatrimestre j

Y_A_01 = LpVariable(name='Y_A_01', cat='Binary')
Y_A_02 = LpVariable(name='Y_A_02', cat='Binary')
Y_A_03 = LpVariable(name='Y_A_03', cat='Binary')
Y_C_01 = LpVariable(name='Y_C_01', cat='Binary')
Y_C_02 = LpVariable(name='Y_C_02', cat='Binary')
Y_C_03 = LpVariable(name='Y_C_03', cat='Binary')
Y_B_01 = LpVariable(name='Y_B_01', cat='Binary')
Y_B_02 = LpVariable(name='Y_B_02', cat='Binary')
Y_B_03 = LpVariable(name='Y_B_03', cat='Binary')


#Ci: Numero de cuatrimestre en que se hace la materia i. Ejemplo, si Ci=3 es que la materia i se hace el cuatrimestre numero 3

CA = LpVariable(name='CA', lowBound=0, upBound=3, cat='Integer')
CC = LpVariable(name='CC', lowBound=0, upBound=3, cat='Integer')
CB = LpVariable(name='CB', lowBound=0, upBound=3, cat='Integer')


#TOTAL_CUATRIMESTRES: Total de cuatrimestres a cursar. Utilizada para escribir el maximo entre Ci MAX(CA, CB..)

TOTAL_CUATRIMESTRES = LpVariable(name='TOTAL_CUATRIMESTRES', lowBound=0, upBound=3, cat='Integer')
#CREDi: Cantidad de creditos al final del cuatrimestre i

CRED01 = LpVariable(name='CRED01', lowBound=0, upBound=10000, cat='Integer')
CRED02 = LpVariable(name='CRED02', lowBound=0, upBound=10000, cat='Integer')
CRED03 = LpVariable(name='CRED03', lowBound=0, upBound=10000, cat='Integer')


#H_{materia i}_{nombre del curso j}_{cuatrimestre k}: La materia i se cursa en el curso j en el cuatrimestre k

H_A_Curso1A_01 = LpVariable(name='H_A_Curso1A_01', cat='Binary')
H_C_Curso1C_01 = LpVariable(name='H_C_Curso1C_01', cat='Binary')
H_B_Curso1B_01 = LpVariable(name='H_B_Curso1B_01', cat='Binary')
H_A_Curso1A_02 = LpVariable(name='H_A_Curso1A_02', cat='Binary')
H_C_Curso1C_02 = LpVariable(name='H_C_Curso1C_02', cat='Binary')
H_B_Curso1B_02 = LpVariable(name='H_B_Curso1B_02', cat='Binary')
H_A_Curso1A_03 = LpVariable(name='H_A_Curso1A_03', cat='Binary')
H_C_Curso1C_03 = LpVariable(name='H_C_Curso1C_03', cat='Binary')
H_B_Curso1B_03 = LpVariable(name='H_B_Curso1B_03', cat='Binary')


#{Dia i}_{Franja j}_{cuatrimestre k}: El dia i (LUNES; MARTES, etc) en la franja horaria j en el cuatrimestre k se esta cursando

LUNES_1_01 = LpVariable(name='LUNES_1_01', cat='Binary')
LUNES_2_01 = LpVariable(name='LUNES_2_01', cat='Binary')
LUNES_3_01 = LpVariable(name='LUNES_3_01', cat='Binary')
LUNES_4_01 = LpVariable(name='LUNES_4_01', cat='Binary')
LUNES_5_01 = LpVariable(name='LUNES_5_01', cat='Binary')
LUNES_6_01 = LpVariable(name='LUNES_6_01', cat='Binary')
LUNES_7_01 = LpVariable(name='LUNES_7_01', cat='Binary')
LUNES_8_01 = LpVariable(name='LUNES_8_01', cat='Binary')
LUNES_9_01 = LpVariable(name='LUNES_9_01', cat='Binary')
LUNES_10_01 = LpVariable(name='LUNES_10_01', cat='Binary')
LUNES_1_02 = LpVariable(name='LUNES_1_02', cat='Binary')
LUNES_2_02 = LpVariable(name='LUNES_2_02', cat='Binary')
LUNES_3_02 = LpVariable(name='LUNES_3_02', cat='Binary')
LUNES_4_02 = LpVariable(name='LUNES_4_02', cat='Binary')
LUNES_5_02 = LpVariable(name='LUNES_5_02', cat='Binary')
LUNES_6_02 = LpVariable(name='LUNES_6_02', cat='Binary')
LUNES_7_02 = LpVariable(name='LUNES_7_02', cat='Binary')
LUNES_8_02 = LpVariable(name='LUNES_8_02', cat='Binary')
LUNES_9_02 = LpVariable(name='LUNES_9_02', cat='Binary')
LUNES_10_02 = LpVariable(name='LUNES_10_02', cat='Binary')
LUNES_1_03 = LpVariable(name='LUNES_1_03', cat='Binary')
LUNES_2_03 = LpVariable(name='LUNES_2_03', cat='Binary')
LUNES_3_03 = LpVariable(name='LUNES_3_03', cat='Binary')
LUNES_4_03 = LpVariable(name='LUNES_4_03', cat='Binary')
LUNES_5_03 = LpVariable(name='LUNES_5_03', cat='Binary')
LUNES_6_03 = LpVariable(name='LUNES_6_03', cat='Binary')
LUNES_7_03 = LpVariable(name='LUNES_7_03', cat='Binary')
LUNES_8_03 = LpVariable(name='LUNES_8_03', cat='Binary')
LUNES_9_03 = LpVariable(name='LUNES_9_03', cat='Binary')
LUNES_10_03 = LpVariable(name='LUNES_10_03', cat='Binary')


#R_{materia}_{nombre curso}_{dia}_{franja}_{cuatrimestre}: El horario para la materia y curso en ese cuatrimestre esta habilitado

R_A_Curso1A_LUNES_1_01 = LpVariable(name='R_A_Curso1A_LUNES_1_01', cat='Binary')
R_A_Curso1A_LUNES_2_01 = LpVariable(name='R_A_Curso1A_LUNES_2_01', cat='Binary')
R_C_Curso1C_LUNES_5_01 = LpVariable(name='R_C_Curso1C_LUNES_5_01', cat='Binary')
R_C_Curso1C_LUNES_6_01 = LpVariable(name='R_C_Curso1C_LUNES_6_01', cat='Binary')
R_B_Curso1B_LUNES_3_01 = LpVariable(name='R_B_Curso1B_LUNES_3_01', cat='Binary')
R_B_Curso1B_LUNES_4_01 = LpVariable(name='R_B_Curso1B_LUNES_4_01', cat='Binary')
R_A_Curso1A_LUNES_1_02 = LpVariable(name='R_A_Curso1A_LUNES_1_02', cat='Binary')
R_A_Curso1A_LUNES_2_02 = LpVariable(name='R_A_Curso1A_LUNES_2_02', cat='Binary')
R_C_Curso1C_LUNES_5_02 = LpVariable(name='R_C_Curso1C_LUNES_5_02', cat='Binary')
R_C_Curso1C_LUNES_6_02 = LpVariable(name='R_C_Curso1C_LUNES_6_02', cat='Binary')
R_B_Curso1B_LUNES_3_02 = LpVariable(name='R_B_Curso1B_LUNES_3_02', cat='Binary')
R_B_Curso1B_LUNES_4_02 = LpVariable(name='R_B_Curso1B_LUNES_4_02', cat='Binary')
R_A_Curso1A_LUNES_1_03 = LpVariable(name='R_A_Curso1A_LUNES_1_03', cat='Binary')
R_A_Curso1A_LUNES_2_03 = LpVariable(name='R_A_Curso1A_LUNES_2_03', cat='Binary')
R_C_Curso1C_LUNES_5_03 = LpVariable(name='R_C_Curso1C_LUNES_5_03', cat='Binary')
R_C_Curso1C_LUNES_6_03 = LpVariable(name='R_C_Curso1C_LUNES_6_03', cat='Binary')
R_B_Curso1B_LUNES_3_03 = LpVariable(name='R_B_Curso1B_LUNES_3_03', cat='Binary')
R_B_Curso1B_LUNES_4_03 = LpVariable(name='R_B_Curso1B_LUNES_4_03', cat='Binary')


# Definicion del problema

prob = LpProblem('Jenny_Calculo_plan_carrera', LpMinimize)


# La materia i se debe cursar en un unico cuatrimestre. Ademas, si es obligatoria, debe cursarse si o si.

prob += (Y_A_01 + Y_A_02 + Y_A_03 >= 1)
prob += (Y_A_01 + Y_A_02 + Y_A_03 <= 1)

prob += (Y_C_01 + Y_C_02 + Y_C_03 >= 1)
prob += (Y_C_01 + Y_C_02 + Y_C_03 <= 1)

prob += (Y_B_01 + Y_B_02 + Y_B_03 >= 1)
prob += (Y_B_01 + Y_B_02 + Y_B_03 <= 1)


# Numero de cuatrimestre en que es cursada la materia

prob += (1*Y_A_01 + 2*Y_A_02 + 3*Y_A_03<= CA)
prob += (1*Y_A_01 + 2*Y_A_02 + 3*Y_A_03>= CA)

prob += (1*Y_C_01 + 2*Y_C_02 + 3*Y_C_03<= CC)
prob += (1*Y_C_01 + 2*Y_C_02 + 3*Y_C_03>= CC)

prob += (1*Y_B_01 + 2*Y_B_02 + 3*Y_B_03<= CB)
prob += (1*Y_B_01 + 2*Y_B_02 + 3*Y_B_03>= CB)


# Los cuatrimestres de las correlativas deben ser menores (cuando la materia se cursa)

prob += (CC >= CA + 1)


# La cantidad de materias por cuatrimestre no puede superar un valor maximo

prob += (Y_A_01 + Y_C_01 + Y_B_01 <= 3)
prob += (Y_A_02 + Y_C_02 + Y_B_02 <= 3)
prob += (Y_A_03 + Y_C_03 + Y_B_03 <= 3)


#TOTAL_CUATRIMESTRES es el maximo de los Ci

prob += (TOTAL_CUATRIMESTRES >= 0)

prob += (CA <= TOTAL_CUATRIMESTRES)
prob += (-CA <= TOTAL_CUATRIMESTRES)

prob += (CC <= TOTAL_CUATRIMESTRES)
prob += (-CC <= TOTAL_CUATRIMESTRES)

prob += (CB <= TOTAL_CUATRIMESTRES)
prob += (-CB <= TOTAL_CUATRIMESTRES)


# Calculo de creditos al terminar cada cuatrimestre

prob += (1*Y_A_01 + 1*Y_C_01 + 1*Y_B_01  <= CRED01)
prob += (1*Y_A_01 + 1*Y_C_01 + 1*Y_B_01  >= CRED01)
prob += (1*Y_A_02 + 1*Y_C_02 + 1*Y_B_02 + CRED01 <= CRED02)
prob += (1*Y_A_02 + 1*Y_C_02 + 1*Y_B_02 + CRED01 >= CRED02)
prob += (1*Y_A_03 + 1*Y_C_03 + 1*Y_B_03 + CRED02 <= CRED03)
prob += (1*Y_A_03 + 1*Y_C_03 + 1*Y_B_03 + CRED02 >= CRED03)

# Restricciones sobre aquellas materias que requieren creditos minimos para poder cursar


#Si la materia se cursa en ese cuatrimestre en ese curso en particular, entonces se deben cursar todos los horarios del mismo

prob += (H_A_Curso1A_01 <= R_A_Curso1A_LUNES_1_01)
prob += (H_A_Curso1A_01 >= R_A_Curso1A_LUNES_1_01)
prob += (H_A_Curso1A_01 <= R_A_Curso1A_LUNES_2_01)
prob += (H_A_Curso1A_01 >= R_A_Curso1A_LUNES_2_01)
prob += (H_C_Curso1C_01 <= R_C_Curso1C_LUNES_5_01)
prob += (H_C_Curso1C_01 >= R_C_Curso1C_LUNES_5_01)
prob += (H_C_Curso1C_01 <= R_C_Curso1C_LUNES_6_01)
prob += (H_C_Curso1C_01 >= R_C_Curso1C_LUNES_6_01)
prob += (H_B_Curso1B_01 <= R_B_Curso1B_LUNES_3_01)
prob += (H_B_Curso1B_01 >= R_B_Curso1B_LUNES_3_01)
prob += (H_B_Curso1B_01 <= R_B_Curso1B_LUNES_4_01)
prob += (H_B_Curso1B_01 >= R_B_Curso1B_LUNES_4_01)
prob += (H_A_Curso1A_02 <= R_A_Curso1A_LUNES_1_02)
prob += (H_A_Curso1A_02 >= R_A_Curso1A_LUNES_1_02)
prob += (H_A_Curso1A_02 <= R_A_Curso1A_LUNES_2_02)
prob += (H_A_Curso1A_02 >= R_A_Curso1A_LUNES_2_02)
prob += (H_C_Curso1C_02 <= R_C_Curso1C_LUNES_5_02)
prob += (H_C_Curso1C_02 >= R_C_Curso1C_LUNES_5_02)
prob += (H_C_Curso1C_02 <= R_C_Curso1C_LUNES_6_02)
prob += (H_C_Curso1C_02 >= R_C_Curso1C_LUNES_6_02)
prob += (H_B_Curso1B_02 <= R_B_Curso1B_LUNES_3_02)
prob += (H_B_Curso1B_02 >= R_B_Curso1B_LUNES_3_02)
prob += (H_B_Curso1B_02 <= R_B_Curso1B_LUNES_4_02)
prob += (H_B_Curso1B_02 >= R_B_Curso1B_LUNES_4_02)
prob += (H_A_Curso1A_03 <= R_A_Curso1A_LUNES_1_03)
prob += (H_A_Curso1A_03 >= R_A_Curso1A_LUNES_1_03)
prob += (H_A_Curso1A_03 <= R_A_Curso1A_LUNES_2_03)
prob += (H_A_Curso1A_03 >= R_A_Curso1A_LUNES_2_03)
prob += (H_C_Curso1C_03 <= R_C_Curso1C_LUNES_5_03)
prob += (H_C_Curso1C_03 >= R_C_Curso1C_LUNES_5_03)
prob += (H_C_Curso1C_03 <= R_C_Curso1C_LUNES_6_03)
prob += (H_C_Curso1C_03 >= R_C_Curso1C_LUNES_6_03)
prob += (H_B_Curso1B_03 <= R_B_Curso1B_LUNES_3_03)
prob += (H_B_Curso1B_03 >= R_B_Curso1B_LUNES_3_03)
prob += (H_B_Curso1B_03 <= R_B_Curso1B_LUNES_4_03)
prob += (H_B_Curso1B_03 >= R_B_Curso1B_LUNES_4_03)

#No hay giratiempos: Solo puede cursarse una materia en un unico curso en el mismo horario

prob += (LUNES_1_01 <= R_A_Curso1A_LUNES_1_01)
prob += (LUNES_1_01 >= R_A_Curso1A_LUNES_1_01)
prob += (LUNES_2_01 <= R_A_Curso1A_LUNES_2_01)
prob += (LUNES_2_01 >= R_A_Curso1A_LUNES_2_01)
prob += (LUNES_3_01 <= R_B_Curso1B_LUNES_3_01)
prob += (LUNES_3_01 >= R_B_Curso1B_LUNES_3_01)
prob += (LUNES_4_01 <= R_B_Curso1B_LUNES_4_01)
prob += (LUNES_4_01 >= R_B_Curso1B_LUNES_4_01)
prob += (LUNES_5_01 <= R_C_Curso1C_LUNES_5_01)
prob += (LUNES_5_01 >= R_C_Curso1C_LUNES_5_01)
prob += (LUNES_6_01 <= R_C_Curso1C_LUNES_6_01)
prob += (LUNES_6_01 >= R_C_Curso1C_LUNES_6_01)
prob += (LUNES_7_01 <= 0)
prob += (LUNES_7_01 >= 0)
prob += (LUNES_8_01 <= 0)
prob += (LUNES_8_01 >= 0)
prob += (LUNES_9_01 <= 0)
prob += (LUNES_9_01 >= 0)
prob += (LUNES_10_01 <= 0)
prob += (LUNES_10_01 >= 0)
prob += (LUNES_1_02 <= R_A_Curso1A_LUNES_1_02)
prob += (LUNES_1_02 >= R_A_Curso1A_LUNES_1_02)
prob += (LUNES_2_02 <= R_A_Curso1A_LUNES_2_02)
prob += (LUNES_2_02 >= R_A_Curso1A_LUNES_2_02)
prob += (LUNES_3_02 <= R_B_Curso1B_LUNES_3_02)
prob += (LUNES_3_02 >= R_B_Curso1B_LUNES_3_02)
prob += (LUNES_4_02 <= R_B_Curso1B_LUNES_4_02)
prob += (LUNES_4_02 >= R_B_Curso1B_LUNES_4_02)
prob += (LUNES_5_02 <= R_C_Curso1C_LUNES_5_02)
prob += (LUNES_5_02 >= R_C_Curso1C_LUNES_5_02)
prob += (LUNES_6_02 <= R_C_Curso1C_LUNES_6_02)
prob += (LUNES_6_02 >= R_C_Curso1C_LUNES_6_02)
prob += (LUNES_7_02 <= 0)
prob += (LUNES_7_02 >= 0)
prob += (LUNES_8_02 <= 0)
prob += (LUNES_8_02 >= 0)
prob += (LUNES_9_02 <= 0)
prob += (LUNES_9_02 >= 0)
prob += (LUNES_10_02 <= 0)
prob += (LUNES_10_02 >= 0)
prob += (LUNES_1_03 <= R_A_Curso1A_LUNES_1_03)
prob += (LUNES_1_03 >= R_A_Curso1A_LUNES_1_03)
prob += (LUNES_2_03 <= R_A_Curso1A_LUNES_2_03)
prob += (LUNES_2_03 >= R_A_Curso1A_LUNES_2_03)
prob += (LUNES_3_03 <= R_B_Curso1B_LUNES_3_03)
prob += (LUNES_3_03 >= R_B_Curso1B_LUNES_3_03)
prob += (LUNES_4_03 <= R_B_Curso1B_LUNES_4_03)
prob += (LUNES_4_03 >= R_B_Curso1B_LUNES_4_03)
prob += (LUNES_5_03 <= R_C_Curso1C_LUNES_5_03)
prob += (LUNES_5_03 >= R_C_Curso1C_LUNES_5_03)
prob += (LUNES_6_03 <= R_C_Curso1C_LUNES_6_03)
prob += (LUNES_6_03 >= R_C_Curso1C_LUNES_6_03)
prob += (LUNES_7_03 <= 0)
prob += (LUNES_7_03 >= 0)
prob += (LUNES_8_03 <= 0)
prob += (LUNES_8_03 >= 0)
prob += (LUNES_9_03 <= 0)
prob += (LUNES_9_03 >= 0)
prob += (LUNES_10_03 <= 0)
prob += (LUNES_10_03 >= 0)

# Si la materia no se cursa ese cuatrimestre, entonces no puede cursarse en ninguno de los cursos de ese cuatrimestre

prob += (Y_A_01 >= H_A_Curso1A_01)
prob += (Y_C_01 >= H_C_Curso1C_01)
prob += (Y_B_01 >= H_B_Curso1B_01)
prob += (Y_A_02 >= H_A_Curso1A_02)
prob += (Y_C_02 >= H_C_Curso1C_02)
prob += (Y_B_02 >= H_B_Curso1B_02)
prob += (Y_A_03 >= H_A_Curso1A_03)
prob += (Y_C_03 >= H_C_Curso1C_03)
prob += (Y_B_03 >= H_B_Curso1B_03)

# La materia no puede cursarse en mas de un curso en el cuatrimestre

prob += (Y_A_01 <= H_A_Curso1A_01)
prob += (Y_A_01 >= H_A_Curso1A_01)
prob += (Y_C_01 <= H_C_Curso1C_01)
prob += (Y_C_01 >= H_C_Curso1C_01)
prob += (Y_B_01 <= H_B_Curso1B_01)
prob += (Y_B_01 >= H_B_Curso1B_01)
prob += (Y_A_02 <= H_A_Curso1A_02)
prob += (Y_A_02 >= H_A_Curso1A_02)
prob += (Y_C_02 <= H_C_Curso1C_02)
prob += (Y_C_02 >= H_C_Curso1C_02)
prob += (Y_B_02 <= H_B_Curso1B_02)
prob += (Y_B_02 >= H_B_Curso1B_02)
prob += (Y_A_03 <= H_A_Curso1A_03)
prob += (Y_A_03 >= H_A_Curso1A_03)
prob += (Y_C_03 <= H_C_Curso1C_03)
prob += (Y_C_03 >= H_C_Curso1C_03)
prob += (Y_B_03 <= H_B_Curso1B_03)
prob += (Y_B_03 >= H_B_Curso1B_03)

# Definicion de la funcion objetivo a minimizar.

prob += 10*TOTAL_CUATRIMESTRES

# Resolucion del problema

tiempo_inicial = time()
status = prob.solve(COIN(threads=2, msg=True))
tiempo_final = time()
DURACION_EJECUCION_PULP = tiempo_final - tiempo_inicial
print('Duracion: {}'.format(convertir_tiempo(DURACION_EJECUCION_PULP)))

with open('resultados_tests/test_correlatividades_se_hacen_en_orden_resultados_pulp.py', 'w') as arch:
    arch.write("tiempo;{}".format(DURACION_EJECUCION_PULP) + "\n")
    arch.write("Y_A_01;{}".format(int(value(Y_A_01))) + "\n")
    arch.write("Y_A_02;{}".format(int(value(Y_A_02))) + "\n")
    arch.write("Y_A_03;{}".format(int(value(Y_A_03))) + "\n")
    arch.write("Y_C_01;{}".format(int(value(Y_C_01))) + "\n")
    arch.write("Y_C_02;{}".format(int(value(Y_C_02))) + "\n")
    arch.write("Y_C_03;{}".format(int(value(Y_C_03))) + "\n")
    arch.write("Y_B_01;{}".format(int(value(Y_B_01))) + "\n")
    arch.write("Y_B_02;{}".format(int(value(Y_B_02))) + "\n")
    arch.write("Y_B_03;{}".format(int(value(Y_B_03))) + "\n")
    arch.write("CA;{}".format(int(value(CA))) + "\n")
    arch.write("CC;{}".format(int(value(CC))) + "\n")
    arch.write("CB;{}".format(int(value(CB))) + "\n")
    arch.write("TOTAL_CUATRIMESTRES;{}".format(int(value(TOTAL_CUATRIMESTRES))) + "\n")
    arch.write("CRED01;{}".format(int(value(CRED01))) + "\n")
    arch.write("CRED02;{}".format(int(value(CRED02))) + "\n")
    arch.write("CRED03;{}".format(int(value(CRED03))) + "\n")
    arch.write("H_A_Curso1A_01;{}".format(int(value(H_A_Curso1A_01))) + "\n")
    arch.write("H_C_Curso1C_01;{}".format(int(value(H_C_Curso1C_01))) + "\n")
    arch.write("H_B_Curso1B_01;{}".format(int(value(H_B_Curso1B_01))) + "\n")
    arch.write("H_A_Curso1A_02;{}".format(int(value(H_A_Curso1A_02))) + "\n")
    arch.write("H_C_Curso1C_02;{}".format(int(value(H_C_Curso1C_02))) + "\n")
    arch.write("H_B_Curso1B_02;{}".format(int(value(H_B_Curso1B_02))) + "\n")
    arch.write("H_A_Curso1A_03;{}".format(int(value(H_A_Curso1A_03))) + "\n")
    arch.write("H_C_Curso1C_03;{}".format(int(value(H_C_Curso1C_03))) + "\n")
    arch.write("H_B_Curso1B_03;{}".format(int(value(H_B_Curso1B_03))) + "\n")
    arch.write("LUNES_1_01;{}".format(int(value(LUNES_1_01))) + "\n")
    arch.write("LUNES_2_01;{}".format(int(value(LUNES_2_01))) + "\n")
    arch.write("LUNES_3_01;{}".format(int(value(LUNES_3_01))) + "\n")
    arch.write("LUNES_4_01;{}".format(int(value(LUNES_4_01))) + "\n")
    arch.write("LUNES_5_01;{}".format(int(value(LUNES_5_01))) + "\n")
    arch.write("LUNES_6_01;{}".format(int(value(LUNES_6_01))) + "\n")
    arch.write("LUNES_7_01;{}".format(int(value(LUNES_7_01))) + "\n")
    arch.write("LUNES_8_01;{}".format(int(value(LUNES_8_01))) + "\n")
    arch.write("LUNES_9_01;{}".format(int(value(LUNES_9_01))) + "\n")
    arch.write("LUNES_10_01;{}".format(int(value(LUNES_10_01))) + "\n")
    arch.write("LUNES_1_02;{}".format(int(value(LUNES_1_02))) + "\n")
    arch.write("LUNES_2_02;{}".format(int(value(LUNES_2_02))) + "\n")
    arch.write("LUNES_3_02;{}".format(int(value(LUNES_3_02))) + "\n")
    arch.write("LUNES_4_02;{}".format(int(value(LUNES_4_02))) + "\n")
    arch.write("LUNES_5_02;{}".format(int(value(LUNES_5_02))) + "\n")
    arch.write("LUNES_6_02;{}".format(int(value(LUNES_6_02))) + "\n")
    arch.write("LUNES_7_02;{}".format(int(value(LUNES_7_02))) + "\n")
    arch.write("LUNES_8_02;{}".format(int(value(LUNES_8_02))) + "\n")
    arch.write("LUNES_9_02;{}".format(int(value(LUNES_9_02))) + "\n")
    arch.write("LUNES_10_02;{}".format(int(value(LUNES_10_02))) + "\n")
    arch.write("LUNES_1_03;{}".format(int(value(LUNES_1_03))) + "\n")
    arch.write("LUNES_2_03;{}".format(int(value(LUNES_2_03))) + "\n")
    arch.write("LUNES_3_03;{}".format(int(value(LUNES_3_03))) + "\n")
    arch.write("LUNES_4_03;{}".format(int(value(LUNES_4_03))) + "\n")
    arch.write("LUNES_5_03;{}".format(int(value(LUNES_5_03))) + "\n")
    arch.write("LUNES_6_03;{}".format(int(value(LUNES_6_03))) + "\n")
    arch.write("LUNES_7_03;{}".format(int(value(LUNES_7_03))) + "\n")
    arch.write("LUNES_8_03;{}".format(int(value(LUNES_8_03))) + "\n")
    arch.write("LUNES_9_03;{}".format(int(value(LUNES_9_03))) + "\n")
    arch.write("LUNES_10_03;{}".format(int(value(LUNES_10_03))) + "\n")
    arch.write("R_A_Curso1A_LUNES_1_01;{}".format(int(value(R_A_Curso1A_LUNES_1_01))) + "\n")
    arch.write("R_A_Curso1A_LUNES_2_01;{}".format(int(value(R_A_Curso1A_LUNES_2_01))) + "\n")
    arch.write("R_C_Curso1C_LUNES_5_01;{}".format(int(value(R_C_Curso1C_LUNES_5_01))) + "\n")
    arch.write("R_C_Curso1C_LUNES_6_01;{}".format(int(value(R_C_Curso1C_LUNES_6_01))) + "\n")
    arch.write("R_B_Curso1B_LUNES_3_01;{}".format(int(value(R_B_Curso1B_LUNES_3_01))) + "\n")
    arch.write("R_B_Curso1B_LUNES_4_01;{}".format(int(value(R_B_Curso1B_LUNES_4_01))) + "\n")
    arch.write("R_A_Curso1A_LUNES_1_02;{}".format(int(value(R_A_Curso1A_LUNES_1_02))) + "\n")
    arch.write("R_A_Curso1A_LUNES_2_02;{}".format(int(value(R_A_Curso1A_LUNES_2_02))) + "\n")
    arch.write("R_C_Curso1C_LUNES_5_02;{}".format(int(value(R_C_Curso1C_LUNES_5_02))) + "\n")
    arch.write("R_C_Curso1C_LUNES_6_02;{}".format(int(value(R_C_Curso1C_LUNES_6_02))) + "\n")
    arch.write("R_B_Curso1B_LUNES_3_02;{}".format(int(value(R_B_Curso1B_LUNES_3_02))) + "\n")
    arch.write("R_B_Curso1B_LUNES_4_02;{}".format(int(value(R_B_Curso1B_LUNES_4_02))) + "\n")
    arch.write("R_A_Curso1A_LUNES_1_03;{}".format(int(value(R_A_Curso1A_LUNES_1_03))) + "\n")
    arch.write("R_A_Curso1A_LUNES_2_03;{}".format(int(value(R_A_Curso1A_LUNES_2_03))) + "\n")
    arch.write("R_C_Curso1C_LUNES_5_03;{}".format(int(value(R_C_Curso1C_LUNES_5_03))) + "\n")
    arch.write("R_C_Curso1C_LUNES_6_03;{}".format(int(value(R_C_Curso1C_LUNES_6_03))) + "\n")
    arch.write("R_B_Curso1B_LUNES_3_03;{}".format(int(value(R_B_Curso1B_LUNES_3_03))) + "\n")
    arch.write("R_B_Curso1B_LUNES_4_03;{}".format(int(value(R_B_Curso1B_LUNES_4_03))) + "\n")
