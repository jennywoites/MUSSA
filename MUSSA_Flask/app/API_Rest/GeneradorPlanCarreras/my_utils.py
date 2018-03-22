import datetime

def get_str_cuatrimestre(cuatrimestre):
    cuatrimestre = int(str(cuatrimestre))
    if cuatrimestre < 10:
        return "0" + str(cuatrimestre)
    return str(cuatrimestre)


def es_par(num):
    return num % 2 == 0

def get_str_fecha_y_hora_actual():
    return '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

def es_horario_valido_para_el_cuatrimestre(parametros, curso, cuatrimestre):
    if parametros.primer_cuatrimestre_es_impar:
        if not es_par(cuatrimestre): #Es un primer cuatrimestre del anio
            return curso.se_dicta_primer_cuatrimestre

        return curso.se_dicta_segundo_cuatrimestre

    if not es_par(cuatrimestre): #Es un segundo cuatrimestre del anio
        return curso.se_dicta_segundo_cuatrimestre

    return curso.se_dicta_primer_cuatrimestre

def convertir_tiempo(tiempo):
    minutos = tiempo // 60
    segundos = tiempo - minutos * 60
    horas = minutos // 60
    minutos = minutos - horas * 60

    msj = ""
    if horas > 0:
        msj += "{} horas, ".format(horas)

    if minutos > 0:
        msj += "{} minutos, ".format(minutos)

    msj += "{0:.2f} segundos".format(segundos)
    return msj