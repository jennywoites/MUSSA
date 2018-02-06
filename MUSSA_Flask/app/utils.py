from datetime import datetime

DIAS = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES", "SABADO"]

#####################################################################
##                     
#####################################################################
def generar_lista_anios():
    MAX_TIEMPO = 5
    hoy = datetime.now().year
    return [x for x in range(hoy, hoy - MAX_TIEMPO, -1)]

def generar_lista_horarios():
    HORA_MIN = 7
    HORA_MAX = 23
    horarios = []
    for i in frange(HORA_MIN, HORA_MAX + 0.5, 0.5):
        hora = int(i)
        minutos = "00" if hora == i else "30"
        horarios.append("{}:{}".format(get_numero_dos_digitos(hora), minutos))
    return horarios

def convertir_horario(horas, minutos):
    c_hora = int(horas)
    c_hora += 0.5 if int(minutos) == 30 else 0
    return c_hora

def frange(start, stop, step):
    i = start
    while i < stop:
        yield i
        i += step


def get_numero_dos_digitos(num):
    num = str(num)
    if len(num) < 2:
        return "0{}".format(num)
    return num