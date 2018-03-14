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

#Y_i_j: La materia con id i se realiza en el cuatrimestre j

Y_1_01 = LpVariable(name='Y_1_01', cat='Binary')
Y_1_02 = LpVariable(name='Y_1_02', cat='Binary')
Y_1_03 = LpVariable(name='Y_1_03', cat='Binary')
Y_1_04 = LpVariable(name='Y_1_04', cat='Binary')
Y_2_01 = LpVariable(name='Y_2_01', cat='Binary')
Y_2_02 = LpVariable(name='Y_2_02', cat='Binary')
Y_2_03 = LpVariable(name='Y_2_03', cat='Binary')
Y_2_04 = LpVariable(name='Y_2_04', cat='Binary')
Y_3_01 = LpVariable(name='Y_3_01', cat='Binary')
Y_3_02 = LpVariable(name='Y_3_02', cat='Binary')
Y_3_03 = LpVariable(name='Y_3_03', cat='Binary')
Y_3_04 = LpVariable(name='Y_3_04', cat='Binary')


#Ci: Numero de cuatrimestre en que se hace la materia con id i. Ejemplo, si Ci=3 es que la materia i se hace el cuatrimestre numero 3

C1 = LpVariable(name='C1', lowBound=0, upBound=4, cat='Integer')
C2 = LpVariable(name='C2', lowBound=0, upBound=4, cat='Integer')
C3 = LpVariable(name='C3', lowBound=0, upBound=4, cat='Integer')


#TOTAL_CUATRIMESTRES: Total de cuatrimestres a cursar. Utilizada para escribir el maximo entre Ci MAX(CA, CB..)

TOTAL_CUATRIMESTRES = LpVariable(name='TOTAL_CUATRIMESTRES', lowBound=0, upBound=4, cat='Integer')
#CREDi: Cantidad de creditos al final del cuatrimestre i

CRED01 = LpVariable(name='CRED01', lowBound=0, upBound=10000, cat='Integer')
CRED02 = LpVariable(name='CRED02', lowBound=0, upBound=10000, cat='Integer')
CRED03 = LpVariable(name='CRED03', lowBound=0, upBound=10000, cat='Integer')
CRED04 = LpVariable(name='CRED04', lowBound=0, upBound=10000, cat='Integer')


#H_{id_materia i}_{id curso j}_{cuatrimestre k}: La materia i se cursa en el curso j en el cuatrimestre k

H_1_1_01 = LpVariable(name='H_1_1_01', cat='Binary')
H_3_5_01 = LpVariable(name='H_3_5_01', cat='Binary')
H_2_4_01 = LpVariable(name='H_2_4_01', cat='Binary')
H_1_2_02 = LpVariable(name='H_1_2_02', cat='Binary')
H_3_5_02 = LpVariable(name='H_3_5_02', cat='Binary')
H_2_3_02 = LpVariable(name='H_2_3_02', cat='Binary')
H_1_1_03 = LpVariable(name='H_1_1_03', cat='Binary')
H_3_5_03 = LpVariable(name='H_3_5_03', cat='Binary')
H_2_4_03 = LpVariable(name='H_2_4_03', cat='Binary')
H_1_2_04 = LpVariable(name='H_1_2_04', cat='Binary')
H_3_5_04 = LpVariable(name='H_3_5_04', cat='Binary')
H_2_3_04 = LpVariable(name='H_2_3_04', cat='Binary')


#{Dia i}_{Franja j}_{cuatrimestre k}: El dia i (LUNES; MARTES, etc) en la franja horaria j en el cuatrimestre k se esta cursando

LUNES_1_01 = LpVariable(name='LUNES_1_01', cat='Binary')
LUNES_2_01 = LpVariable(name='LUNES_2_01', cat='Binary')
LUNES_5_01 = LpVariable(name='LUNES_5_01', cat='Binary')
LUNES_6_01 = LpVariable(name='LUNES_6_01', cat='Binary')
MARTES_3_01 = LpVariable(name='MARTES_3_01', cat='Binary')
MARTES_4_01 = LpVariable(name='MARTES_4_01', cat='Binary')
LUNES_3_02 = LpVariable(name='LUNES_3_02', cat='Binary')
LUNES_4_02 = LpVariable(name='LUNES_4_02', cat='Binary')
LUNES_5_02 = LpVariable(name='LUNES_5_02', cat='Binary')
LUNES_6_02 = LpVariable(name='LUNES_6_02', cat='Binary')
MARTES_1_02 = LpVariable(name='MARTES_1_02', cat='Binary')
MARTES_2_02 = LpVariable(name='MARTES_2_02', cat='Binary')
LUNES_1_03 = LpVariable(name='LUNES_1_03', cat='Binary')
LUNES_2_03 = LpVariable(name='LUNES_2_03', cat='Binary')
LUNES_5_03 = LpVariable(name='LUNES_5_03', cat='Binary')
LUNES_6_03 = LpVariable(name='LUNES_6_03', cat='Binary')
MARTES_3_03 = LpVariable(name='MARTES_3_03', cat='Binary')
MARTES_4_03 = LpVariable(name='MARTES_4_03', cat='Binary')
LUNES_3_04 = LpVariable(name='LUNES_3_04', cat='Binary')
LUNES_4_04 = LpVariable(name='LUNES_4_04', cat='Binary')
LUNES_5_04 = LpVariable(name='LUNES_5_04', cat='Binary')
LUNES_6_04 = LpVariable(name='LUNES_6_04', cat='Binary')
MARTES_1_04 = LpVariable(name='MARTES_1_04', cat='Binary')
MARTES_2_04 = LpVariable(name='MARTES_2_04', cat='Binary')


#R_{id_materia}_{id curso}_{dia}_{franja}_{cuatrimestre}: El horario para la materia y curso en ese cuatrimestre esta habilitado

R_1_1_LUNES_1_01 = LpVariable(name='R_1_1_LUNES_1_01', cat='Binary')
R_1_1_LUNES_2_01 = LpVariable(name='R_1_1_LUNES_2_01', cat='Binary')
R_3_5_LUNES_5_01 = LpVariable(name='R_3_5_LUNES_5_01', cat='Binary')
R_3_5_LUNES_6_01 = LpVariable(name='R_3_5_LUNES_6_01', cat='Binary')
R_2_4_MARTES_3_01 = LpVariable(name='R_2_4_MARTES_3_01', cat='Binary')
R_2_4_MARTES_4_01 = LpVariable(name='R_2_4_MARTES_4_01', cat='Binary')
R_1_2_MARTES_1_02 = LpVariable(name='R_1_2_MARTES_1_02', cat='Binary')
R_1_2_MARTES_2_02 = LpVariable(name='R_1_2_MARTES_2_02', cat='Binary')
R_3_5_LUNES_5_02 = LpVariable(name='R_3_5_LUNES_5_02', cat='Binary')
R_3_5_LUNES_6_02 = LpVariable(name='R_3_5_LUNES_6_02', cat='Binary')
R_2_3_LUNES_3_02 = LpVariable(name='R_2_3_LUNES_3_02', cat='Binary')
R_2_3_LUNES_4_02 = LpVariable(name='R_2_3_LUNES_4_02', cat='Binary')
R_1_1_LUNES_1_03 = LpVariable(name='R_1_1_LUNES_1_03', cat='Binary')
R_1_1_LUNES_2_03 = LpVariable(name='R_1_1_LUNES_2_03', cat='Binary')
R_3_5_LUNES_5_03 = LpVariable(name='R_3_5_LUNES_5_03', cat='Binary')
R_3_5_LUNES_6_03 = LpVariable(name='R_3_5_LUNES_6_03', cat='Binary')
R_2_4_MARTES_3_03 = LpVariable(name='R_2_4_MARTES_3_03', cat='Binary')
R_2_4_MARTES_4_03 = LpVariable(name='R_2_4_MARTES_4_03', cat='Binary')
R_1_2_MARTES_1_04 = LpVariable(name='R_1_2_MARTES_1_04', cat='Binary')
R_1_2_MARTES_2_04 = LpVariable(name='R_1_2_MARTES_2_04', cat='Binary')
R_3_5_LUNES_5_04 = LpVariable(name='R_3_5_LUNES_5_04', cat='Binary')
R_3_5_LUNES_6_04 = LpVariable(name='R_3_5_LUNES_6_04', cat='Binary')
R_2_3_LUNES_3_04 = LpVariable(name='R_2_3_LUNES_3_04', cat='Binary')
R_2_3_LUNES_4_04 = LpVariable(name='R_2_3_LUNES_4_04', cat='Binary')


# Definicion del problema

prob = LpProblem('Jenny_Calculo_plan_carrera', LpMinimize)


# La materia i se debe cursar en un unico cuatrimestre. Ademas, si es obligatoria, debe cursarse si o si.

prob += (Y_1_01 + Y_1_02 + Y_1_03 + Y_1_04 >= 1)
prob += (Y_1_01 + Y_1_02 + Y_1_03 + Y_1_04 <= 1)

prob += (Y_3_01 + Y_3_02 + Y_3_03 + Y_3_04 >= 1)
prob += (Y_3_01 + Y_3_02 + Y_3_03 + Y_3_04 <= 1)

prob += (Y_2_01 + Y_2_02 + Y_2_03 + Y_2_04 >= 1)
prob += (Y_2_01 + Y_2_02 + Y_2_03 + Y_2_04 <= 1)


# Numero de cuatrimestre en que es cursada la materia

prob += (1*Y_1_01 + 2*Y_1_02 + 3*Y_1_03 + 4*Y_1_04<= C1)
prob += (1*Y_1_01 + 2*Y_1_02 + 3*Y_1_03 + 4*Y_1_04>= C1)

prob += (1*Y_2_01 + 2*Y_2_02 + 3*Y_2_03 + 4*Y_2_04<= C2)
prob += (1*Y_2_01 + 2*Y_2_02 + 3*Y_2_03 + 4*Y_2_04>= C2)

prob += (1*Y_3_01 + 2*Y_3_02 + 3*Y_3_03 + 4*Y_3_04<= C3)
prob += (1*Y_3_01 + 2*Y_3_02 + 3*Y_3_03 + 4*Y_3_04>= C3)


# Los cuatrimestres de las correlativas deben ser menores (cuando la materia se cursa)

prob += (C3 >= C1 + 1)


# La cantidad de materias por cuatrimestre no puede superar un valor maximo

prob += (Y_1_01 + Y_2_01 + Y_3_01 <= 2)
prob += (Y_1_02 + Y_2_02 + Y_3_02 <= 2)
prob += (Y_1_03 + Y_2_03 + Y_3_03 <= 2)
prob += (Y_1_04 + Y_2_04 + Y_3_04 <= 2)


#TOTAL_CUATRIMESTRES es el maximo de los Ci


prob += (C1 <= TOTAL_CUATRIMESTRES)
prob += (-C1 <= TOTAL_CUATRIMESTRES)

prob += (C2 <= TOTAL_CUATRIMESTRES)
prob += (-C2 <= TOTAL_CUATRIMESTRES)

prob += (C3 <= TOTAL_CUATRIMESTRES)
prob += (-C3 <= TOTAL_CUATRIMESTRES)


# Calculo de creditos al terminar cada cuatrimestre

prob += (6*Y_1_01 + 6*Y_2_01 + 6*Y_3_01  <= CRED01)
prob += (6*Y_1_01 + 6*Y_2_01 + 6*Y_3_01  >= CRED01)
prob += (6*Y_1_02 + 6*Y_2_02 + 6*Y_3_02 + CRED01 <= CRED02)
prob += (6*Y_1_02 + 6*Y_2_02 + 6*Y_3_02 + CRED01 >= CRED02)
prob += (6*Y_1_03 + 6*Y_2_03 + 6*Y_3_03 + CRED02 <= CRED03)
prob += (6*Y_1_03 + 6*Y_2_03 + 6*Y_3_03 + CRED02 >= CRED03)
prob += (6*Y_1_04 + 6*Y_2_04 + 6*Y_3_04 + CRED03 <= CRED04)
prob += (6*Y_1_04 + 6*Y_2_04 + 6*Y_3_04 + CRED03 >= CRED04)

# Restricciones sobre aquellas materias que requieren creditos minimos para poder cursar


#Si la materia se cursa en ese cuatrimestre en ese curso en particular, entonces se deben cursar todos los horarios del mismo

prob += (H_1_1_01 <= R_1_1_LUNES_1_01)
prob += (H_1_1_01 >= R_1_1_LUNES_1_01)
prob += (H_1_1_01 <= R_1_1_LUNES_2_01)
prob += (H_1_1_01 >= R_1_1_LUNES_2_01)
prob += (H_3_5_01 <= R_3_5_LUNES_5_01)
prob += (H_3_5_01 >= R_3_5_LUNES_5_01)
prob += (H_3_5_01 <= R_3_5_LUNES_6_01)
prob += (H_3_5_01 >= R_3_5_LUNES_6_01)
prob += (H_2_4_01 <= R_2_4_MARTES_3_01)
prob += (H_2_4_01 >= R_2_4_MARTES_3_01)
prob += (H_2_4_01 <= R_2_4_MARTES_4_01)
prob += (H_2_4_01 >= R_2_4_MARTES_4_01)
prob += (H_1_2_02 <= R_1_2_MARTES_1_02)
prob += (H_1_2_02 >= R_1_2_MARTES_1_02)
prob += (H_1_2_02 <= R_1_2_MARTES_2_02)
prob += (H_1_2_02 >= R_1_2_MARTES_2_02)
prob += (H_3_5_02 <= R_3_5_LUNES_5_02)
prob += (H_3_5_02 >= R_3_5_LUNES_5_02)
prob += (H_3_5_02 <= R_3_5_LUNES_6_02)
prob += (H_3_5_02 >= R_3_5_LUNES_6_02)
prob += (H_2_3_02 <= R_2_3_LUNES_3_02)
prob += (H_2_3_02 >= R_2_3_LUNES_3_02)
prob += (H_2_3_02 <= R_2_3_LUNES_4_02)
prob += (H_2_3_02 >= R_2_3_LUNES_4_02)
prob += (H_1_1_03 <= R_1_1_LUNES_1_03)
prob += (H_1_1_03 >= R_1_1_LUNES_1_03)
prob += (H_1_1_03 <= R_1_1_LUNES_2_03)
prob += (H_1_1_03 >= R_1_1_LUNES_2_03)
prob += (H_3_5_03 <= R_3_5_LUNES_5_03)
prob += (H_3_5_03 >= R_3_5_LUNES_5_03)
prob += (H_3_5_03 <= R_3_5_LUNES_6_03)
prob += (H_3_5_03 >= R_3_5_LUNES_6_03)
prob += (H_2_4_03 <= R_2_4_MARTES_3_03)
prob += (H_2_4_03 >= R_2_4_MARTES_3_03)
prob += (H_2_4_03 <= R_2_4_MARTES_4_03)
prob += (H_2_4_03 >= R_2_4_MARTES_4_03)
prob += (H_1_2_04 <= R_1_2_MARTES_1_04)
prob += (H_1_2_04 >= R_1_2_MARTES_1_04)
prob += (H_1_2_04 <= R_1_2_MARTES_2_04)
prob += (H_1_2_04 >= R_1_2_MARTES_2_04)
prob += (H_3_5_04 <= R_3_5_LUNES_5_04)
prob += (H_3_5_04 >= R_3_5_LUNES_5_04)
prob += (H_3_5_04 <= R_3_5_LUNES_6_04)
prob += (H_3_5_04 >= R_3_5_LUNES_6_04)
prob += (H_2_3_04 <= R_2_3_LUNES_3_04)
prob += (H_2_3_04 >= R_2_3_LUNES_3_04)
prob += (H_2_3_04 <= R_2_3_LUNES_4_04)
prob += (H_2_3_04 >= R_2_3_LUNES_4_04)

#No hay giratiempos: Solo puede cursarse una materia en un unico curso en el mismo horario

prob += (LUNES_1_01 <= R_1_1_LUNES_1_01)
prob += (LUNES_1_01 >= R_1_1_LUNES_1_01)
prob += (LUNES_2_01 <= R_1_1_LUNES_2_01)
prob += (LUNES_2_01 >= R_1_1_LUNES_2_01)
prob += (LUNES_5_01 <= R_3_5_LUNES_5_01)
prob += (LUNES_5_01 >= R_3_5_LUNES_5_01)
prob += (LUNES_6_01 <= R_3_5_LUNES_6_01)
prob += (LUNES_6_01 >= R_3_5_LUNES_6_01)
prob += (MARTES_3_01 <= R_2_4_MARTES_3_01)
prob += (MARTES_3_01 >= R_2_4_MARTES_3_01)
prob += (MARTES_4_01 <= R_2_4_MARTES_4_01)
prob += (MARTES_4_01 >= R_2_4_MARTES_4_01)
prob += (LUNES_3_02 <= R_2_3_LUNES_3_02)
prob += (LUNES_3_02 >= R_2_3_LUNES_3_02)
prob += (LUNES_4_02 <= R_2_3_LUNES_4_02)
prob += (LUNES_4_02 >= R_2_3_LUNES_4_02)
prob += (LUNES_5_02 <= R_3_5_LUNES_5_02)
prob += (LUNES_5_02 >= R_3_5_LUNES_5_02)
prob += (LUNES_6_02 <= R_3_5_LUNES_6_02)
prob += (LUNES_6_02 >= R_3_5_LUNES_6_02)
prob += (MARTES_1_02 <= R_1_2_MARTES_1_02)
prob += (MARTES_1_02 >= R_1_2_MARTES_1_02)
prob += (MARTES_2_02 <= R_1_2_MARTES_2_02)
prob += (MARTES_2_02 >= R_1_2_MARTES_2_02)
prob += (LUNES_1_03 <= R_1_1_LUNES_1_03)
prob += (LUNES_1_03 >= R_1_1_LUNES_1_03)
prob += (LUNES_2_03 <= R_1_1_LUNES_2_03)
prob += (LUNES_2_03 >= R_1_1_LUNES_2_03)
prob += (LUNES_5_03 <= R_3_5_LUNES_5_03)
prob += (LUNES_5_03 >= R_3_5_LUNES_5_03)
prob += (LUNES_6_03 <= R_3_5_LUNES_6_03)
prob += (LUNES_6_03 >= R_3_5_LUNES_6_03)
prob += (MARTES_3_03 <= R_2_4_MARTES_3_03)
prob += (MARTES_3_03 >= R_2_4_MARTES_3_03)
prob += (MARTES_4_03 <= R_2_4_MARTES_4_03)
prob += (MARTES_4_03 >= R_2_4_MARTES_4_03)
prob += (LUNES_3_04 <= R_2_3_LUNES_3_04)
prob += (LUNES_3_04 >= R_2_3_LUNES_3_04)
prob += (LUNES_4_04 <= R_2_3_LUNES_4_04)
prob += (LUNES_4_04 >= R_2_3_LUNES_4_04)
prob += (LUNES_5_04 <= R_3_5_LUNES_5_04)
prob += (LUNES_5_04 >= R_3_5_LUNES_5_04)
prob += (LUNES_6_04 <= R_3_5_LUNES_6_04)
prob += (LUNES_6_04 >= R_3_5_LUNES_6_04)
prob += (MARTES_1_04 <= R_1_2_MARTES_1_04)
prob += (MARTES_1_04 >= R_1_2_MARTES_1_04)
prob += (MARTES_2_04 <= R_1_2_MARTES_2_04)
prob += (MARTES_2_04 >= R_1_2_MARTES_2_04)

# Si la materia no se cursa ese cuatrimestre, entonces no puede cursarse en ninguno de los cursos de ese cuatrimestre

prob += (Y_1_01 >= H_1_1_01)
prob += (Y_3_01 >= H_3_5_01)
prob += (Y_2_01 >= H_2_4_01)
prob += (Y_1_02 >= H_1_2_02)
prob += (Y_3_02 >= H_3_5_02)
prob += (Y_2_02 >= H_2_3_02)
prob += (Y_1_03 >= H_1_1_03)
prob += (Y_3_03 >= H_3_5_03)
prob += (Y_2_03 >= H_2_4_03)
prob += (Y_1_04 >= H_1_2_04)
prob += (Y_3_04 >= H_3_5_04)
prob += (Y_2_04 >= H_2_3_04)

# La materia no puede cursarse en mas de un curso en el cuatrimestre

prob += (Y_1_01 <= H_1_1_01 + 0)
prob += (Y_1_01 >= H_1_1_01 + 0)
prob += (Y_3_01 <= H_3_5_01)
prob += (Y_3_01 >= H_3_5_01)
prob += (Y_2_01 <= 0 + H_2_4_01)
prob += (Y_2_01 >= 0 + H_2_4_01)
prob += (Y_1_02 <= 0 + H_1_2_02)
prob += (Y_1_02 >= 0 + H_1_2_02)
prob += (Y_3_02 <= H_3_5_02)
prob += (Y_3_02 >= H_3_5_02)
prob += (Y_2_02 <= H_2_3_02 + 0)
prob += (Y_2_02 >= H_2_3_02 + 0)
prob += (Y_1_03 <= H_1_1_03 + 0)
prob += (Y_1_03 >= H_1_1_03 + 0)
prob += (Y_3_03 <= H_3_5_03)
prob += (Y_3_03 >= H_3_5_03)
prob += (Y_2_03 <= 0 + H_2_4_03)
prob += (Y_2_03 >= 0 + H_2_4_03)
prob += (Y_1_04 <= 0 + H_1_2_04)
prob += (Y_1_04 >= 0 + H_1_2_04)
prob += (Y_3_04 <= H_3_5_04)
prob += (Y_3_04 >= H_3_5_04)
prob += (Y_2_04 <= H_2_3_04 + 0)
prob += (Y_2_04 >= H_2_3_04 + 0)

# No todos los cursos se dictan ambos cuatrimestres


# Definicion de la funcion objetivo a minimizar.

prob += 10*TOTAL_CUATRIMESTRES

# Resolucion del problema

tiempo_inicial = time()
status = prob.solve(COIN(threads=2, msg=True))
tiempo_final = time()
DURACION_EJECUCION_PULP = tiempo_final - tiempo_inicial
print('Duracion: {}'.format(convertir_tiempo(DURACION_EJECUCION_PULP)))

with open('resultados_tests/test_con_cursos_dictados_en_un_unico_cuatrimestre_resultados_pulp.py', 'w') as arch:
    arch.write("tiempo;{}".format(DURACION_EJECUCION_PULP) + "\n")
    arch.write("Y_1_01;{}".format(int(value(Y_1_01))) + "\n")
    arch.write("Y_1_02;{}".format(int(value(Y_1_02))) + "\n")
    arch.write("Y_1_03;{}".format(int(value(Y_1_03))) + "\n")
    arch.write("Y_1_04;{}".format(int(value(Y_1_04))) + "\n")
    arch.write("Y_2_01;{}".format(int(value(Y_2_01))) + "\n")
    arch.write("Y_2_02;{}".format(int(value(Y_2_02))) + "\n")
    arch.write("Y_2_03;{}".format(int(value(Y_2_03))) + "\n")
    arch.write("Y_2_04;{}".format(int(value(Y_2_04))) + "\n")
    arch.write("Y_3_01;{}".format(int(value(Y_3_01))) + "\n")
    arch.write("Y_3_02;{}".format(int(value(Y_3_02))) + "\n")
    arch.write("Y_3_03;{}".format(int(value(Y_3_03))) + "\n")
    arch.write("Y_3_04;{}".format(int(value(Y_3_04))) + "\n")
    arch.write("C1;{}".format(int(value(C1))) + "\n")
    arch.write("C2;{}".format(int(value(C2))) + "\n")
    arch.write("C3;{}".format(int(value(C3))) + "\n")
    arch.write("TOTAL_CUATRIMESTRES;{}".format(int(value(TOTAL_CUATRIMESTRES))) + "\n")
    arch.write("CRED01;{}".format(int(value(CRED01))) + "\n")
    arch.write("CRED02;{}".format(int(value(CRED02))) + "\n")
    arch.write("CRED03;{}".format(int(value(CRED03))) + "\n")
    arch.write("CRED04;{}".format(int(value(CRED04))) + "\n")
    arch.write("H_1_1_01;{}".format(int(value(H_1_1_01))) + "\n")
    arch.write("H_1_2_01;0" + '\n')
    arch.write("H_3_5_01;{}".format(int(value(H_3_5_01))) + "\n")
    arch.write("H_2_3_01;0" + '\n')
    arch.write("H_2_4_01;{}".format(int(value(H_2_4_01))) + "\n")
    arch.write("H_1_1_02;0" + '\n')
    arch.write("H_1_2_02;{}".format(int(value(H_1_2_02))) + "\n")
    arch.write("H_3_5_02;{}".format(int(value(H_3_5_02))) + "\n")
    arch.write("H_2_3_02;{}".format(int(value(H_2_3_02))) + "\n")
    arch.write("H_2_4_02;0" + '\n')
    arch.write("H_1_1_03;{}".format(int(value(H_1_1_03))) + "\n")
    arch.write("H_1_2_03;0" + '\n')
    arch.write("H_3_5_03;{}".format(int(value(H_3_5_03))) + "\n")
    arch.write("H_2_3_03;0" + '\n')
    arch.write("H_2_4_03;{}".format(int(value(H_2_4_03))) + "\n")
    arch.write("H_1_1_04;0" + '\n')
    arch.write("H_1_2_04;{}".format(int(value(H_1_2_04))) + "\n")
    arch.write("H_3_5_04;{}".format(int(value(H_3_5_04))) + "\n")
    arch.write("H_2_3_04;{}".format(int(value(H_2_3_04))) + "\n")
    arch.write("H_2_4_04;0" + '\n')
    arch.write("LUNES_1_01;{}".format(int(value(LUNES_1_01))) + "\n")
    arch.write("LUNES_2_01;{}".format(int(value(LUNES_2_01))) + "\n")
    arch.write("LUNES_3_01;0" + '\n')
    arch.write("LUNES_4_01;0" + '\n')
    arch.write("LUNES_5_01;{}".format(int(value(LUNES_5_01))) + "\n")
    arch.write("LUNES_6_01;{}".format(int(value(LUNES_6_01))) + "\n")
    arch.write("LUNES_7_01;0" + '\n')
    arch.write("LUNES_8_01;0" + '\n')
    arch.write("LUNES_9_01;0" + '\n')
    arch.write("LUNES_10_01;0" + '\n')
    arch.write("MARTES_1_01;0" + '\n')
    arch.write("MARTES_2_01;0" + '\n')
    arch.write("MARTES_3_01;{}".format(int(value(MARTES_3_01))) + "\n")
    arch.write("MARTES_4_01;{}".format(int(value(MARTES_4_01))) + "\n")
    arch.write("MARTES_5_01;0" + '\n')
    arch.write("MARTES_6_01;0" + '\n')
    arch.write("MARTES_7_01;0" + '\n')
    arch.write("MARTES_8_01;0" + '\n')
    arch.write("MARTES_9_01;0" + '\n')
    arch.write("MARTES_10_01;0" + '\n')
    arch.write("LUNES_1_02;0" + '\n')
    arch.write("LUNES_2_02;0" + '\n')
    arch.write("LUNES_3_02;{}".format(int(value(LUNES_3_02))) + "\n")
    arch.write("LUNES_4_02;{}".format(int(value(LUNES_4_02))) + "\n")
    arch.write("LUNES_5_02;{}".format(int(value(LUNES_5_02))) + "\n")
    arch.write("LUNES_6_02;{}".format(int(value(LUNES_6_02))) + "\n")
    arch.write("LUNES_7_02;0" + '\n')
    arch.write("LUNES_8_02;0" + '\n')
    arch.write("LUNES_9_02;0" + '\n')
    arch.write("LUNES_10_02;0" + '\n')
    arch.write("MARTES_1_02;{}".format(int(value(MARTES_1_02))) + "\n")
    arch.write("MARTES_2_02;{}".format(int(value(MARTES_2_02))) + "\n")
    arch.write("MARTES_3_02;0" + '\n')
    arch.write("MARTES_4_02;0" + '\n')
    arch.write("MARTES_5_02;0" + '\n')
    arch.write("MARTES_6_02;0" + '\n')
    arch.write("MARTES_7_02;0" + '\n')
    arch.write("MARTES_8_02;0" + '\n')
    arch.write("MARTES_9_02;0" + '\n')
    arch.write("MARTES_10_02;0" + '\n')
    arch.write("LUNES_1_03;{}".format(int(value(LUNES_1_03))) + "\n")
    arch.write("LUNES_2_03;{}".format(int(value(LUNES_2_03))) + "\n")
    arch.write("LUNES_3_03;0" + '\n')
    arch.write("LUNES_4_03;0" + '\n')
    arch.write("LUNES_5_03;{}".format(int(value(LUNES_5_03))) + "\n")
    arch.write("LUNES_6_03;{}".format(int(value(LUNES_6_03))) + "\n")
    arch.write("LUNES_7_03;0" + '\n')
    arch.write("LUNES_8_03;0" + '\n')
    arch.write("LUNES_9_03;0" + '\n')
    arch.write("LUNES_10_03;0" + '\n')
    arch.write("MARTES_1_03;0" + '\n')
    arch.write("MARTES_2_03;0" + '\n')
    arch.write("MARTES_3_03;{}".format(int(value(MARTES_3_03))) + "\n")
    arch.write("MARTES_4_03;{}".format(int(value(MARTES_4_03))) + "\n")
    arch.write("MARTES_5_03;0" + '\n')
    arch.write("MARTES_6_03;0" + '\n')
    arch.write("MARTES_7_03;0" + '\n')
    arch.write("MARTES_8_03;0" + '\n')
    arch.write("MARTES_9_03;0" + '\n')
    arch.write("MARTES_10_03;0" + '\n')
    arch.write("LUNES_1_04;0" + '\n')
    arch.write("LUNES_2_04;0" + '\n')
    arch.write("LUNES_3_04;{}".format(int(value(LUNES_3_04))) + "\n")
    arch.write("LUNES_4_04;{}".format(int(value(LUNES_4_04))) + "\n")
    arch.write("LUNES_5_04;{}".format(int(value(LUNES_5_04))) + "\n")
    arch.write("LUNES_6_04;{}".format(int(value(LUNES_6_04))) + "\n")
    arch.write("LUNES_7_04;0" + '\n')
    arch.write("LUNES_8_04;0" + '\n')
    arch.write("LUNES_9_04;0" + '\n')
    arch.write("LUNES_10_04;0" + '\n')
    arch.write("MARTES_1_04;{}".format(int(value(MARTES_1_04))) + "\n")
    arch.write("MARTES_2_04;{}".format(int(value(MARTES_2_04))) + "\n")
    arch.write("MARTES_3_04;0" + '\n')
    arch.write("MARTES_4_04;0" + '\n')
    arch.write("MARTES_5_04;0" + '\n')
    arch.write("MARTES_6_04;0" + '\n')
    arch.write("MARTES_7_04;0" + '\n')
    arch.write("MARTES_8_04;0" + '\n')
    arch.write("MARTES_9_04;0" + '\n')
    arch.write("MARTES_10_04;0" + '\n')
    arch.write("R_1_1_LUNES_1_01;{}".format(int(value(R_1_1_LUNES_1_01))) + "\n")
    arch.write("R_1_1_LUNES_2_01;{}".format(int(value(R_1_1_LUNES_2_01))) + "\n")
    arch.write("R_3_5_LUNES_5_01;{}".format(int(value(R_3_5_LUNES_5_01))) + "\n")
    arch.write("R_3_5_LUNES_6_01;{}".format(int(value(R_3_5_LUNES_6_01))) + "\n")
    arch.write("R_2_4_MARTES_3_01;{}".format(int(value(R_2_4_MARTES_3_01))) + "\n")
    arch.write("R_2_4_MARTES_4_01;{}".format(int(value(R_2_4_MARTES_4_01))) + "\n")
    arch.write("R_1_2_MARTES_1_02;{}".format(int(value(R_1_2_MARTES_1_02))) + "\n")
    arch.write("R_1_2_MARTES_2_02;{}".format(int(value(R_1_2_MARTES_2_02))) + "\n")
    arch.write("R_3_5_LUNES_5_02;{}".format(int(value(R_3_5_LUNES_5_02))) + "\n")
    arch.write("R_3_5_LUNES_6_02;{}".format(int(value(R_3_5_LUNES_6_02))) + "\n")
    arch.write("R_2_3_LUNES_3_02;{}".format(int(value(R_2_3_LUNES_3_02))) + "\n")
    arch.write("R_2_3_LUNES_4_02;{}".format(int(value(R_2_3_LUNES_4_02))) + "\n")
    arch.write("R_1_1_LUNES_1_03;{}".format(int(value(R_1_1_LUNES_1_03))) + "\n")
    arch.write("R_1_1_LUNES_2_03;{}".format(int(value(R_1_1_LUNES_2_03))) + "\n")
    arch.write("R_3_5_LUNES_5_03;{}".format(int(value(R_3_5_LUNES_5_03))) + "\n")
    arch.write("R_3_5_LUNES_6_03;{}".format(int(value(R_3_5_LUNES_6_03))) + "\n")
    arch.write("R_2_4_MARTES_3_03;{}".format(int(value(R_2_4_MARTES_3_03))) + "\n")
    arch.write("R_2_4_MARTES_4_03;{}".format(int(value(R_2_4_MARTES_4_03))) + "\n")
    arch.write("R_1_2_MARTES_1_04;{}".format(int(value(R_1_2_MARTES_1_04))) + "\n")
    arch.write("R_1_2_MARTES_2_04;{}".format(int(value(R_1_2_MARTES_2_04))) + "\n")
    arch.write("R_3_5_LUNES_5_04;{}".format(int(value(R_3_5_LUNES_5_04))) + "\n")
    arch.write("R_3_5_LUNES_6_04;{}".format(int(value(R_3_5_LUNES_6_04))) + "\n")
    arch.write("R_2_3_LUNES_3_04;{}".format(int(value(R_2_3_LUNES_3_04))) + "\n")
    arch.write("R_2_3_LUNES_4_04;{}".format(int(value(R_2_3_LUNES_4_04))) + "\n")
