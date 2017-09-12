from pulp import *


from time import time


#Yij: La materia i se realiza en el cuatrimestre j

Y_A_1 = LpVariable(name='Y_A_1', cat='Binary')
Y_A_2 = LpVariable(name='Y_A_2', cat='Binary')
Y_B_1 = LpVariable(name='Y_B_1', cat='Binary')
Y_B_2 = LpVariable(name='Y_B_2', cat='Binary')


#Ci: Numero de cuatrimestre en que se hace la materia i. Ejemplo, si Ci=3 es que la materia i se hace el cuatrimestre numero 3

CA = LpVariable(name='CA', cat='Integer')
CB = LpVariable(name='CB', cat='Integer')


#TOTAL_CUATRIMESTRES: Total de cuatrimestres a cursar. Utilizada para escribir el maximo entre Ci MAX(CA, CB..)

TOTAL_CUATRIMESTRES = LpVariable(name='TOTAL_CUATRIMESTRES', cat='Integer')

#CREDi: Cantidad de creditos al final del cuatrimestre i

CRED0 = LpVariable(name='CRED0', cat='Integer')
CRED1 = LpVariable(name='CRED1', cat='Integer')


#H_{materia i}_{nombre del curso j}_{cuatrimestre k}: La materia i se cursa en el curso j en el cuatrimestre k

H_A_Curso1A_1 = LpVariable(name='H_A_Curso1A_1', cat='Binary')
H_A_Curso2A_1 = LpVariable(name='H_A_Curso2A_1', cat='Binary')
H_A_Curso3A_1 = LpVariable(name='H_A_Curso3A_1', cat='Binary')
H_B_Curso1B_1 = LpVariable(name='H_B_Curso1B_1', cat='Binary')
H_B_Curso2B_1 = LpVariable(name='H_B_Curso2B_1', cat='Binary')
H_B_Curso3B_1 = LpVariable(name='H_B_Curso3B_1', cat='Binary')
H_B_Curso4B_1 = LpVariable(name='H_B_Curso4B_1', cat='Binary')
H_A_Curso1A_2 = LpVariable(name='H_A_Curso1A_2', cat='Binary')
H_A_Curso2A_2 = LpVariable(name='H_A_Curso2A_2', cat='Binary')
H_A_Curso3A_2 = LpVariable(name='H_A_Curso3A_2', cat='Binary')
H_B_Curso1B_2 = LpVariable(name='H_B_Curso1B_2', cat='Binary')
H_B_Curso2B_2 = LpVariable(name='H_B_Curso2B_2', cat='Binary')
H_B_Curso3B_2 = LpVariable(name='H_B_Curso3B_2', cat='Binary')
H_B_Curso4B_2 = LpVariable(name='H_B_Curso4B_2', cat='Binary')


#{Dia i}_{Franja j}_{cuatrimestre k}: El dia i (LUNES; MARTES, etc) en la franja horaria j en el cuatrimestre k se esta cursando

LUNES_1_1 = LpVariable(name='LUNES_1_1', cat='Binary')
LUNES_2_1 = LpVariable(name='LUNES_2_1', cat='Binary')
LUNES_3_1 = LpVariable(name='LUNES_3_1', cat='Binary')
LUNES_4_1 = LpVariable(name='LUNES_4_1', cat='Binary')
LUNES_5_1 = LpVariable(name='LUNES_5_1', cat='Binary')
LUNES_6_1 = LpVariable(name='LUNES_6_1', cat='Binary')
LUNES_7_1 = LpVariable(name='LUNES_7_1', cat='Binary')
LUNES_8_1 = LpVariable(name='LUNES_8_1', cat='Binary')
LUNES_9_1 = LpVariable(name='LUNES_9_1', cat='Binary')
LUNES_10_1 = LpVariable(name='LUNES_10_1', cat='Binary')
LUNES_11_1 = LpVariable(name='LUNES_11_1', cat='Binary')
LUNES_12_1 = LpVariable(name='LUNES_12_1', cat='Binary')
LUNES_1_2 = LpVariable(name='LUNES_1_2', cat='Binary')
LUNES_2_2 = LpVariable(name='LUNES_2_2', cat='Binary')
LUNES_3_2 = LpVariable(name='LUNES_3_2', cat='Binary')
LUNES_4_2 = LpVariable(name='LUNES_4_2', cat='Binary')
LUNES_5_2 = LpVariable(name='LUNES_5_2', cat='Binary')
LUNES_6_2 = LpVariable(name='LUNES_6_2', cat='Binary')
LUNES_7_2 = LpVariable(name='LUNES_7_2', cat='Binary')
LUNES_8_2 = LpVariable(name='LUNES_8_2', cat='Binary')
LUNES_9_2 = LpVariable(name='LUNES_9_2', cat='Binary')
LUNES_10_2 = LpVariable(name='LUNES_10_2', cat='Binary')
LUNES_11_2 = LpVariable(name='LUNES_11_2', cat='Binary')
LUNES_12_2 = LpVariable(name='LUNES_12_2', cat='Binary')


#R_{materia}_{nombre curso}_{dia}_{franja}_{cuatrimestre}: El horario para la materia y curso en ese cuatrimestre esta habilitado

R_A_Curso1A_LUNES_1_1 = LpVariable(name='R_A_Curso1A_LUNES_1_1', cat='Binary')
R_A_Curso1A_LUNES_2_1 = LpVariable(name='R_A_Curso1A_LUNES_2_1', cat='Binary')
R_A_Curso1A_LUNES_3_1 = LpVariable(name='R_A_Curso1A_LUNES_3_1', cat='Binary')
R_A_Curso2A_LUNES_2_1 = LpVariable(name='R_A_Curso2A_LUNES_2_1', cat='Binary')
R_A_Curso2A_LUNES_3_1 = LpVariable(name='R_A_Curso2A_LUNES_3_1', cat='Binary')
R_A_Curso2A_LUNES_5_1 = LpVariable(name='R_A_Curso2A_LUNES_5_1', cat='Binary')
R_A_Curso2A_LUNES_6_1 = LpVariable(name='R_A_Curso2A_LUNES_6_1', cat='Binary')
R_A_Curso2A_LUNES_7_1 = LpVariable(name='R_A_Curso2A_LUNES_7_1', cat='Binary')
R_A_Curso3A_LUNES_4_1 = LpVariable(name='R_A_Curso3A_LUNES_4_1', cat='Binary')
R_A_Curso3A_LUNES_5_1 = LpVariable(name='R_A_Curso3A_LUNES_5_1', cat='Binary')
R_A_Curso3A_LUNES_6_1 = LpVariable(name='R_A_Curso3A_LUNES_6_1', cat='Binary')
R_B_Curso1B_LUNES_1_1 = LpVariable(name='R_B_Curso1B_LUNES_1_1', cat='Binary')
R_B_Curso1B_LUNES_2_1 = LpVariable(name='R_B_Curso1B_LUNES_2_1', cat='Binary')
R_B_Curso1B_LUNES_3_1 = LpVariable(name='R_B_Curso1B_LUNES_3_1', cat='Binary')
R_B_Curso2B_LUNES_4_1 = LpVariable(name='R_B_Curso2B_LUNES_4_1', cat='Binary')
R_B_Curso2B_LUNES_9_1 = LpVariable(name='R_B_Curso2B_LUNES_9_1', cat='Binary')
R_B_Curso3B_LUNES_7_1 = LpVariable(name='R_B_Curso3B_LUNES_7_1', cat='Binary')
R_B_Curso3B_LUNES_8_1 = LpVariable(name='R_B_Curso3B_LUNES_8_1', cat='Binary')
R_B_Curso3B_LUNES_9_1 = LpVariable(name='R_B_Curso3B_LUNES_9_1', cat='Binary')
R_B_Curso3B_LUNES_10_1 = LpVariable(name='R_B_Curso3B_LUNES_10_1', cat='Binary')
R_B_Curso4B_LUNES_9_1 = LpVariable(name='R_B_Curso4B_LUNES_9_1', cat='Binary')
R_B_Curso4B_LUNES_10_1 = LpVariable(name='R_B_Curso4B_LUNES_10_1', cat='Binary')
R_A_Curso1A_LUNES_1_2 = LpVariable(name='R_A_Curso1A_LUNES_1_2', cat='Binary')
R_A_Curso1A_LUNES_2_2 = LpVariable(name='R_A_Curso1A_LUNES_2_2', cat='Binary')
R_A_Curso1A_LUNES_3_2 = LpVariable(name='R_A_Curso1A_LUNES_3_2', cat='Binary')
R_A_Curso2A_LUNES_2_2 = LpVariable(name='R_A_Curso2A_LUNES_2_2', cat='Binary')
R_A_Curso2A_LUNES_3_2 = LpVariable(name='R_A_Curso2A_LUNES_3_2', cat='Binary')
R_A_Curso2A_LUNES_5_2 = LpVariable(name='R_A_Curso2A_LUNES_5_2', cat='Binary')
R_A_Curso2A_LUNES_6_2 = LpVariable(name='R_A_Curso2A_LUNES_6_2', cat='Binary')
R_A_Curso2A_LUNES_7_2 = LpVariable(name='R_A_Curso2A_LUNES_7_2', cat='Binary')
R_A_Curso3A_LUNES_4_2 = LpVariable(name='R_A_Curso3A_LUNES_4_2', cat='Binary')
R_A_Curso3A_LUNES_5_2 = LpVariable(name='R_A_Curso3A_LUNES_5_2', cat='Binary')
R_A_Curso3A_LUNES_6_2 = LpVariable(name='R_A_Curso3A_LUNES_6_2', cat='Binary')
R_B_Curso1B_LUNES_1_2 = LpVariable(name='R_B_Curso1B_LUNES_1_2', cat='Binary')
R_B_Curso1B_LUNES_2_2 = LpVariable(name='R_B_Curso1B_LUNES_2_2', cat='Binary')
R_B_Curso1B_LUNES_3_2 = LpVariable(name='R_B_Curso1B_LUNES_3_2', cat='Binary')
R_B_Curso2B_LUNES_4_2 = LpVariable(name='R_B_Curso2B_LUNES_4_2', cat='Binary')
R_B_Curso2B_LUNES_9_2 = LpVariable(name='R_B_Curso2B_LUNES_9_2', cat='Binary')
R_B_Curso3B_LUNES_7_2 = LpVariable(name='R_B_Curso3B_LUNES_7_2', cat='Binary')
R_B_Curso3B_LUNES_8_2 = LpVariable(name='R_B_Curso3B_LUNES_8_2', cat='Binary')
R_B_Curso3B_LUNES_9_2 = LpVariable(name='R_B_Curso3B_LUNES_9_2', cat='Binary')
R_B_Curso3B_LUNES_10_2 = LpVariable(name='R_B_Curso3B_LUNES_10_2', cat='Binary')
R_B_Curso4B_LUNES_9_2 = LpVariable(name='R_B_Curso4B_LUNES_9_2', cat='Binary')
R_B_Curso4B_LUNES_10_2 = LpVariable(name='R_B_Curso4B_LUNES_10_2', cat='Binary')


#OCUPADO_{dia}_{cuatrimestre}: Vale 1 si el {dia} en el {cuatrimestre} tiene al menos un horario ocupado

OCUPADO_LUNES_1 = LpVariable(name='OCUPADO_LUNES_1', cat='Binary')
OCUPADO_LUNES_2 = LpVariable(name='OCUPADO_LUNES_2', cat='Binary')


#MAXIMA_FRANJA_{dia}_{cuatrimestre}: Numero de la maxima franja ocupada en el {dia} en el {cuatrimestre}.
#MINIMA_FRANJA_{dia}_{cuatrimestre}: Numero de la minima franja ocupada en el {dia} en el {cuatrimestre}.

MAXIMA_FRANJA_LUNES_1 = LpVariable(name='MAXIMA_FRANJA_LUNES_1', cat='Integer')
MINIMA_FRANJA_LUNES_1 = LpVariable(name='MINIMA_FRANJA_LUNES_1', cat='Integer')
MAXIMA_FRANJA_LUNES_2 = LpVariable(name='MAXIMA_FRANJA_LUNES_2', cat='Integer')
MINIMA_FRANJA_LUNES_2 = LpVariable(name='MINIMA_FRANJA_LUNES_2', cat='Integer')


#HORAS_LIBRES_{dia}_{cuatrimestre}: Cantidad de horas libres entre materias el {dia} en el {cuatrimestre}.

HORAS_LIBRES_LUNES_1 = LpVariable(name='HORAS_LIBRES_LUNES_1', cat='Integer')
HORAS_LIBRES_LUNES_2 = LpVariable(name='HORAS_LIBRES_LUNES_2', cat='Integer')


#HORAS_LIBRES_TOTALES: Cantidad de horas libres en todo el plan

HORAS_LIBRES_TOTALES = LpVariable(name='HORAS_LIBRES_TOTALES', cat='Integer')


# Definicion del problema

prob = LpProblem('Jenny_Calculo_plan_carrera', LpMinimize)


# La materia i se debe cursar en un unico cuatrimestre. Ademas, si es obligatoria, debe cursarse si o si.

prob += (Y_A_1 + Y_A_2 >= 1)
prob += (Y_A_1 + Y_A_2 <= 1)

prob += (Y_B_1 + Y_B_2 >= 1)
prob += (Y_B_1 + Y_B_2 <= 1)


# Numero de cuatrimestre en que es cursada la materia

prob += (1*Y_A_1 + 2*Y_A_2 - CA <= 0)
prob += (1*Y_A_1 + 2*Y_A_2 - CA >= 0)

prob += (1*Y_B_1 + 2*Y_B_2 - CB <= 0)
prob += (1*Y_B_1 + 2*Y_B_2 - CB >= 0)


# Los cuatrimestres de las correlativas deben ser menores



# La cantidad de materias por cuatrimestre no puede superar un valor maximo

prob += (Y_A_1 + Y_B_1 <= 2)
prob += (Y_A_2 + Y_B_2 <= 2)


#TOTAL_CUATRIMESTRES es el maximo de los Ci

prob += (TOTAL_CUATRIMESTRES >= 0)

prob += (CA <= TOTAL_CUATRIMESTRES)
prob += (-CA <= TOTAL_CUATRIMESTRES)

prob += (CB <= TOTAL_CUATRIMESTRES)
prob += (-CB <= TOTAL_CUATRIMESTRES)


# Calculo de creditos al terminar cada cuatrimestre

prob += (CRED0 <= 0)
prob += (CRED0 >= 0)
prob += (1*Y_A_1 + 1*Y_B_1 + CRED0 - CRED1 <= 0)
prob += (1*Y_A_1 + 1*Y_B_1 + CRED0 - CRED1 >= 0)

# Restricciones sobre aquellas materias que requieren creditos minimos para poder cursar


#Si la materia se cursa en ese cuatrimestre en ese curso en particular, entonces se debn cursar todos los horarios del mismo

prob += (H_A_Curso1A_1 <= R_A_Curso1A_LUNES_1_1)
prob += (H_A_Curso1A_1 >= R_A_Curso1A_LUNES_1_1)
prob += (H_A_Curso1A_1 <= R_A_Curso1A_LUNES_2_1)
prob += (H_A_Curso1A_1 >= R_A_Curso1A_LUNES_2_1)
prob += (H_A_Curso1A_1 <= R_A_Curso1A_LUNES_3_1)
prob += (H_A_Curso1A_1 >= R_A_Curso1A_LUNES_3_1)
prob += (R_A_Curso1A_LUNES_1_1 <= R_A_Curso1A_LUNES_2_1)
prob += (R_A_Curso1A_LUNES_1_1 >= R_A_Curso1A_LUNES_2_1)
prob += (R_A_Curso1A_LUNES_1_1 <= R_A_Curso1A_LUNES_3_1)
prob += (R_A_Curso1A_LUNES_1_1 >= R_A_Curso1A_LUNES_3_1)
prob += (R_A_Curso1A_LUNES_2_1 <= R_A_Curso1A_LUNES_3_1)
prob += (R_A_Curso1A_LUNES_2_1 >= R_A_Curso1A_LUNES_3_1)

prob += (H_A_Curso2A_1 <= R_A_Curso2A_LUNES_2_1)
prob += (H_A_Curso2A_1 >= R_A_Curso2A_LUNES_2_1)
prob += (H_A_Curso2A_1 <= R_A_Curso2A_LUNES_3_1)
prob += (H_A_Curso2A_1 >= R_A_Curso2A_LUNES_3_1)
prob += (H_A_Curso2A_1 <= R_A_Curso2A_LUNES_5_1)
prob += (H_A_Curso2A_1 >= R_A_Curso2A_LUNES_5_1)
prob += (H_A_Curso2A_1 <= R_A_Curso2A_LUNES_6_1)
prob += (H_A_Curso2A_1 >= R_A_Curso2A_LUNES_6_1)
prob += (H_A_Curso2A_1 <= R_A_Curso2A_LUNES_7_1)
prob += (H_A_Curso2A_1 >= R_A_Curso2A_LUNES_7_1)
prob += (R_A_Curso2A_LUNES_2_1 <= R_A_Curso2A_LUNES_3_1)
prob += (R_A_Curso2A_LUNES_2_1 >= R_A_Curso2A_LUNES_3_1)
prob += (R_A_Curso2A_LUNES_2_1 <= R_A_Curso2A_LUNES_5_1)
prob += (R_A_Curso2A_LUNES_2_1 >= R_A_Curso2A_LUNES_5_1)
prob += (R_A_Curso2A_LUNES_2_1 <= R_A_Curso2A_LUNES_6_1)
prob += (R_A_Curso2A_LUNES_2_1 >= R_A_Curso2A_LUNES_6_1)
prob += (R_A_Curso2A_LUNES_2_1 <= R_A_Curso2A_LUNES_7_1)
prob += (R_A_Curso2A_LUNES_2_1 >= R_A_Curso2A_LUNES_7_1)
prob += (R_A_Curso2A_LUNES_3_1 <= R_A_Curso2A_LUNES_5_1)
prob += (R_A_Curso2A_LUNES_3_1 >= R_A_Curso2A_LUNES_5_1)
prob += (R_A_Curso2A_LUNES_3_1 <= R_A_Curso2A_LUNES_6_1)
prob += (R_A_Curso2A_LUNES_3_1 >= R_A_Curso2A_LUNES_6_1)
prob += (R_A_Curso2A_LUNES_3_1 <= R_A_Curso2A_LUNES_7_1)
prob += (R_A_Curso2A_LUNES_3_1 >= R_A_Curso2A_LUNES_7_1)
prob += (R_A_Curso2A_LUNES_5_1 <= R_A_Curso2A_LUNES_6_1)
prob += (R_A_Curso2A_LUNES_5_1 >= R_A_Curso2A_LUNES_6_1)
prob += (R_A_Curso2A_LUNES_5_1 <= R_A_Curso2A_LUNES_7_1)
prob += (R_A_Curso2A_LUNES_5_1 >= R_A_Curso2A_LUNES_7_1)
prob += (R_A_Curso2A_LUNES_6_1 <= R_A_Curso2A_LUNES_7_1)
prob += (R_A_Curso2A_LUNES_6_1 >= R_A_Curso2A_LUNES_7_1)

prob += (H_A_Curso3A_1 <= R_A_Curso3A_LUNES_4_1)
prob += (H_A_Curso3A_1 >= R_A_Curso3A_LUNES_4_1)
prob += (H_A_Curso3A_1 <= R_A_Curso3A_LUNES_5_1)
prob += (H_A_Curso3A_1 >= R_A_Curso3A_LUNES_5_1)
prob += (H_A_Curso3A_1 <= R_A_Curso3A_LUNES_6_1)
prob += (H_A_Curso3A_1 >= R_A_Curso3A_LUNES_6_1)
prob += (R_A_Curso3A_LUNES_4_1 <= R_A_Curso3A_LUNES_5_1)
prob += (R_A_Curso3A_LUNES_4_1 >= R_A_Curso3A_LUNES_5_1)
prob += (R_A_Curso3A_LUNES_4_1 <= R_A_Curso3A_LUNES_6_1)
prob += (R_A_Curso3A_LUNES_4_1 >= R_A_Curso3A_LUNES_6_1)
prob += (R_A_Curso3A_LUNES_5_1 <= R_A_Curso3A_LUNES_6_1)
prob += (R_A_Curso3A_LUNES_5_1 >= R_A_Curso3A_LUNES_6_1)

prob += (H_B_Curso1B_1 <= R_B_Curso1B_LUNES_1_1)
prob += (H_B_Curso1B_1 >= R_B_Curso1B_LUNES_1_1)
prob += (H_B_Curso1B_1 <= R_B_Curso1B_LUNES_2_1)
prob += (H_B_Curso1B_1 >= R_B_Curso1B_LUNES_2_1)
prob += (H_B_Curso1B_1 <= R_B_Curso1B_LUNES_3_1)
prob += (H_B_Curso1B_1 >= R_B_Curso1B_LUNES_3_1)
prob += (R_B_Curso1B_LUNES_1_1 <= R_B_Curso1B_LUNES_2_1)
prob += (R_B_Curso1B_LUNES_1_1 >= R_B_Curso1B_LUNES_2_1)
prob += (R_B_Curso1B_LUNES_1_1 <= R_B_Curso1B_LUNES_3_1)
prob += (R_B_Curso1B_LUNES_1_1 >= R_B_Curso1B_LUNES_3_1)
prob += (R_B_Curso1B_LUNES_2_1 <= R_B_Curso1B_LUNES_3_1)
prob += (R_B_Curso1B_LUNES_2_1 >= R_B_Curso1B_LUNES_3_1)

prob += (H_B_Curso2B_1 <= R_B_Curso2B_LUNES_4_1)
prob += (H_B_Curso2B_1 >= R_B_Curso2B_LUNES_4_1)
prob += (H_B_Curso2B_1 <= R_B_Curso2B_LUNES_9_1)
prob += (H_B_Curso2B_1 >= R_B_Curso2B_LUNES_9_1)
prob += (R_B_Curso2B_LUNES_4_1 <= R_B_Curso2B_LUNES_9_1)
prob += (R_B_Curso2B_LUNES_4_1 >= R_B_Curso2B_LUNES_9_1)

prob += (H_B_Curso3B_1 <= R_B_Curso3B_LUNES_7_1)
prob += (H_B_Curso3B_1 >= R_B_Curso3B_LUNES_7_1)
prob += (H_B_Curso3B_1 <= R_B_Curso3B_LUNES_8_1)
prob += (H_B_Curso3B_1 >= R_B_Curso3B_LUNES_8_1)
prob += (H_B_Curso3B_1 <= R_B_Curso3B_LUNES_9_1)
prob += (H_B_Curso3B_1 >= R_B_Curso3B_LUNES_9_1)
prob += (H_B_Curso3B_1 <= R_B_Curso3B_LUNES_10_1)
prob += (H_B_Curso3B_1 >= R_B_Curso3B_LUNES_10_1)
prob += (R_B_Curso3B_LUNES_7_1 <= R_B_Curso3B_LUNES_8_1)
prob += (R_B_Curso3B_LUNES_7_1 >= R_B_Curso3B_LUNES_8_1)
prob += (R_B_Curso3B_LUNES_7_1 <= R_B_Curso3B_LUNES_9_1)
prob += (R_B_Curso3B_LUNES_7_1 >= R_B_Curso3B_LUNES_9_1)
prob += (R_B_Curso3B_LUNES_7_1 <= R_B_Curso3B_LUNES_10_1)
prob += (R_B_Curso3B_LUNES_7_1 >= R_B_Curso3B_LUNES_10_1)
prob += (R_B_Curso3B_LUNES_8_1 <= R_B_Curso3B_LUNES_9_1)
prob += (R_B_Curso3B_LUNES_8_1 >= R_B_Curso3B_LUNES_9_1)
prob += (R_B_Curso3B_LUNES_8_1 <= R_B_Curso3B_LUNES_10_1)
prob += (R_B_Curso3B_LUNES_8_1 >= R_B_Curso3B_LUNES_10_1)
prob += (R_B_Curso3B_LUNES_9_1 <= R_B_Curso3B_LUNES_10_1)
prob += (R_B_Curso3B_LUNES_9_1 >= R_B_Curso3B_LUNES_10_1)

prob += (H_B_Curso4B_1 <= R_B_Curso4B_LUNES_9_1)
prob += (H_B_Curso4B_1 >= R_B_Curso4B_LUNES_9_1)
prob += (H_B_Curso4B_1 <= R_B_Curso4B_LUNES_10_1)
prob += (H_B_Curso4B_1 >= R_B_Curso4B_LUNES_10_1)
prob += (R_B_Curso4B_LUNES_9_1 <= R_B_Curso4B_LUNES_10_1)
prob += (R_B_Curso4B_LUNES_9_1 >= R_B_Curso4B_LUNES_10_1)

prob += (H_A_Curso1A_2 <= R_A_Curso1A_LUNES_1_2)
prob += (H_A_Curso1A_2 >= R_A_Curso1A_LUNES_1_2)
prob += (H_A_Curso1A_2 <= R_A_Curso1A_LUNES_2_2)
prob += (H_A_Curso1A_2 >= R_A_Curso1A_LUNES_2_2)
prob += (H_A_Curso1A_2 <= R_A_Curso1A_LUNES_3_2)
prob += (H_A_Curso1A_2 >= R_A_Curso1A_LUNES_3_2)
prob += (R_A_Curso1A_LUNES_1_2 <= R_A_Curso1A_LUNES_2_2)
prob += (R_A_Curso1A_LUNES_1_2 >= R_A_Curso1A_LUNES_2_2)
prob += (R_A_Curso1A_LUNES_1_2 <= R_A_Curso1A_LUNES_3_2)
prob += (R_A_Curso1A_LUNES_1_2 >= R_A_Curso1A_LUNES_3_2)
prob += (R_A_Curso1A_LUNES_2_2 <= R_A_Curso1A_LUNES_3_2)
prob += (R_A_Curso1A_LUNES_2_2 >= R_A_Curso1A_LUNES_3_2)

prob += (H_A_Curso2A_2 <= R_A_Curso2A_LUNES_2_2)
prob += (H_A_Curso2A_2 >= R_A_Curso2A_LUNES_2_2)
prob += (H_A_Curso2A_2 <= R_A_Curso2A_LUNES_3_2)
prob += (H_A_Curso2A_2 >= R_A_Curso2A_LUNES_3_2)
prob += (H_A_Curso2A_2 <= R_A_Curso2A_LUNES_5_2)
prob += (H_A_Curso2A_2 >= R_A_Curso2A_LUNES_5_2)
prob += (H_A_Curso2A_2 <= R_A_Curso2A_LUNES_6_2)
prob += (H_A_Curso2A_2 >= R_A_Curso2A_LUNES_6_2)
prob += (H_A_Curso2A_2 <= R_A_Curso2A_LUNES_7_2)
prob += (H_A_Curso2A_2 >= R_A_Curso2A_LUNES_7_2)
prob += (R_A_Curso2A_LUNES_2_2 <= R_A_Curso2A_LUNES_3_2)
prob += (R_A_Curso2A_LUNES_2_2 >= R_A_Curso2A_LUNES_3_2)
prob += (R_A_Curso2A_LUNES_2_2 <= R_A_Curso2A_LUNES_5_2)
prob += (R_A_Curso2A_LUNES_2_2 >= R_A_Curso2A_LUNES_5_2)
prob += (R_A_Curso2A_LUNES_2_2 <= R_A_Curso2A_LUNES_6_2)
prob += (R_A_Curso2A_LUNES_2_2 >= R_A_Curso2A_LUNES_6_2)
prob += (R_A_Curso2A_LUNES_2_2 <= R_A_Curso2A_LUNES_7_2)
prob += (R_A_Curso2A_LUNES_2_2 >= R_A_Curso2A_LUNES_7_2)
prob += (R_A_Curso2A_LUNES_3_2 <= R_A_Curso2A_LUNES_5_2)
prob += (R_A_Curso2A_LUNES_3_2 >= R_A_Curso2A_LUNES_5_2)
prob += (R_A_Curso2A_LUNES_3_2 <= R_A_Curso2A_LUNES_6_2)
prob += (R_A_Curso2A_LUNES_3_2 >= R_A_Curso2A_LUNES_6_2)
prob += (R_A_Curso2A_LUNES_3_2 <= R_A_Curso2A_LUNES_7_2)
prob += (R_A_Curso2A_LUNES_3_2 >= R_A_Curso2A_LUNES_7_2)
prob += (R_A_Curso2A_LUNES_5_2 <= R_A_Curso2A_LUNES_6_2)
prob += (R_A_Curso2A_LUNES_5_2 >= R_A_Curso2A_LUNES_6_2)
prob += (R_A_Curso2A_LUNES_5_2 <= R_A_Curso2A_LUNES_7_2)
prob += (R_A_Curso2A_LUNES_5_2 >= R_A_Curso2A_LUNES_7_2)
prob += (R_A_Curso2A_LUNES_6_2 <= R_A_Curso2A_LUNES_7_2)
prob += (R_A_Curso2A_LUNES_6_2 >= R_A_Curso2A_LUNES_7_2)

prob += (H_A_Curso3A_2 <= R_A_Curso3A_LUNES_4_2)
prob += (H_A_Curso3A_2 >= R_A_Curso3A_LUNES_4_2)
prob += (H_A_Curso3A_2 <= R_A_Curso3A_LUNES_5_2)
prob += (H_A_Curso3A_2 >= R_A_Curso3A_LUNES_5_2)
prob += (H_A_Curso3A_2 <= R_A_Curso3A_LUNES_6_2)
prob += (H_A_Curso3A_2 >= R_A_Curso3A_LUNES_6_2)
prob += (R_A_Curso3A_LUNES_4_2 <= R_A_Curso3A_LUNES_5_2)
prob += (R_A_Curso3A_LUNES_4_2 >= R_A_Curso3A_LUNES_5_2)
prob += (R_A_Curso3A_LUNES_4_2 <= R_A_Curso3A_LUNES_6_2)
prob += (R_A_Curso3A_LUNES_4_2 >= R_A_Curso3A_LUNES_6_2)
prob += (R_A_Curso3A_LUNES_5_2 <= R_A_Curso3A_LUNES_6_2)
prob += (R_A_Curso3A_LUNES_5_2 >= R_A_Curso3A_LUNES_6_2)

prob += (H_B_Curso1B_2 <= R_B_Curso1B_LUNES_1_2)
prob += (H_B_Curso1B_2 >= R_B_Curso1B_LUNES_1_2)
prob += (H_B_Curso1B_2 <= R_B_Curso1B_LUNES_2_2)
prob += (H_B_Curso1B_2 >= R_B_Curso1B_LUNES_2_2)
prob += (H_B_Curso1B_2 <= R_B_Curso1B_LUNES_3_2)
prob += (H_B_Curso1B_2 >= R_B_Curso1B_LUNES_3_2)
prob += (R_B_Curso1B_LUNES_1_2 <= R_B_Curso1B_LUNES_2_2)
prob += (R_B_Curso1B_LUNES_1_2 >= R_B_Curso1B_LUNES_2_2)
prob += (R_B_Curso1B_LUNES_1_2 <= R_B_Curso1B_LUNES_3_2)
prob += (R_B_Curso1B_LUNES_1_2 >= R_B_Curso1B_LUNES_3_2)
prob += (R_B_Curso1B_LUNES_2_2 <= R_B_Curso1B_LUNES_3_2)
prob += (R_B_Curso1B_LUNES_2_2 >= R_B_Curso1B_LUNES_3_2)

prob += (H_B_Curso2B_2 <= R_B_Curso2B_LUNES_4_2)
prob += (H_B_Curso2B_2 >= R_B_Curso2B_LUNES_4_2)
prob += (H_B_Curso2B_2 <= R_B_Curso2B_LUNES_9_2)
prob += (H_B_Curso2B_2 >= R_B_Curso2B_LUNES_9_2)
prob += (R_B_Curso2B_LUNES_4_2 <= R_B_Curso2B_LUNES_9_2)
prob += (R_B_Curso2B_LUNES_4_2 >= R_B_Curso2B_LUNES_9_2)

prob += (H_B_Curso3B_2 <= R_B_Curso3B_LUNES_7_2)
prob += (H_B_Curso3B_2 >= R_B_Curso3B_LUNES_7_2)
prob += (H_B_Curso3B_2 <= R_B_Curso3B_LUNES_8_2)
prob += (H_B_Curso3B_2 >= R_B_Curso3B_LUNES_8_2)
prob += (H_B_Curso3B_2 <= R_B_Curso3B_LUNES_9_2)
prob += (H_B_Curso3B_2 >= R_B_Curso3B_LUNES_9_2)
prob += (H_B_Curso3B_2 <= R_B_Curso3B_LUNES_10_2)
prob += (H_B_Curso3B_2 >= R_B_Curso3B_LUNES_10_2)
prob += (R_B_Curso3B_LUNES_7_2 <= R_B_Curso3B_LUNES_8_2)
prob += (R_B_Curso3B_LUNES_7_2 >= R_B_Curso3B_LUNES_8_2)
prob += (R_B_Curso3B_LUNES_7_2 <= R_B_Curso3B_LUNES_9_2)
prob += (R_B_Curso3B_LUNES_7_2 >= R_B_Curso3B_LUNES_9_2)
prob += (R_B_Curso3B_LUNES_7_2 <= R_B_Curso3B_LUNES_10_2)
prob += (R_B_Curso3B_LUNES_7_2 >= R_B_Curso3B_LUNES_10_2)
prob += (R_B_Curso3B_LUNES_8_2 <= R_B_Curso3B_LUNES_9_2)
prob += (R_B_Curso3B_LUNES_8_2 >= R_B_Curso3B_LUNES_9_2)
prob += (R_B_Curso3B_LUNES_8_2 <= R_B_Curso3B_LUNES_10_2)
prob += (R_B_Curso3B_LUNES_8_2 >= R_B_Curso3B_LUNES_10_2)
prob += (R_B_Curso3B_LUNES_9_2 <= R_B_Curso3B_LUNES_10_2)
prob += (R_B_Curso3B_LUNES_9_2 >= R_B_Curso3B_LUNES_10_2)

prob += (H_B_Curso4B_2 <= R_B_Curso4B_LUNES_9_2)
prob += (H_B_Curso4B_2 >= R_B_Curso4B_LUNES_9_2)
prob += (H_B_Curso4B_2 <= R_B_Curso4B_LUNES_10_2)
prob += (H_B_Curso4B_2 >= R_B_Curso4B_LUNES_10_2)
prob += (R_B_Curso4B_LUNES_9_2 <= R_B_Curso4B_LUNES_10_2)
prob += (R_B_Curso4B_LUNES_9_2 >= R_B_Curso4B_LUNES_10_2)


#No hay giratiempos: Solo puede cursarse una materia en un unico curso en el mismo horario

prob += (LUNES_1_1 <= R_A_Curso1A_LUNES_1_1 + R_B_Curso1B_LUNES_1_1)
prob += (LUNES_1_1 >= R_A_Curso1A_LUNES_1_1 + R_B_Curso1B_LUNES_1_1)
prob += (LUNES_2_1 <= R_A_Curso1A_LUNES_2_1 + R_A_Curso2A_LUNES_2_1 + R_B_Curso1B_LUNES_2_1)
prob += (LUNES_2_1 >= R_A_Curso1A_LUNES_2_1 + R_A_Curso2A_LUNES_2_1 + R_B_Curso1B_LUNES_2_1)
prob += (LUNES_3_1 <= R_A_Curso1A_LUNES_3_1 + R_A_Curso2A_LUNES_3_1 + R_B_Curso1B_LUNES_3_1)
prob += (LUNES_3_1 >= R_A_Curso1A_LUNES_3_1 + R_A_Curso2A_LUNES_3_1 + R_B_Curso1B_LUNES_3_1)
prob += (LUNES_4_1 <= R_A_Curso3A_LUNES_4_1 + R_B_Curso2B_LUNES_4_1)
prob += (LUNES_4_1 >= R_A_Curso3A_LUNES_4_1 + R_B_Curso2B_LUNES_4_1)
prob += (LUNES_5_1 <= R_A_Curso2A_LUNES_5_1 + R_A_Curso3A_LUNES_5_1)
prob += (LUNES_5_1 >= R_A_Curso2A_LUNES_5_1 + R_A_Curso3A_LUNES_5_1)
prob += (LUNES_6_1 <= R_A_Curso2A_LUNES_6_1 + R_A_Curso3A_LUNES_6_1)
prob += (LUNES_6_1 >= R_A_Curso2A_LUNES_6_1 + R_A_Curso3A_LUNES_6_1)
prob += (LUNES_7_1 <= R_A_Curso2A_LUNES_7_1 + R_B_Curso3B_LUNES_7_1)
prob += (LUNES_7_1 >= R_A_Curso2A_LUNES_7_1 + R_B_Curso3B_LUNES_7_1)
prob += (LUNES_8_1 <= R_B_Curso3B_LUNES_8_1)
prob += (LUNES_8_1 >= R_B_Curso3B_LUNES_8_1)
prob += (LUNES_9_1 <= R_B_Curso2B_LUNES_9_1 + R_B_Curso3B_LUNES_9_1 + R_B_Curso4B_LUNES_9_1)
prob += (LUNES_9_1 >= R_B_Curso2B_LUNES_9_1 + R_B_Curso3B_LUNES_9_1 + R_B_Curso4B_LUNES_9_1)
prob += (LUNES_10_1 <= R_B_Curso3B_LUNES_10_1 + R_B_Curso4B_LUNES_10_1)
prob += (LUNES_10_1 >= R_B_Curso3B_LUNES_10_1 + R_B_Curso4B_LUNES_10_1)
prob += (LUNES_11_1 <= 0)
prob += (LUNES_11_1 >= 0)
prob += (LUNES_12_1 <= 0)
prob += (LUNES_12_1 >= 0)
prob += (LUNES_1_2 <= R_A_Curso1A_LUNES_1_2 + R_B_Curso1B_LUNES_1_2)
prob += (LUNES_1_2 >= R_A_Curso1A_LUNES_1_2 + R_B_Curso1B_LUNES_1_2)
prob += (LUNES_2_2 <= R_A_Curso1A_LUNES_2_2 + R_A_Curso2A_LUNES_2_2 + R_B_Curso1B_LUNES_2_2)
prob += (LUNES_2_2 >= R_A_Curso1A_LUNES_2_2 + R_A_Curso2A_LUNES_2_2 + R_B_Curso1B_LUNES_2_2)
prob += (LUNES_3_2 <= R_A_Curso1A_LUNES_3_2 + R_A_Curso2A_LUNES_3_2 + R_B_Curso1B_LUNES_3_2)
prob += (LUNES_3_2 >= R_A_Curso1A_LUNES_3_2 + R_A_Curso2A_LUNES_3_2 + R_B_Curso1B_LUNES_3_2)
prob += (LUNES_4_2 <= R_A_Curso3A_LUNES_4_2 + R_B_Curso2B_LUNES_4_2)
prob += (LUNES_4_2 >= R_A_Curso3A_LUNES_4_2 + R_B_Curso2B_LUNES_4_2)
prob += (LUNES_5_2 <= R_A_Curso2A_LUNES_5_2 + R_A_Curso3A_LUNES_5_2)
prob += (LUNES_5_2 >= R_A_Curso2A_LUNES_5_2 + R_A_Curso3A_LUNES_5_2)
prob += (LUNES_6_2 <= R_A_Curso2A_LUNES_6_2 + R_A_Curso3A_LUNES_6_2)
prob += (LUNES_6_2 >= R_A_Curso2A_LUNES_6_2 + R_A_Curso3A_LUNES_6_2)
prob += (LUNES_7_2 <= R_A_Curso2A_LUNES_7_2 + R_B_Curso3B_LUNES_7_2)
prob += (LUNES_7_2 >= R_A_Curso2A_LUNES_7_2 + R_B_Curso3B_LUNES_7_2)
prob += (LUNES_8_2 <= R_B_Curso3B_LUNES_8_2)
prob += (LUNES_8_2 >= R_B_Curso3B_LUNES_8_2)
prob += (LUNES_9_2 <= R_B_Curso2B_LUNES_9_2 + R_B_Curso3B_LUNES_9_2 + R_B_Curso4B_LUNES_9_2)
prob += (LUNES_9_2 >= R_B_Curso2B_LUNES_9_2 + R_B_Curso3B_LUNES_9_2 + R_B_Curso4B_LUNES_9_2)
prob += (LUNES_10_2 <= R_B_Curso3B_LUNES_10_2 + R_B_Curso4B_LUNES_10_2)
prob += (LUNES_10_2 >= R_B_Curso3B_LUNES_10_2 + R_B_Curso4B_LUNES_10_2)
prob += (LUNES_11_2 <= 0)
prob += (LUNES_11_2 >= 0)
prob += (LUNES_12_2 <= 0)
prob += (LUNES_12_2 >= 0)

# Si la materia no se cursa ese cuatrimestre, entonces no puede cursarse en ninguno de los cursos de ese cuatrimestre

prob += (Y_A_1 >= H_A_Curso1A_1)
prob += (Y_A_1 >= H_A_Curso2A_1)
prob += (Y_A_1 >= H_A_Curso3A_1)
prob += (Y_B_1 >= H_B_Curso1B_1)
prob += (Y_B_1 >= H_B_Curso2B_1)
prob += (Y_B_1 >= H_B_Curso3B_1)
prob += (Y_B_1 >= H_B_Curso4B_1)
prob += (Y_A_2 >= H_A_Curso1A_2)
prob += (Y_A_2 >= H_A_Curso2A_2)
prob += (Y_A_2 >= H_A_Curso3A_2)
prob += (Y_B_2 >= H_B_Curso1B_2)
prob += (Y_B_2 >= H_B_Curso2B_2)
prob += (Y_B_2 >= H_B_Curso3B_2)
prob += (Y_B_2 >= H_B_Curso4B_2)

# La materia no puede cursarse en mas de un curso en el cuatrimestre

prob += (Y_A_1 <= H_A_Curso1A_1 + H_A_Curso2A_1 + H_A_Curso3A_1)
prob += (Y_B_1 <= H_B_Curso1B_1 + H_B_Curso2B_1 + H_B_Curso3B_1 + H_B_Curso4B_1)
prob += (Y_A_2 <= H_A_Curso1A_2 + H_A_Curso2A_2 + H_A_Curso3A_2)
prob += (Y_B_2 <= H_B_Curso1B_2 + H_B_Curso2B_2 + H_B_Curso3B_2 + H_B_Curso4B_2)

#Numero de franja horaria mayor por dia por cuatrimestre

prob += (MAXIMA_FRANJA_LUNES_1 >= 1 * LUNES_1_1 )
prob += (MAXIMA_FRANJA_LUNES_1 >= 2 * LUNES_2_1 )
prob += (MAXIMA_FRANJA_LUNES_1 >= 3 * LUNES_3_1 )
prob += (MAXIMA_FRANJA_LUNES_1 >= 4 * LUNES_4_1 )
prob += (MAXIMA_FRANJA_LUNES_1 >= 5 * LUNES_5_1 )
prob += (MAXIMA_FRANJA_LUNES_1 >= 6 * LUNES_6_1 )
prob += (MAXIMA_FRANJA_LUNES_1 >= 7 * LUNES_7_1 )
prob += (MAXIMA_FRANJA_LUNES_1 >= 8 * LUNES_8_1 )
prob += (MAXIMA_FRANJA_LUNES_1 >= 9 * LUNES_9_1 )
prob += (MAXIMA_FRANJA_LUNES_1 >= 10 * LUNES_10_1 )
prob += (MAXIMA_FRANJA_LUNES_1 >= 11 * LUNES_11_1 )
prob += (MAXIMA_FRANJA_LUNES_1 >= 12 * LUNES_12_1 )
prob += (MAXIMA_FRANJA_LUNES_2 >= 1 * LUNES_1_2 )
prob += (MAXIMA_FRANJA_LUNES_2 >= 2 * LUNES_2_2 )
prob += (MAXIMA_FRANJA_LUNES_2 >= 3 * LUNES_3_2 )
prob += (MAXIMA_FRANJA_LUNES_2 >= 4 * LUNES_4_2 )
prob += (MAXIMA_FRANJA_LUNES_2 >= 5 * LUNES_5_2 )
prob += (MAXIMA_FRANJA_LUNES_2 >= 6 * LUNES_6_2 )
prob += (MAXIMA_FRANJA_LUNES_2 >= 7 * LUNES_7_2 )
prob += (MAXIMA_FRANJA_LUNES_2 >= 8 * LUNES_8_2 )
prob += (MAXIMA_FRANJA_LUNES_2 >= 9 * LUNES_9_2 )
prob += (MAXIMA_FRANJA_LUNES_2 >= 10 * LUNES_10_2 )
prob += (MAXIMA_FRANJA_LUNES_2 >= 11 * LUNES_11_2 )
prob += (MAXIMA_FRANJA_LUNES_2 >= 12 * LUNES_12_2 )

#Numero de franja horaria menor por dia por cuatrimestre

prob += (MINIMA_FRANJA_LUNES_1 <= 1 * LUNES_1_1 + (1 - LUNES_1_1) * 10000 )
prob += (MINIMA_FRANJA_LUNES_1 <= 2 * LUNES_2_1 + (1 - LUNES_2_1) * 10000 )
prob += (MINIMA_FRANJA_LUNES_1 <= 3 * LUNES_3_1 + (1 - LUNES_3_1) * 10000 )
prob += (MINIMA_FRANJA_LUNES_1 <= 4 * LUNES_4_1 + (1 - LUNES_4_1) * 10000 )
prob += (MINIMA_FRANJA_LUNES_1 <= 5 * LUNES_5_1 + (1 - LUNES_5_1) * 10000 )
prob += (MINIMA_FRANJA_LUNES_1 <= 6 * LUNES_6_1 + (1 - LUNES_6_1) * 10000 )
prob += (MINIMA_FRANJA_LUNES_1 <= 7 * LUNES_7_1 + (1 - LUNES_7_1) * 10000 )
prob += (MINIMA_FRANJA_LUNES_1 <= 8 * LUNES_8_1 + (1 - LUNES_8_1) * 10000 )
prob += (MINIMA_FRANJA_LUNES_1 <= 9 * LUNES_9_1 + (1 - LUNES_9_1) * 10000 )
prob += (MINIMA_FRANJA_LUNES_1 <= 10 * LUNES_10_1 + (1 - LUNES_10_1) * 10000 )
prob += (MINIMA_FRANJA_LUNES_1 <= 11 * LUNES_11_1 + (1 - LUNES_11_1) * 10000 )
prob += (MINIMA_FRANJA_LUNES_1 <= 12 * LUNES_12_1 + (1 - LUNES_12_1) * 10000 )
prob += (MINIMA_FRANJA_LUNES_1 <= OCUPADO_LUNES_1 * 10000)
prob += (MINIMA_FRANJA_LUNES_2 <= 1 * LUNES_1_2 + (1 - LUNES_1_2) * 10000 )
prob += (MINIMA_FRANJA_LUNES_2 <= 2 * LUNES_2_2 + (1 - LUNES_2_2) * 10000 )
prob += (MINIMA_FRANJA_LUNES_2 <= 3 * LUNES_3_2 + (1 - LUNES_3_2) * 10000 )
prob += (MINIMA_FRANJA_LUNES_2 <= 4 * LUNES_4_2 + (1 - LUNES_4_2) * 10000 )
prob += (MINIMA_FRANJA_LUNES_2 <= 5 * LUNES_5_2 + (1 - LUNES_5_2) * 10000 )
prob += (MINIMA_FRANJA_LUNES_2 <= 6 * LUNES_6_2 + (1 - LUNES_6_2) * 10000 )
prob += (MINIMA_FRANJA_LUNES_2 <= 7 * LUNES_7_2 + (1 - LUNES_7_2) * 10000 )
prob += (MINIMA_FRANJA_LUNES_2 <= 8 * LUNES_8_2 + (1 - LUNES_8_2) * 10000 )
prob += (MINIMA_FRANJA_LUNES_2 <= 9 * LUNES_9_2 + (1 - LUNES_9_2) * 10000 )
prob += (MINIMA_FRANJA_LUNES_2 <= 10 * LUNES_10_2 + (1 - LUNES_10_2) * 10000 )
prob += (MINIMA_FRANJA_LUNES_2 <= 11 * LUNES_11_2 + (1 - LUNES_11_2) * 10000 )
prob += (MINIMA_FRANJA_LUNES_2 <= 12 * LUNES_12_2 + (1 - LUNES_12_2) * 10000 )
prob += (MINIMA_FRANJA_LUNES_2 <= OCUPADO_LUNES_2 * 10000)

#Si alguna de las franjas horarias del dia esta ocupada, entonces el dia esta ocupado

prob += (OCUPADO_LUNES_1 >= LUNES_1_1 )
prob += (OCUPADO_LUNES_1 >= LUNES_2_1 )
prob += (OCUPADO_LUNES_1 >= LUNES_3_1 )
prob += (OCUPADO_LUNES_1 >= LUNES_4_1 )
prob += (OCUPADO_LUNES_1 >= LUNES_5_1 )
prob += (OCUPADO_LUNES_1 >= LUNES_6_1 )
prob += (OCUPADO_LUNES_1 >= LUNES_7_1 )
prob += (OCUPADO_LUNES_1 >= LUNES_8_1 )
prob += (OCUPADO_LUNES_1 >= LUNES_9_1 )
prob += (OCUPADO_LUNES_1 >= LUNES_10_1 )
prob += (OCUPADO_LUNES_1 >= LUNES_11_1 )
prob += (OCUPADO_LUNES_1 >= LUNES_12_1 )
prob += (OCUPADO_LUNES_1 <= LUNES_1_1 + LUNES_2_1 + LUNES_3_1 + LUNES_4_1 + LUNES_5_1 + LUNES_6_1 + LUNES_7_1 + LUNES_8_1 + LUNES_9_1 + LUNES_10_1 + LUNES_11_1 + LUNES_12_1)

prob += (OCUPADO_LUNES_2 >= LUNES_1_2 )
prob += (OCUPADO_LUNES_2 >= LUNES_2_2 )
prob += (OCUPADO_LUNES_2 >= LUNES_3_2 )
prob += (OCUPADO_LUNES_2 >= LUNES_4_2 )
prob += (OCUPADO_LUNES_2 >= LUNES_5_2 )
prob += (OCUPADO_LUNES_2 >= LUNES_6_2 )
prob += (OCUPADO_LUNES_2 >= LUNES_7_2 )
prob += (OCUPADO_LUNES_2 >= LUNES_8_2 )
prob += (OCUPADO_LUNES_2 >= LUNES_9_2 )
prob += (OCUPADO_LUNES_2 >= LUNES_10_2 )
prob += (OCUPADO_LUNES_2 >= LUNES_11_2 )
prob += (OCUPADO_LUNES_2 >= LUNES_12_2 )
prob += (OCUPADO_LUNES_2 <= LUNES_1_2 + LUNES_2_2 + LUNES_3_2 + LUNES_4_2 + LUNES_5_2 + LUNES_6_2 + LUNES_7_2 + LUNES_8_2 + LUNES_9_2 + LUNES_10_2 + LUNES_11_2 + LUNES_12_2)

#Calcular la cantidad de franjas libres entre la primer y la ultima franja ocupada en el dia.
#Si en el dia no se cursan materias, da 0.

prob += (MAXIMA_FRANJA_LUNES_1 + OCUPADO_LUNES_1 - MINIMA_FRANJA_LUNES_1 - (LUNES_1_1 + LUNES_2_1 + LUNES_3_1 + LUNES_4_1 + LUNES_5_1 + LUNES_6_1 + LUNES_7_1 + LUNES_8_1 + LUNES_9_1 + LUNES_10_1 + LUNES_11_1 + LUNES_12_1) <= HORAS_LIBRES_LUNES_1)
prob += (MAXIMA_FRANJA_LUNES_1 + OCUPADO_LUNES_1 - MINIMA_FRANJA_LUNES_1 - (LUNES_1_1 + LUNES_2_1 + LUNES_3_1 + LUNES_4_1 + LUNES_5_1 + LUNES_6_1 + LUNES_7_1 + LUNES_8_1 + LUNES_9_1 + LUNES_10_1 + LUNES_11_1 + LUNES_12_1) >= HORAS_LIBRES_LUNES_1)
prob += (MAXIMA_FRANJA_LUNES_2 + OCUPADO_LUNES_2 - MINIMA_FRANJA_LUNES_2 - (LUNES_1_2 + LUNES_2_2 + LUNES_3_2 + LUNES_4_2 + LUNES_5_2 + LUNES_6_2 + LUNES_7_2 + LUNES_8_2 + LUNES_9_2 + LUNES_10_2 + LUNES_11_2 + LUNES_12_2) <= HORAS_LIBRES_LUNES_2)
prob += (MAXIMA_FRANJA_LUNES_2 + OCUPADO_LUNES_2 - MINIMA_FRANJA_LUNES_2 - (LUNES_1_2 + LUNES_2_2 + LUNES_3_2 + LUNES_4_2 + LUNES_5_2 + LUNES_6_2 + LUNES_7_2 + LUNES_8_2 + LUNES_9_2 + LUNES_10_2 + LUNES_11_2 + LUNES_12_2) >= HORAS_LIBRES_LUNES_2)

#Total de horas libres entre materias en el plan, es la suma de las horas libres de cada dia por cuatrimestre

prob += (HORAS_LIBRES_LUNES_1 + HORAS_LIBRES_LUNES_2 <= HORAS_LIBRES_TOTALES)
prob += (HORAS_LIBRES_LUNES_1 + HORAS_LIBRES_LUNES_2 >= HORAS_LIBRES_TOTALES)

# Definicion de la funcion objetivo a minimizar.

prob += 1*TOTAL_CUATRIMESTRES + 1*HORAS_LIBRES_TOTALES

# Resolucion del problema

tiempo_inicial = time()
status = prob.solve(GLPK(msg=0))

tiempo_final = time()
print('Duracion: {}'.format(tiempo_final - tiempo_inicial))
# Impresion de resultados por pantalla

print('Total de cuatrimestres: {}'.format(value(TOTAL_CUATRIMESTRES)))

plan_final = []
for i in range(value(TOTAL_CUATRIMESTRES)):
    plan_final.append([])
msj = 'Materia {} se hace en el cuatrimestre {}'
if value(CA) > 0:
    plan_final[value(CA)-1].append('A')
    print(msj.format('A', value(CA)))
else:
    print('La materia A no se hace')
if value(CB) > 0:
    plan_final[value(CB)-1].append('B')
    print(msj.format('B', value(CB)))
else:
    print('La materia B no se hace')
print(plan_final)
print('Total de horas libres: {}'.format(value(HORAS_LIBRES_TOTALES)))
msj = 'Cuatrimestre: {} - Creditos acumulados: {}'
print(msj.format(0, value(CRED0)))
print(msj.format(1, value(CRED1)))
print('OCUPADO_LUNES_1: {}'.format(value(OCUPADO_LUNES_1)))
print('MAXIMA_FRANJA_LUNES_1: {}'.format(value(MAXIMA_FRANJA_LUNES_1)))
print('MINIMA_FRANJA_LUNES_1: {}'.format(value(MINIMA_FRANJA_LUNES_1)))
print('HORAS_LIBRES_LUNES_1: {}'.format(value(HORAS_LIBRES_LUNES_1)))
print('OCUPADO_LUNES_2: {}'.format(value(OCUPADO_LUNES_2)))
print('MAXIMA_FRANJA_LUNES_2: {}'.format(value(MAXIMA_FRANJA_LUNES_2)))
print('MINIMA_FRANJA_LUNES_2: {}'.format(value(MINIMA_FRANJA_LUNES_2)))
print('HORAS_LIBRES_LUNES_2: {}'.format(value(HORAS_LIBRES_LUNES_2)))
print('HORAS_LIBRES_TOTALES: {}'.format(value(HORAS_LIBRES_TOTALES)))
print('LUNES_1_1: {}'.format(value(LUNES_1_1)))
print('LUNES_2_1: {}'.format(value(LUNES_2_1)))
print('LUNES_3_1: {}'.format(value(LUNES_3_1)))
print('LUNES_4_1: {}'.format(value(LUNES_4_1)))
print('LUNES_5_1: {}'.format(value(LUNES_5_1)))
print('LUNES_6_1: {}'.format(value(LUNES_6_1)))
print('LUNES_7_1: {}'.format(value(LUNES_7_1)))
print('LUNES_8_1: {}'.format(value(LUNES_8_1)))
print('LUNES_9_1: {}'.format(value(LUNES_9_1)))
print('LUNES_10_1: {}'.format(value(LUNES_10_1)))
print('LUNES_11_1: {}'.format(value(LUNES_11_1)))
print('LUNES_12_1: {}'.format(value(LUNES_12_1)))
print('LUNES_1_2: {}'.format(value(LUNES_1_2)))
print('LUNES_2_2: {}'.format(value(LUNES_2_2)))
print('LUNES_3_2: {}'.format(value(LUNES_3_2)))
print('LUNES_4_2: {}'.format(value(LUNES_4_2)))
print('LUNES_5_2: {}'.format(value(LUNES_5_2)))
print('LUNES_6_2: {}'.format(value(LUNES_6_2)))
print('LUNES_7_2: {}'.format(value(LUNES_7_2)))
print('LUNES_8_2: {}'.format(value(LUNES_8_2)))
print('LUNES_9_2: {}'.format(value(LUNES_9_2)))
print('LUNES_10_2: {}'.format(value(LUNES_10_2)))
print('LUNES_11_2: {}'.format(value(LUNES_11_2)))
print('LUNES_12_2: {}'.format(value(LUNES_12_2)))
if value(H_A_Curso1A_1):
    print('Valor de H_A_Curso1A_1 en cuatrimestre 1: {}'.format(value(H_A_Curso1A_1)))
if value(H_A_Curso2A_1):
    print('Valor de H_A_Curso2A_1 en cuatrimestre 1: {}'.format(value(H_A_Curso2A_1)))
if value(H_A_Curso3A_1):
    print('Valor de H_A_Curso3A_1 en cuatrimestre 1: {}'.format(value(H_A_Curso3A_1)))
if value(H_A_Curso1A_2):
    print('Valor de H_A_Curso1A_2 en cuatrimestre 2: {}'.format(value(H_A_Curso1A_2)))
if value(H_A_Curso2A_2):
    print('Valor de H_A_Curso2A_2 en cuatrimestre 2: {}'.format(value(H_A_Curso2A_2)))
if value(H_A_Curso3A_2):
    print('Valor de H_A_Curso3A_2 en cuatrimestre 2: {}'.format(value(H_A_Curso3A_2)))
if value(H_B_Curso1B_1):
    print('Valor de H_B_Curso1B_1 en cuatrimestre 1: {}'.format(value(H_B_Curso1B_1)))
if value(H_B_Curso2B_1):
    print('Valor de H_B_Curso2B_1 en cuatrimestre 1: {}'.format(value(H_B_Curso2B_1)))
if value(H_B_Curso3B_1):
    print('Valor de H_B_Curso3B_1 en cuatrimestre 1: {}'.format(value(H_B_Curso3B_1)))
if value(H_B_Curso4B_1):
    print('Valor de H_B_Curso4B_1 en cuatrimestre 1: {}'.format(value(H_B_Curso4B_1)))
if value(H_B_Curso1B_2):
    print('Valor de H_B_Curso1B_2 en cuatrimestre 2: {}'.format(value(H_B_Curso1B_2)))
if value(H_B_Curso2B_2):
    print('Valor de H_B_Curso2B_2 en cuatrimestre 2: {}'.format(value(H_B_Curso2B_2)))
if value(H_B_Curso3B_2):
    print('Valor de H_B_Curso3B_2 en cuatrimestre 2: {}'.format(value(H_B_Curso3B_2)))
if value(H_B_Curso4B_2):
    print('Valor de H_B_Curso4B_2 en cuatrimestre 2: {}'.format(value(H_B_Curso4B_2)))
