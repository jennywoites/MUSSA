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

Y_B_01 = LpVariable(name='Y_B_01', cat='Binary')
Y_B_02 = LpVariable(name='Y_B_02', cat='Binary')
Y_B_03 = LpVariable(name='Y_B_03', cat='Binary')
Y_C_01 = LpVariable(name='Y_C_01', cat='Binary')
Y_C_02 = LpVariable(name='Y_C_02', cat='Binary')
Y_C_03 = LpVariable(name='Y_C_03', cat='Binary')
Y_A_01 = LpVariable(name='Y_A_01', cat='Binary')
Y_A_02 = LpVariable(name='Y_A_02', cat='Binary')
Y_A_03 = LpVariable(name='Y_A_03', cat='Binary')


#Ci: Numero de cuatrimestre en que se hace la materia con id i. Ejemplo, si Ci=3 es que la materia i se hace el cuatrimestre numero 3

CB = LpVariable(name='CB', lowBound=0, upBound=3, cat='Integer')
CC = LpVariable(name='CC', lowBound=0, upBound=3, cat='Integer')
CA = LpVariable(name='CA', lowBound=0, upBound=3, cat='Integer')


#TOTAL_CUATRIMESTRES: Total de cuatrimestres a cursar. Utilizada para escribir el maximo entre Ci MAX(CA, CB..)

TOTAL_CUATRIMESTRES = LpVariable(name='TOTAL_CUATRIMESTRES', lowBound=0, upBound=3, cat='Integer')
#CREDi: Cantidad de creditos al final del cuatrimestre i

CRED01 = LpVariable(name='CRED01', lowBound=0, upBound=10000, cat='Integer')
CRED02 = LpVariable(name='CRED02', lowBound=0, upBound=10000, cat='Integer')
CRED03 = LpVariable(name='CRED03', lowBound=0, upBound=10000, cat='Integer')


#H_{id_materia i}_{id curso j}_{cuatrimestre k}: La materia i se cursa en el curso j en el cuatrimestre k

H_B_B_01 = LpVariable(name='H_B_B_01', cat='Binary')
H_C_C_01 = LpVariable(name='H_C_C_01', cat='Binary')
H_A_A_01 = LpVariable(name='H_A_A_01', cat='Binary')
H_B_B_02 = LpVariable(name='H_B_B_02', cat='Binary')
H_C_C_02 = LpVariable(name='H_C_C_02', cat='Binary')
H_A_A_02 = LpVariable(name='H_A_A_02', cat='Binary')
H_B_B_03 = LpVariable(name='H_B_B_03', cat='Binary')
H_C_C_03 = LpVariable(name='H_C_C_03', cat='Binary')
H_A_A_03 = LpVariable(name='H_A_A_03', cat='Binary')


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


#R_{id_materia}_{id curso}_{dia}_{franja}_{cuatrimestre}: El horario para la materia y curso en ese cuatrimestre esta habilitado

