DIAS = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES", "SABADO"]


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