DIAS = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES", "SABADO"]

#####################################################################
##                     
#####################################################################

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